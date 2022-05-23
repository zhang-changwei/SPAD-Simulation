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

    def __init__(self, i=None, didt=None):
        if not i:
            i = (P.Va-P.Vb)/P.Rd
        if not didt:
            didt = -(P.Va-P.Vb)/(P.Rd*P.Rd*P.Cd)
        self.init = [i, didt]

    def quenchEq(self, t, y):
        '''y[0] = i, y[1] = di/dt'''
        d2ydt = -P.Q.A*y[1] - P.Q.B*y[0] + P.Q.C
        return [y[1], d2ydt]

    def quenchProcess(self, dur=0, highresolution=True, ave=False):
        rand = rng.random()
        # first point
        if ave == False and rand <= P.P10(self.init[0])*P.Step:
            return Result(True, t=np.array([0]), y=np.array(self.init).reshape(-1, 1))

        # print(P.Tau1(P.If), P.Q.Tq)
        duration = (P.Tau1(P.If) + P.Q.Tq) * 5
        if highresolution:
            t_eval = np.arange(0, duration, P.Step)
        else:
            t_eval = None
        sol = solve_ivp(self.quenchEq, t_span=(0, duration), y0=self.init, t_eval=t_eval)
        if sol.success:
            if ave:
                probList = P.P10(sol.y[0, 1:]) * (sol.t[1:] - sol.t[:-1])
                probLeftList = np.cumprod(1 - probList)
                probList[1:] *= probLeftList[: -1]
                probLeft = probLeftList[-1]
                tauAve = np.sum(probList * sol.t[1:]) + probLeft * (P.Tau1(sol.y[0, -1]) + sol.t[-1])
                if tauAve <= sol.t[-1]:
                    sol.t = sol.t[sol.t <= tauAve]
                    sol.y = sol.y[:, :(sol.t.size)]
                else:
                    sol.t = np.append(sol.t, tauAve)
                    sol.y = np.hstack((sol.y, [[sol.y[0, -1]], [sol.y[1, -1]]]))
            else:
                # probLeft = 1
                for ts, d, i in zip(sol.t[1:], sol.t[1:] - sol.t[:-1], sol.y[0, 1:]):
                    rand = rng.random()
                    prob = P.P10(i) * d
                    if rand <= prob: # probLeft * prob:
                        sol.t = sol.t[sol.t <= ts]
                        sol.y = sol.y[:, :(sol.t.size)]
                        break
                    # probLeft = probLeft * (1 - prob)
                else:
                    rand = rng.exponential(P.Tau1(sol.y[0, -1])) + sol.t[-1]
                    sol.t = np.append(sol.t, rand)
                    sol.y = np.hstack((sol.y, [[sol.y[0, -1]], [sol.y[1, -1]]])) # how to choose y[1]
            return sol
        else:
            logger.warning(f'[Quench Error] {sol.status} {sol.message}')


class Recover:

    def __init__(self, q=None, i=None):
        if not q:
            q = (P.Vb + P.Rd*P.If)*P.Cd
        if not i:
            i = P.If
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
        sol = solve_ivp(self.recoverEq, t_span=(0, dur), y0=self.init, t_eval=t_eval, atol=1e-8)
        if sol.success:
            return sol
        else:
            logger.warning(f'[Recover Error] {sol.status} {sol.message}')

if __name__ == '__main__':
    qq = Quench()
    sol = qq.quenchProcess(ave=True)
    print(sol.t, sol.y)
    plt.plot(sol.t, sol.y[0])
    plt.plot(sol.t, sol.y[0] + P.Cd*P.Rd*sol.y[1])
    # plt.hlines(100e-6, sol.t[0], sol.t[-1])
    plt.xlim(0, 1e-6)
    plt.show()
# if __name__ == '__main__':
#     ti = timer()
#     qq = Recover()
#     sol = qq.recoverProcess()
#     tf = timer()
#     print(tf-ti, sol.message)
    # plt.plot(sol.t, sol.y[0]/P.Cd)
    # plt.plot(sol.t, sol.y[1])
    # plt.ylim(P.Vb, P.Va)
    # plt.plot(sol.t, sol.y[0] + P.Cd*P.Rd*sol.y[1])
    # plt.hlines(100e-6, sol.t[0], sol.t[-1])
    # plt.show()