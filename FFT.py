import matplotlib.pyplot as plt
import numpy as np
import serial
import time

Fs = 1000.0  # sampling rate
Ts = 1.0/Fs  # sampling interval
# time vector; create Fs samples between 0 and 1.0 sec.
t = np.arange(0, 1, Ts)
n = len(t)  # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T  # a vector of frequencies; two sides frequency range
frq = frq[range(int(n/2))]  # one side frequency range

serdev = '/COM6'
s = serial.Serial(serdev)
print("OK")
while (1):
    line = s.readline()
    print(line)
    if (line == b'Start\r\n'):
        break


print("Get original signal")
y = np.arange(0, 1, Ts)  # signal vector; create Fs samples
for x in range(0, int(Fs)):
    line = s.readline()  # Read an echo string from B_L4S5I_IOT01A terminated with '\n'
    # print line
    y[x] = float(line)


print("Get low pass signal")
yAfterRC = np.arange(0, 1, Ts)
for x in range(0, int(Fs)):
    # print(x)
    line = s.readline()  # Read an echo string from B_L4S5I_IOT01A terminated with '\n'
    # print line
    yAfterRC[x] = float(line)


print("Stimulate low pass signal")
yAfterFormula = np.arange(0, 1, Ts)
NthOrder = 100
tmpSum = 0.4 * NthOrder
for x in range(0, int(Fs)):
    if x < NthOrder:
        yAfterFormula[x] = (tmpSum + y[x] - 0.5) / NthOrder
        tmpSum += y[x] - 0.5
    else:
        yAfterFormula[x] = (tmpSum + y[x] - y[x-NthOrder]) / NthOrder
        tmpSum += y[x] - y[x-NthOrder]

print("FFT")
Y = np.fft.fft(y)/n*2  # fft computing and normalization
Y = Y[range(int(n/2))]  # remove the conjugate frequency parts

YAfterRC = np.fft.fft(yAfterRC)/n*2  # fft computing and normalization
YAfterRC = YAfterRC[range(int(n/2))]  # remove the conjugate frequency parts

YAfterFormula = np.fft.fft(yAfterFormula) / n * 2
YAfterFormula = YAfterFormula[range(int(n/2))]

#############################################
plt.figure(0)
fig, ax = plt.subplots(2, 1, constrained_layout=True)
ax[0].plot(t, y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(Y), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.suptitle("Before RC")

# inset axes....
axins = ax[1].inset_axes([0.5, 0.2, 0.47, 0.77])
axins.plot(frq, abs(Y), 'r')
# sub region of the original image
x1, x2, y1, y2 = -5, 30, -0.1, 1.1
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax[1].indicate_inset_zoom(axins, edgecolor="black")
#############################################
plt.figure(1)
fig, ax = plt.subplots(2, 1, constrained_layout=True)
ax[0].plot(t, yAfterRC)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(YAfterRC), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.suptitle("After RC")

# inset axes....
axins = ax[1].inset_axes([0.5, 0.2, 0.47, 0.77])
axins.plot(frq, abs(YAfterRC), 'r')
# sub region of the original image
x1, x2, y1, y2 = -5, 30, -0.1, 1.1
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax[1].indicate_inset_zoom(axins, edgecolor="black")
#############################################
plt.figure(2)
fig, ax = plt.subplots(2, 1, constrained_layout=True)
ax[0].plot(t, yAfterFormula)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(YAfterFormula), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.suptitle("After Formula")

# inset axes....
axins = ax[1].inset_axes([0.5, 0.2, 0.47, 0.77])
axins.plot(frq, abs(YAfterFormula), 'r')
# sub region of the original image
x1, x2, y1, y2 = -5, 30, -0.1, 1.1
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax[1].indicate_inset_zoom(axins, edgecolor="black")

plt.show()
s.close()
