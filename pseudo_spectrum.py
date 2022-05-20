import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import re

#==================Function==================
def Sd_calculate(w,damp_ratio,eq_data,component,filtered=False): #TODO 需優化!!
    if filtered==True:
        component+="_filtered"

    for i in range(len(w)):
        num=1
        den=(1,2*damp_ratio*w[i],w[i]*w[i])
        system = (num, den)
        t1, yout, xout = ss.lsim(system,eq_data[f"{component}"],eq_data["Time"])
        Sd[i]=max(abs(yout))
    return Sd


def onclick(event):
    global plot_time
    plot_time+=1
    # print(plot_time)
    
    ix, iy = float(event.xdata), float(event.ydata) #record mouse click period value

    # print(f"Period:{ix} (sec)")
    # print(f" high bandpass as {1/ix} Hz")
    filter_value[f"{component} bandpass_boundary (Hz)"]=np.round(1/ix,2)
    filter_value[f"{component} usable_period (sec)"]=np.round(ix/1.25,4)

    if plot_time>0:
        ax.clear()
        ax.plot(T,Sv,color="gray")
        ax.set_xlabel("Period (sec)")
        ax.set_ylabel("PSV (cm/sec)")
        ax.set_title(f"{Sta_name} {component} high bandpass filtering\n pseudo velocity respond spectrum" )
        ax.axvline(ix,color="purple")
        ax.axvline(ix/1.25,color="red",linestyle="--")
        canvas.draw()

def close_win():
    win.destroy()

#============parameter================
data_list=os.listdir("./event")
#TODO
data_num=7
Sta_name=re.findall(r"\w*\d+",data_list[data_num])[0]
damp_ratio=0.05 #阻尼比
t0,t,dt=0.01,10,0.05 #period
#======================================
print(Sta_name)
T=np.arange(t0,t+dt,dt)
w=2*np.pi/T #結構自然頻率
Sd=np.zeros(len(T)) #pseudo displacement

path=f"./result/{Sta_name}"
if not os.path.isdir(path):
    os.makedirs(path)

#read data
eq_data=pd.read_csv(f"event/{Sta_name}_acc.csv",usecols=[0,1,2,3]) #讀入原始地震資料
column=["Period (sec)","Vertical_PSV (cm/sec)","NS_PSV (cm/sec)","EW_PSV (cm/sec)","Vertical_PSA (gal)","NS_PSA (gal)","EW_PSA (gal)"]

pseudo_table=pd.DataFrame(0,columns=column,index=range(len(T)))
# plt.plot(eq_data["Time"],eq_data["Vertical"])

