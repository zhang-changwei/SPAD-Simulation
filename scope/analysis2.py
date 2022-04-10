import numpy as np
from matplotlib import pyplot as plt
import glob
import pickle
from scipy.optimize import curve_fit
from scipy.integrate import quad
from pool import poisson

# interval histogram plot

peakList, propertyList = [],[]
for pk, pt in zip(glob.glob('feature/*.peak.pickle'), glob.glob('feature/*.property.pickle')):
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
    return a*(x)*np.exp(-b*(x))

phist, bins = np.histogram(intervals, bins=np.logspace(np.log10(10), np.log10(pmax), num=30, base=10))
x = (bins[:-1] + bins[1:])/2
# for i in x: print (i)
# for i in phist: print(i)
opt, cov = curve_fit(func, x, phist, p0=(1.95, 0.0095))
y = func(x, *opt)

# plt.hist(intervals, bins=np.logspace(np.log10(10), np.log10(pmax), num=30, base=10))
plt.hist(intervals, bins=np.linspace(pmin, pmax, num=40))
plt.plot(x, y)

plt.yscale('log')
# plt.xscale('log')
plt.xlabel('interval')
plt.ylabel('count')
plt.show()