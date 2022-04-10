from binparse import BinRead
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, peak_widths, peak_prominences
import pickle

# 参数: 卷积: 4, 阶段高度: (0.75, 0.25), hist bin: 15

file = 'data/wave_record_0'

# yAll = BinRead(file+'.bin')
with open(file+'.bin.pickle', 'rb') as pf:
    yAll = pickle.load(pf)
    
sample = len(yAll[0])
x = np.arange(sample)
peakList, propertyList = [],[]

for i in range(len(yAll)):
    row, column = np.ceil(len(yAll)/2), 2

    y = np.array(yAll[i])
    
    # statistics
    ymin, ymax, ymed = np.min(y), np.max(y), np.median(y)

    # hist 
    yhist, bins = np.histogram(y, bins=np.arange(ymin, ymax, 15))
    yhmax = np.argmax(yhist)
    yzero = (bins[yhmax] + bins[yhmax+1])/2
    yzho = 0.75*yzero + 0.25*ymax
    
    # del negative points, translation downward
    y[y<yzero] = yzero
    y = y-yzero
    ymin, ymax, ymed, yzho = ymin-yzero, ymax-yzero, ymed-yzero, yzho-yzero

    # filter
    y_fil = np.convolve(y, np.ones((4,))/4, mode='same')
    y_filmax, y_filmed = np.max(y_fil), np.median(y_fil)
    y_filzho = 0.25*y_filmax
    peaks, properties = find_peaks(y_fil, height=y_filzho, width=3, prominence=y_filzho-y_filmed)
    # get original peak height
    peakcount = len(peaks)
    peaks = []
    if peakcount>=3: # remove the first and the last peak
        y_copy = np.copy(y)
        pl, pr = np.floor(properties['left_ips']), np.ceil(properties['right_ips'])
        for pi in range(1, peakcount-1):
            pk = np.argmax(y_copy[int(pl[pi]) : int(pr[pi])])
            peaks.append(pk + int(pl[pi]))
        # regenerate peak properity
        properties['prominences'], properties['left_bases'], properties['right_bases'] = peak_prominences(y_copy, peaks)
        properties['widths'], properties['width_heights'], properties['left_ips'], properties['right_ips'] = peak_widths(y_copy, peaks)
        # data
        peakList.append((np.array(peaks), y[peaks]))
        propertyList.append(properties)
    else:
        print ('ignore', i)

    # filtered plot
    # plt.subplot(int(row*100+column*10+i+1))
    if i==15:
        plt.plot(y)
        plt.plot(peaks, y[peaks], 'x')
        plt.vlines(x=peaks, ymin=y[peaks]-properties['prominences'], ymax=y[peaks], color='C1')
        plt.hlines(y=properties['width_heights'], xmin=properties['left_ips'], xmax=properties['right_ips'], color='C1')
        plt.hlines(y=y_filzho, xmin=x[0], xmax=x[-1], color='black')

    # unfiltered find_peaks
    # peaks, properties = find_peaks(y, height=yzho, width=3, prominence=yzho-ymed)

    # unfiltered plot
    # plt.subplot(int(row*100+column*10+i+1))
    # plt.plot(y)
    # plt.plot(peaks, y[peaks], 'x')
    # plt.vlines(x=peaks, ymin=y[peaks]-properties['prominences'], ymax=y[peaks],
    #            color='C1')
    # plt.hlines(y=properties['width_heights'], xmin=properties['left_ips'], xmax=properties['right_ips'],
    #            color='C1')
    # # plt.hlines(y=yzero, xmin=0, xmax=x[-1], color='black')
    # plt.hlines(y=yzho, xmin=0, xmax=x[-1], color='black')


    # hist
    # plt.subplot(int(row*100+column*10+i+1))
    # plt.hist(y, bins=np.arange(ymin, ymax, 15))

    # filter contrast
    # plt.subplot(int(row*100+column*10+i+1))
    # plt.plot(y, '-')
    # plt.plot(y_fil, '-')

    # update


# save
with open(file+'.peak.pickle', 'wb') as pf:
    pickle.dump(peakList, pf)
with open(file+'.property.pickle', 'wb') as pf:
    pickle.dump(propertyList, pf)

# show
plt.show()
