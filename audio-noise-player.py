#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pyaudio as pa
import sys
import time

samplerate = 44100
seconds = 30
frame_len = 100000
volume = 2

samples = samplerate * seconds + 1

p = pa.PyAudio()

if False:
    t = np.linspace(0, seconds, samples)
    y = volume * np.sin(2*np.pi*440*t)


y = volume * np.random.random(samples)
y -= y.mean()
f_axis = np.linspace(1, 200, (samplerate * seconds)//2 + 1)
scaling = 1 / f_axis

yf = np.fft.rfft(y)
yf_scaled = yf * scaling
y_spect = np.fft.irfft(yf_scaled)

# plt.plot(yf_scaled);plt.show()

y_raw = y_spect.astype(np.float32)

a = 0

def callback(in_data, frame_count, time_info, status):
    global a
    sdata = y_raw[a: a + frame_len*frame_count]
    a = np.mod(a + frame_len, samples)
    return sdata, pa.paContinue

stream = p.open(samplerate, 1, pa.paFloat32, output=True, stream_callback=callback)

stream.start_stream()

while True:
    time.sleep(0.1)

stream.stop_stream()
stream.close()
pa.terminate()
