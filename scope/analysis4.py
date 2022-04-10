import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle

# peak height, peak width correlation scatter plot

peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('feature/*.peak.pickle'), glob.glob('feature/*.property.pickle')):
    with open(pk, 'rb') as pf:
        tmp = pickle.load(pf)
        peakList += tmp
    with open(pt, 'rb') as pf:
        tmp = pickle.load(pf)
        propertyList += tmp
    
# pk[0]: (list) x, pk[1]: (list) y
for pk, pt in zip(peakList, propertyList):
    pkheight = pt['prominences']
    pkwidth  = pt['widths']
    plt.scatter(pkwidth, pkheight, marker='.', color='C1')
    
plt.xlabel('peak width')
plt.ylabel('peak height')
plt.show()