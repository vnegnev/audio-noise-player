#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pyaudio as pa
import sys

samplerate = 44100
seconds = 5
loops = 10000
volume = 2

p = pa.PyAudio()

stream = p.open(samplerate, 1, pa.paFloat32, output=True)

if False:
    t = np.linspace(0, seconds, samplerate * seconds + 1)
    y = volume * np.sin(2*np.pi*440*t)

data_list = []

for k in range(100):
    y = volume * np.random.random(samplerate * seconds + 1)
    y -= y.mean()
    f_axis = np.linspace(1, 200, (samplerate * seconds)//2 + 1)
    scaling = 1 / f_axis

    yf = np.fft.rfft(y)
    yf_scaled = yf * scaling
    y_spect = np.fft.irfft(yf_scaled)

    # plt.plot(yf_scaled);plt.show()

    y_raw = y_spect.astype(np.float32)

    data_list.append(y_raw)

for k in data_list:
    stream.write(k)
