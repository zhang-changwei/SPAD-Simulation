import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def bi(x, u):
    return u*np.exp(-u*x)
rng = np.random.default_rng()
y = rng.exponential(20, size=1000)

def func(x, k, b, c):
    return x*(b-k*x) + c

def func2(x, a, b):
    return a*x*np.exp(-b*x)

phist, bins = np.histogram(y, bins=np.logspace(np.log10(np.min(y)), np.log10(np.max(y)), num=100, base=10))
x = (bins[:-1] + bins[1:])/2
opt, cov = curve_fit(func2, x, phist)
print (opt)
y2 = func2(x, *opt)


plt.hist(y, bins=np.logspace(np.log10(np.min(y)), np.log10(np.max(y)), num=100, base=10))
plt.plot(x, y2)
plt.xscale('log')
plt.yscale('log')
plt.show()

