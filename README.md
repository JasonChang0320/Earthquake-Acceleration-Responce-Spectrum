# Earthquake-Acceleration-Responce-Spectrum

Using **single degree of freedom system** to analyze the influence of strong earthquake waveform to building, and also use **high-pass and low-pass filter** to preprocess our data, and calculate three component waveforms **PSD (Maximum Relative Pseudo-Displacement), PSV (Maximum Relative Pseudo-Velocity), PSA (MaximumAbsolute Pseudo- Acceleration).**

## File descriptipon

**pseudo_spectrum.py** is the main code, including all preprocess and caculation

**HWA019 Acceleration Responce Spectrum.png** one of examples which is 2018 0206 Hualian earthquake record from station HWA019. The image show the three component PSA

## High-pass and low-pass filter

Using Tkinter to build a GUI to determine the high pass filter of cut-off frequency. As for low-pass frequency we set is 10Hz, the parameter we set is below:

```bash
pip install -r requirements.txt
```

## PSD, PSV, PSA caculation

## Example for 2018 0206 Hualian earthquake, station: HWA019

![image](https://github.com/JasonChang0320/Earthquake-Acceleration-Responce-Spectrum/blob/main/HWA019%20Acceleration%20Responce%20Spectrum.png)