for component in ["Vertical","NS","EW"]:
    #plot waveform
    fig, ax=plt.subplots(figsize=(7,7))
    ax.plot(eq_data["Time"],eq_data[f"{component}"])
    ax.set_title(f"no filtered original waveform ({component})")
    ax.set_xlabel("time (sec)")
    ax.set_ylabel("gal")
    # fig.savefig(f"{path}/no filtered original waveform ({component}).png",dpi=300)

    #calculate Sd & Sv
    Sd=Sd_calculate(w,damp_ratio,eq_data,component,filtered=False)
    Sv=Sd*w #pseudo velocity

    #============看可用的週期範圍, 點選要高通濾波的截止頻率==============
    win=tk.Tk()
    win.title(f"{Sta_name} {component}_filtering")
    win.geometry("700x650+10+10")
    win.maxsize(1000,700)
    filter_value={}
    plot_time=0

    #original filter plot
    fig, ax=plt.subplots(figsize=(7,7))
    ax.plot(T,Sv,color="gray")
    ax.set_xlabel("Period (sec)")
    ax.set_ylabel("PSV (cm/sec)")
    ax.set_title(f"{Sta_name} {component} high bandpass filtering\n pseudo velocity respond spectrum" )

    canvas=FigureCanvasTkAgg(fig,win)
    canvas.mpl_connect('button_press_event', onclick)
    canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

    close_btn=tk.Button(win,text="Close",command=close_win)
    close_btn.pack(side="bottom")

    win.mainloop()

    #==========進行低通濾波=========

    sample_rate=200 #取樣頻率 (Hz)
    order=4 #4階
    lb_cutoff_freq=10  #(Hz)截至頻率
    Wn=2*lb_cutoff_freq/sample_rate #Wn 是正規化的截止頻率，介於 0 和 1 之間
    #
    b, a = ss.butter(order, Wn, 'lowpass')  #scipy 的 butterworth 低通濾波器 
    eq_data[f"{component}_filtered"] = ss.filtfilt(b, a, eq_data[component])
    # eq_data["NS_filtered"] = ss.filtfilt(b, a, eq_data["NS"])
    # eq_data["EW_filtered"] = ss.filtfilt(b, a, eq_data["EW"])

    #===========進行高通濾波============

    hb_cutoff_freq=filter_value[f"{component} bandpass_boundary (Hz)"]  #(Hz)截至頻率
    Wn=2*hb_cutoff_freq/sample_rate #Wn 是正規化的截止頻率，介於 0 和 1 之間
    b, a = ss.butter(order, Wn, 'highpass')  #scipy 的 butterworth 高通濾波器 
    eq_data[f"{component}_filtered"] = ss.filtfilt(b, a, eq_data[f"{component}_filtered"])


    Sd=Sd_calculate(w,damp_ratio,eq_data,component,filtered=True)
    Sv=Sd*w #pseudo velocity
    ax.plot(T,Sv,color="orange")
    ax.axvline(1/lb_cutoff_freq,linestyle="--",color="red")
    ax.set_title(f"{Sta_name} pseudo velocity respond spectrum ({component}) \n \
                    Bandpass between {hb_cutoff_freq} (Hz) and {lb_cutoff_freq} (Hz) \n \
                    Usable Period Range: {filter_value[f'{component} usable_period (sec)']} (sec) and {1/lb_cutoff_freq} (sec)" )
    # fig.savefig(f"{path}/pseudo velocity respond spectrum ({component}).png",dpi=300)

    #============plot filtered waveform=============
    fig, ax=plt.subplots(figsize=(7,7))
    ax.plot(eq_data["Time"],eq_data[f"{component}_filtered"])
    ax.set_title(f"Bandpass between {hb_cutoff_freq} (Hz) and {lb_cutoff_freq} (Hz) waveform ({component})")
    ax.set_xlabel("time (sec)")
    ax.set_ylabel("gal")
    # fig.savefig(f"{path}/filtered waveform ({component}).png",dpi=300)

    #=============pseudo acc================
    Sa=Sv*w 
    fig, ax=plt.subplots(figsize=(7,7))
    ax.plot(T,Sa)
    ax.set_xlabel("Period (sec)")
    ax.set_ylabel("Sa (gal)")
    ax.set_title(f"Station: {Sta_name} \n Acceleration Responce Spectrum ({component})")
    # fig.savefig(f"{path}/Acceleration Responce Spectrum ({component}).png",dpi=300)

    #==========write_information into dataframe==========
    pseudo_table["Period (sec)"]=T
    pseudo_table[f"{component}_PSV (cm/sec)"]=Sv
    pseudo_table[f"{component}_PSA (gal)"]=Sa

# pseudo_table.to_csv(f"{path}/period_data.csv",index=False)


# plot Sa
data=pd.read_csv("./result/HWA019/period_data.csv")

fig,ax=plt.subplots(figsize=(7,7))

ax.plot(data["Period (sec)"],data["Vertical_PSA (gal)"]/980,label="Vertical")
ax.plot(data["Period (sec)"],data["NS_PSA (gal)"]/980,label="NS")
ax.plot(data["Period (sec)"],data["EW_PSA (gal)"]/980,label="EW")
ax.set_xlim(0,5)
ax.set_ylim(0,1.8)
ax.set_ylabel("Sa (g)")
ax.set_xlabel("Period (sec)")
ax.set_title("HWA019 Acceleration Responce Spectrum")
ax.legend()
# fig.savefig("HWA019 Acceleration Responce Spectrum.png",dpi=300)
