from copy import deepcopy
from tkinter import W
from core import Quench, Recover
from matplotlib import pyplot as plt
import numpy as np
import math
from param import *

class Neighbor:
    '''Prev Next for Connection, Head Tail for Segment'''
    def __init__(self):
        self.th = 0
        self.tt = 0
        self.yh = None
        self.yt = None
        self.init = (None, None)

class SPAD:

    def __init__(self, parent=None):
        self._parent = parent

    def config(self, hd=False, save=False, plotcount=1, plotmode=['RSIt'], color='C0'):
        self.plotmode = plotmode
        self.color = color

        self.hdBool = hd
        self.saveBool = save
        self.plotBool = bool(plotcount)
        if self.plotBool and not hasattr(self, 'axes'):
            self.createPlot(plotcount)
        if self.saveBool:
            self.createSave()

    @property
    def parent(self):
        return self._parent

    def start(self, duration=0, simumode='Q'):
        self.prev = Neighbor()
        self.next = Neighbor()

        if simumode == 'Q' or simumode == 'QR':
            q = Quench()
            sol = q.quenchProcess(duration, self.hdBool)
            if sol.success:
                self.updatePlotQ(sol.t, sol.y)
        if simumode == 'QR' or simumode == 'R':
            self.prev = deepcopy(self.next)
            r = Recover(q=self.prev.init[0], i=self.prev.init[1])
            sol = r.recoverProcess(duration, self.hdBool)
            if sol.success:
                self.updatePlotR(sol.t, sol.y, start=self.prev.tt)
                if simumode == 'QR':
                    self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)), plot=True)

        if simumode == 'T' and duration:
            switchOnTSLists = self.switchOnEvent(duration)

            startTSList = next(switchOnTSLists)
            self.updatePlotFirst(t=startTSList[0])
            for ts, dur in zip(startTSList[:-1], startTSList[1:]-startTSList[:-1]):
                # q
                self.prev = deepcopy(self.next)
                q = Quench(i=self.prev.init[0], didt=self.prev.init[1])
                sol = q.quenchProcess(dur, self.hdBool)
                if sol.success:
                    self.updatePlotQ(sol.t, sol.y, start=ts)
                    self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
                else:
                    return
                # r
                self.prev = deepcopy(self.next)
                r = Recover(q=self.prev.init[0], i=self.prev.init[1])
                sol = r.recoverProcess(dur+ts-self.prev.tt, self.hdBool)
                if sol.success:
                    self.updatePlotR(sol.t, sol.y, start=self.prev.tt)
                    self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
                else:
                    return
            lastTS = startTSList[-1]

            for TSList in switchOnTSLists:
                flag = self.QR(lastTS, TSList[0]-lastTS)
                if not flag:
                    return
                for ts, dur in zip(TSList[:-1], TSList[1:]-TSList[:-1]):
                    flag = self.QR(ts, dur)
                    if not flag:
                        return
                lastTS = TSList[-1]

    def QR(self, ts, dur):
        # q
        self.prev = deepcopy(self.next)
        q = Quench(i=self.prev.init[0], didt=self.prev.init[1])
        sol = q.quenchProcess(dur, self.hdBool)
        if sol.success:
            self.updatePlotQ(sol.t, sol.y, start=ts)
            self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
        else:
            return
        # r
        self.prev = deepcopy(self.next)
        r = Recover(q=self.prev.init[0], i=self.prev.init[1])
        sol = r.recoverProcess(dur+ts-self.prev.tt, self.hdBool)
        if sol.success:
            self.updatePlotR(sol.t, sol.y, start=self.prev.tt)
            self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
        else:
            return
        return True

    def check(self):
        pass

    def switchOnEvent(self, dur):
        length = dur//P.Step
        ind = 0
        while length > 0:
            tsList = np.arange(min(P.Bin, length)) + ind*P.Bin
            rnd = rng.random(len(tsList))
            np.putmask(rnd, rnd<P.SwitchOnProb, False)
            np.putmask(rnd, rnd>=P.SwitchOnProb, True)
            switchOnTSList = np.ma.MaskedArray(tsList, mask=rnd, copy=False).compressed()
            yield switchOnTSList * P.Step
            length -= P.Bin
            ind += 1

    def updatePlotQ(self, t, y, start=0):
        headY = []
        tailY = []
        for pm, ax in zip(self.plotmode, self.axes):
            if pm == 'RSIt':
                sig = y[0] + P.Rd*P.Cd*y[1]
            elif pm == 'SPADVt':
                sig = P.Rd*y[0] + P.Vb
            elif pm == 'SPADIt':
                sig = y[0]
            headY.append(sig[0])
            tailY.append(sig[-1])
            ax.plot(t + start, sig, marker='', color=self.color)
        self.next.th = t[0] + start
        self.next.tt = t[-1] + start
        self.next.yh = np.array(headY).reshape((-1, 1))
        self.next.yt = np.array(tailY).reshape((-1, 1))
        self.next.init = ((P.Vb + P.Rd*y[0, -1])*P.Cd, 
                          y[0, -1] + P.Rd*P.Cd*y[1, -1])
        self.parent.curve.canvas.draw()
        self.parent.curve.canvas._tkcanvas.update()

    def updatePlotR(self, t, y, start=0):
        headY = []
        tailY = []
        for pm, ax in zip(self.plotmode, self.axes):
            if pm == 'RSIt':
                sig = y[1]
            elif pm == 'SPADVt':
                sig = y[0]/P.Cd
            elif pm == 'SPADIt':
                sig = np.zeros_like(t)
            headY.append(sig[0])
            tailY.append(sig[-1])
            ax.plot(t + start, sig, marker='', color=self.color)
        self.next.th = t[0] + start
        self.next.tt = t[-1] + start
        self.next.yh = np.array(headY).reshape((-1, 1))
        self.next.yt = np.array(tailY).reshape((-1, 1))
        self.next.init = ((y[0, -1]/P.Cd - P.Vb)/P.Rd, 
                          -(y[0, -1]/P.Cd - P.Vb)/(P.Rd*P.Rd*P.Cd))
        self.parent.curve.canvas.draw()
        self.parent.root.update()

    def updatePlotConnection(self, t, y, plot=False):
        for i, ax in enumerate(self.axes):
            ax.plot(t, y[i], marker='', color=self.color)
        if plot:
            self.parent.curve.canvas.draw()

    def updatePlotFirst(self, t=0):
        headY = []
        tailY = []
        for pm, ax in zip(self.plotmode, self.axes):
            if pm == 'RSIt':
                sig = 0
            elif pm == 'SPADVt':
                sig = P.Va
            elif pm == 'SPADIt':
                sig = 0
            headY.append(sig)
            tailY.append(sig)
        self.next.th = t
        self.next.tt = t
        self.next.yh = np.array(headY).reshape((-1, 1))
        self.next.yt = np.array(tailY).reshape((-1, 1))


    def fplot(self, x, y, xtol, ytol):
        pass

    def createPlot(self, count):
        TITLE = {'RSIt': 'RS I-t', 'SPADVt': 'SPAD V-t', 'SPADIt': 'SPAD I-t', 'DCIV': 'DC I-V'}
        if count == 1:
            self.axes = [self.parent.curve.figure.add_subplot(111)]
        else:
            self.axes = self.parent.curve.figure.subplots(math.ceil(count/2), 2).flatten()[:count]
        for pm, ax in zip(self.plotmode, self.axes):
            ax.set_title(TITLE[pm])

    def createSave(self):
        with open('data/test.csv', 'w', buffering=1) as self.file:
            pass
