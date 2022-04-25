import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle

# peak height, peak width correlation scatter plot

peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('../feature/*.peak.pickle'), glob.glob('../feature/*.property.pickle')):
    with open(pk, 'rb') as pf:
        tmp = pickle.load(pf)
        peakList += tmp
    with open(pt, 'rb') as pf:
        tmp = pickle.load(pf)
        propertyList += tmp
    
# pk[0]: (list) x, pk[1]: (list) y
widthList = np.array([])
for pk, pt in zip(peakList, propertyList):
    pkheight = pt['prominences']
    pkwidth  = pt['widths']
    widthList = np.hstack((widthList, pkwidth))
    # plt.scatter(pkwidth, pkheight, marker='.', color='C0')
    
pmin, pmax = np.min(widthList), np.max(widthList)
plt.hist(widthList, bins=np.linspace(pmin, pmax, num=40), histtype='step')
plt.yscale('log')
plt.show()
# plt.xlabel('peak width / a.u.')
# plt.ylabel('peak height / a.u.')
# plt.show()