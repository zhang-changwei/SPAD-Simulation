import numpy as np
from numpy import log, pi, exp
from scipy.special import factorial, gamma

def poisson(x, lbda):
    # for large x
    a = x*np.log(lbda)
    b = x*log(x)+log(2*pi*x)/2-x
    c = -lbda
    return exp(a-b+c)

    # return lbda**x/gamma(x)*np.exp(-lbda)

def log10poisson(x, lbda):
    return x*np.log(10)*poisson(x, lbda)