import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle
from scipy.optimize import curve_fit
from scipy.integrate import quad
from pool import poisson

# peak height histogram plot

peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('feature/*.peak.pickle'), glob.glob('feature/*.property.pickle')):
    with open(pk, 'rb') as pf:
        tmp = pickle.load(pf)
        peakList += tmp
    with open(pt, 'rb') as pf:
        tmp = pickle.load(pf)
        propertyList += tmp
    
pkheights = np.array([])

# pk[0]: (list) x, pk[1]: (list) y
for pk, pt in zip(peakList, propertyList):
    pkheights = np.hstack((pkheights, pt['prominences']))
    
pmax, pmin, pmean, psum = np.max(pkheights), np.min(pkheights), np.mean(pkheights), np.sum(pkheights)

# phist, bins = np.histogram(pkheights, bins=np.linspace(pmin, pmax, num=40), density=True)
# px = (bins[:-1] + bins[1:])/2
# print (phist, '\n', px)
# popt, pcov = curve_fit(poisson, px, phist)
# print (popt, pcov)
# print (pmin, pmax, pmean)
# phist, bins = np.histogram(pkheights, bins=np.logspace(np.log10(pmin), np.log10(pmax), num=40, base=10))
# print(phist)
# x = (bins[:-1] + bins[1:])/2
# y = bins[1:] - bins[:-1]
# for i in range(x.size):
#     y[i], err = quad(lambda xx: poisson(xx, pmean), bins[i], bins[i+1]) # / y[i]
# print(np.sum(y))

plt.hist(pkheights, bins=np.logspace(np.log10(pmin), np.log10(pmax), num=40, base=10)) #, density=True)
# plt.plot(x, phist/np.sum(phist))
# plt.plot(x, y)

plt.xscale('log')
plt.xlabel('peak height')
plt.ylabel('count')
plt.show()