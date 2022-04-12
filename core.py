from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from param import *
from timeit import default_timer as timer
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class Result:
    def __init__(self, success=True, t=None, y=None):
        self.success = success
        self.t = t
        self.y = y

class Quench:

    def __init__(self, i=None, didt=None, iq=P.IQCenter):
        if not i:
            i = (P.Va-P.Vb)/P.Rd
        if not didt:
            didt = -(P.Va-P.Vb)/(P.Rd*P.Rd*P.Cd)
        self.init = [i, didt]
        self.iq = iq

    def quenchEq(self, t, y):
        '''y[0] = i, y[1] = di/dt'''
        d2ydt = -P.Q.A*y[1] - P.Q.B*y[0] + P.Q.C
        return [y[1], d2ydt]

    def quenchProcess(self, dur=0, highresolution=False):
        dur = max(dur, P.Q.Tq * 5)
        if self.init[0] <= self.iq:
            return Result(True, t=np.array([0]), y=np.array(self.init).T)
        if highresolution:
            t_eval = np.arange(0, dur, P.Step)
        else:
            t_eval = None
        sol = solve_ivp(self.quenchEq, t_span=(0, dur), y0=self.init, t_eval=t_eval)
        if sol.success:
            masked = np.ma.masked_less_equal(sol.y[0], self.iq, copy=False)
            y0 = np.copy(masked.compressed())
            y1 = np.copy(sol.y[1, :len(y0)])
            t0 = np.copy(sol.t[:len(y0)])
            sol.t = t0
            sol.y = np.array([y0, y1])
            return sol
        else:
            logger.warning(f'[Recover Error] {sol.status} {sol.message}')


class Recover:

    def __init__(self, q=None, i=None):
        if not q:
            q = (P.Vb + P.Rd*P.IQCenter)*P.Cd
        if not i:
            i = P.IQCenter
        self.init = [q, i]

    def recoverEq(self, t, y):
        '''y[0] = q, y[1] = i'''
        d2ydt = -P.R.A*y[1] - P.R.B*y[0] + P.R.C
        return [y[1], d2ydt]

    def recoverProcess(self, dur=0, highresolution=False):
        if not dur:
            dur = P.R.Tr * 5
        if highresolution:
            t_eval = np.arange(0, dur, P.Step)
        else:
            t_eval = None
        sol = solve_ivp(self.recoverEq, t_span=(0, dur), y0=self.init, t_eval=t_eval)
        if sol.success:
            return sol
        else:
            logger.warning(f'[Recover Error] {sol.status} {sol.message}')

# if __name__ == '__main__':
#     ti = timer()
#     qq = Quench()
#     sol = qq.quenchProcess()
#     print(len(sol.t), sol.t[1:]-sol.t[:-1])
#     tf = timer()
#     print(tf-ti)
#     plt.plot(sol.t, sol.y[0])
#     plt.plot(sol.t, sol.y[0] + P.Cd*P.Rd*sol.y[1])
#     plt.hlines(100e-6, sol.t[0], sol.t[-1])
#     plt.show()
if __name__ == '__main__':
    ti = timer()
    qq = Recover()
    sol = qq.recoverProcess()
    tf = timer()
    print(tf-ti, sol.message)
    # plt.plot(sol.t, sol.y[0]/P.Cd)
    plt.plot(sol.t, sol.y[1])
    # plt.ylim(P.Vb, P.Va)
    # plt.plot(sol.t, sol.y[0] + P.Cd*P.Rd*sol.y[1])
    # plt.hlines(100e-6, sol.t[0], sol.t[-1])
    plt.show()