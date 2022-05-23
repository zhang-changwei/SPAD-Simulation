import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle

import pandas

# interval, peak height correlation scatter plot

dot = 0
peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('../feature/*.peak.pickle'), glob.glob('../feature/*.property.pickle')):
    with open(pk, 'rb') as pf:
        tmp = pickle.load(pf)
        peakList += tmp
    with open(pt, 'rb') as pf:
        tmp = pickle.load(pf)
        propertyList += tmp
    
datax = []
datay = []
# pk[0]: (list) x, pk[1]: (list) y
for pk, pt in zip(peakList, propertyList):
    if len(pk[0]) >= 2: # at least 2 peaks
        interval = pk[0][1:] - pk[0][:-1]
        pkheight = pt['prominences'][1:]
        plt.scatter(interval*0.2, pkheight, marker='.', color='C0')
        datax.extend(interval*0.2)
        datay.extend(pkheight)
        dot = dot + len(interval)
    
# data = np.vstack([[datax], [datay]])
# df = pandas.DataFrame(data.T, columns=['1', '2'])
# df.to_csv('analysis1.csv', index=False)
# print(dot)
# plt.xscale('log')
# x = np.linspace(4, 35, 100)
# y = 775-775*np.exp(-(x-3)/5)
# y1 = 775-775*np.exp(-(x-3)/6)
# y2 = 775-775*np.exp(-(x-3)/4)
# plt.plot(x, y, label='10', color='C7')
# plt.plot(x, y1, label='20', color='C8')
# plt.plot(x, y2, label='5', color='C9')
plt.xlabel(r'interval / $\mathrm{\mu s}$')
plt.ylabel('peak height / a.u.')
# plt.legend()
plt.show()