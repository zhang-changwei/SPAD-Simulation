import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle
from scipy.optimize import curve_fit
from scipy.integrate import quad
from pool import poisson
from export import save

# interval histogram plot

peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('../feature/*.peak.pickle'), glob.glob('../feature/*.property.pickle')):
    with open(pk, 'rb') as pf:
        tmp = pickle.load(pf)
        peakList += tmp
    with open(pt, 'rb') as pf:
        tmp = pickle.load(pf)
        propertyList += tmp
    
intervals = np.array([])

# pk[0]: (list) x, pk[1]: (list) y
for pk, pt in zip(peakList, propertyList):
    if len(pk[0]) >= 2: # at least 2 peaks
        intervals = np.hstack((intervals, pk[0][1:] - pk[0][:-1]))

pmax, pmin, pmean, psum = np.max(intervals), np.min(intervals), np.mean(intervals), np.sum(intervals)

def func(x, a, b):
    return a*np.exp(-x/b)

# phist, bins = np.histogram(intervals, bins=np.linspace(pmin, pmax, num=40))
# x = (bins[:-1] + bins[1:])/2
# save(np.vstack((x, phist)))
# opt, cov = curve_fit(func, x[9:], phist[9:])
x = np.linspace(100, 360, 50)
y = func(x, 589.7, 54.6)

# plt.hist(intervals, bins=np.logspace(np.log10(10), np.log10(pmax), num=30, base=10))
plt.hist(intervals*0.2, bins=np.linspace(pmin*0.2, pmax*0.2, num=40), histtype='step')
plt.plot(x*0.2, y)

plt.hlines(95, 5, 20, ls='dashed', color='C1')
plt.vlines(5, 0, 95, ls='dashed', color='C1')
plt.yscale('log')
# plt.xscale('log')
plt.xlabel(r'interval / $\mathrm{\mu s}$')
plt.ylabel('count')
plt.show()