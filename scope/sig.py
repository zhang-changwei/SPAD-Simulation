import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter, find_peaks

y = np.load('data/data.npy')
# y = savgol_filter(y, 5, 2)

# peaks5, _ = find_peaks(y, height=1000, width=5, prominence=400) # mostly width & prominence
# plt.subplot(1, 1, 1) # row, column, num
# plt.plot(peaks5, y[peaks5],"xk"); plt.plot(y); plt.legend(['all'])
# plt.show()

xfour = np.fft.fft(y)
xfreq = np.fft.fftfreq(y.size)

xfour[0] = 0

xfour = np.fft.fftshift(xfour)
xfreq = np.fft.fftshift(xfreq)

xn = np.sqrt(xfour.real**2+xfour.imag**2)
# xinvf = np.fft.ifft(xfour)

# plt.plot(xfreq, xn, '.')
plt.plot(xfreq, xn)
plt.show()