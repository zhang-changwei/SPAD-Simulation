import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle

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
    
# pk[0]: (list) x, pk[1]: (list) y
for pk, pt in zip(peakList, propertyList):
    if len(pk[0]) >= 2: # at least 2 peaks
        interval = pk[0][1:] - pk[0][:-1]
        pkheight = pt['prominences'][1:]
        plt.scatter(interval, pkheight, marker='.', color='C0')
        dot = dot + len(interval)
    
print(dot)
# plt.xscale('log')
plt.xlabel('interval / a.u.')
plt.ylabel('peak height / a.u.')
plt.show()