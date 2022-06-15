# Earthquake-Acceleration-Responce-Spectrum

Using **single degree of freedom system** to analyze the influence of strong earthquake waveform to building, and also use **high-pass and low-pass filter** to preprocess our data, and calculate three component waveforms **PSD (Maximum Relative Pseudo-Displacement), PSV (Maximum Relative Pseudo-Velocity), PSA (MaximumAbsolute Pseudo- Acceleration).**

## File descriptipon

**pseudo_spectrum.py** is the main code, including all preprocess and caculation

**HWA019 Acceleration Responce Spectrum.png** one of examples which is 2018 0206 Hualian earthquake record from station HWA019. The image show the three component PSA

## High-pass and low-pass filter

Using Tkinter to build a GUI to determine the high pass filter of cut-off frequency. As for low-pass frequency we set is 10Hz, the parameter we set is below:

```python
import scipy.signal as ss

#==========進行低通濾波=========
sample_rate=200 #取樣頻率 (Hz)
order=4 #4階
lb_cutoff_freq=10  #(Hz)截至頻率
Wn=2*lb_cutoff_freq/sample_rate #Wn 是正規化的截止頻率，介於 0 和 1 之間

b, a = ss.butter(order, Wn, 'lowpass')  #scipy 的 butterworth 低通濾波器 
eq_data[f"{component}_filtered"] = ss.filtfilt(b, a, eq_data[component])

#===========進行高通濾波============
hb_cutoff_freq=filter_value[f"{component} bandpass_boundary (Hz)"]  #(Hz)截至頻率
Wn=2*hb_cutoff_freq/sample_rate #Wn 是正規化的截止頻率，介於 0 和 1 之間
b, a = ss.butter(order, Wn, 'highpass')  #scipy 的 butterworth 高通濾波器 
eq_data[f"{component}_filtered"] = ss.filtfilt(b, a, eq_data[f"{component}_filtered"])
```

## PSD, PSV, PSA caculation

## Example for 2018 0206 Hualian earthquake, station: HWA019

![image](https://github.com/JasonChang0320/Earthquake-Acceleration-Responce-Spectrum/blob/main/HWA019%20Acceleration%20Responce%20Spectrum.png)
