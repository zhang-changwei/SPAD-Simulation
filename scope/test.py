import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def bi(x, u):
    return u*np.exp(-u*x)
rng = np.random.default_rng()
y = rng.exponential(20, size=10000)

def func(x, a, b):
    return a*np.exp(-x/b)

def func2(x, a, b):
    return a*x*np.exp(-b*x)

# phist, bins = np.histogram(y, bins=np.logspace(np.log10(np.min(y)), np.log10(np.max(y)), num=100, base=10))
# x = (bins[:-1] + bins[1:])/2
# opt, cov = curve_fit(func2, x, phist)
# print (opt)
# y2 = func2(x, *opt)

phist, bins = np.histogram(y, bins=np.linspace(np.min(y), np.max(y), num=100))
x = (bins[:-1] + bins[1:])/2
opt, cov = curve_fit(func, x, phist)
print (opt)
y2 = func(x, *opt)

plt.hist(y, bins=np.linspace(np.min(y), np.max(y), num=100), histtype='step')
plt.plot(x, y2)
plt.xlabel('interval / a.u.')
plt.ylabel('count')
# plt.xscale('log')
plt.yscale('log')
plt.show()

