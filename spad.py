from copy import deepcopy
from core import Quench, Recover
from matplotlib import pyplot as plt
import numpy as np
import math
from typing import Iterable, Optional
from param import *

class Neighbor:
    '''Prev Next for Connection, Head Tail for Segment'''
    def __init__(self):
        self.th = 0
        self.tt = 0
        self.yh = None
        self.yt = None
        self.init = (None, None)

class Data:

    def __init__(self, on:bool):
        self.on = on
        self._data = []
        self._time = []
        self.peakHeight = []
        self.peakWidth = []
        self.peakTS = []
        self._eventTS = []
        self.dcCurrent = []
        self.dcVoltage = []

    @property
    def data(self):
        return np.hstack(self._data)
    @property
    def time(self):
        return np.hstack(self._time)

    @property
    def peakCount(self):
        return len(self.peakTS)
    @property
    def eventCount(self):
        return len(self.eventTS) - 1
    @property
    def eventTS(self):
        return np.hstack(self._eventTS)

class SPAD:

    def __init__(self, parent=None):
        self._parent = parent
        self.axes = []

    def config(self, hd=False, savemode=[], plotmode=['RSIt'], color='C0', updatedata=True):
        self.plotmode = plotmode
        self.savemode = savemode
        self.color = color

        self.hdBool = hd
        self.saveBool = bool(savemode)
        self.plotBool = bool(plotmode)
        if self.plotBool and not self.axes:
            self.createPlot(len(plotmode))
            if len(self.axes) != len(plotmode):
                raise ValueError()
        if updatedata:
            self.data = Data(self.saveBool)

    @property
    def parent(self):
        return self._parent

    def start(self, duration=0, simumode='Q'):
        self.prev = Neighbor()
        self.next = Neighbor()

        if simumode == 'IV':
            self.updatePlotNaiveIV()

        if simumode == 'Q' or simumode == 'QR':
            self.updatePlotFirst(t=0)
            self.prev = deepcopy(self.next)
            q = Quench()
            sol = q.quenchProcess(duration, self.hdBool, ave=True)
            if sol.success:
                self.updatePlotQ(sol.t, sol.y)
                if self.plotBool:
                    self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)), show=True)
        if simumode == 'QR' or simumode == 'R':
            self.prev = deepcopy(self.next)
            r = Recover(q=self.prev.init[0], i=self.prev.init[1])
            sol = r.recoverProcess(duration, self.hdBool)
            if sol.success:
                self.updatePlotR(sol.t, sol.y, start=self.prev.tt)
                if simumode == 'QR' and self.plotBool:
                    self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)), show=True)

        if simumode == 'T' and duration:
            switchOnTSLists = self.switchOnEvent(duration)

            # startTSList = next(switchOnTSLists)
            self.updatePlotFirst(t=0) # startTSList[0]
            nowTS, nextProcess = 0, 'Quench'
            for TSList in switchOnTSLists:
                for ts, dur in zip(TSList[:-1], TSList[1:]-TSList[:-1]):
                    # first check whether to enter q
                    if ts + dur < nowTS:
                        continue
                    elif nextProcess == 'Quench':
                        # q
                        self.prev = deepcopy(self.next)
                        q = Quench(i=self.prev.init[0], didt=self.prev.init[1])
                        sol = q.quenchProcess(dur, self.hdBool)
                        if not sol.success:
                            return
                        self.updatePlotQ(sol.t, sol.y, start=ts)
                        if self.plotBool:
                            self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
                        
                        nowTS, nextProcess = self.next.tt, 'Recover'
                        if ts + dur < nowTS:
                            continue # the light event strikes in the quench process
                    # r
                    self.prev = deepcopy(self.next)
                    r = Recover(q=self.prev.init[0], i=self.prev.init[1])
                    sol = r.recoverProcess(dur+ts-self.prev.tt, self.hdBool)
                    if not sol.success:
                        return
                    self.updatePlotR(sol.t, sol.y, start=self.prev.tt)
                    if self.plotBool:
                        self.updatePlotConnection((self.prev.tt, self.next.th), np.hstack((self.prev.yt, self.next.yh)))
                    nowTS, nextProcess = self.next.tt, 'Quench'

    def check(self):
        pass

    def switchOnEvent(self, dur:float):
        length = dur//P.Step
        ind = 0
        switchOnTSList = []
        while length > 0:
            tsList = np.arange(min(P.Bin, length)) + ind*P.Bin
            rnd = rng.random(len(tsList))
            np.putmask(rnd, rnd<P.SwitchOnProb, False)
            np.putmask(rnd, rnd>=P.SwitchOnProb, True)
            switchOnTSList.append(np.ma.MaskedArray(tsList, mask=rnd, copy=False).compressed())
            length -= P.Bin
            ind += 1
            if ind % int(1/P.SwitchOnProb) == 0:
                TSList = np.hstack(switchOnTSList) * P.Step
                if 'Summary' in self.savemode:
                    self.data._eventTS.append(TSList)
                yield TSList
                switchOnTSList = []
        TSList = np.hstack(switchOnTSList) * P.Step
        if 'Summary' in self.savemode:
            self.data._eventTS.append(TSList)
        yield TSList

    def updatePlotQ(self, t:Iterable, y:Iterable, start:float=0):
        self.next.th = t[0] + start
        self.next.tt = t[-1] + start
        self.next.init = ((P.Vb + P.Rd*y[0, -1])*P.Cd, 
                          y[0, -1] + P.Rd*P.Cd*y[1, -1])
        if self.plotBool:
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
            self.next.yh = np.array(headY).reshape((-1, 1))
            self.next.yt = np.array(tailY).reshape((-1, 1))
            self.parent.curve.canvas.draw()
            self.parent.curve.canvas._tkcanvas.update()
        if self.saveBool:
            if 'Raw' in self.savemode:
                self.data._time.append(t + start)
                self.data._data.append(y[0] + P.Rd*P.Cd*y[1])
            if 'Summary' in self.savemode:
                self.data.peakTS.append(t[np.argmax(y[0] + P.Rd*P.Cd*y[1])] + start)
                self.data.peakHeight.append(np.max(y[0] + P.Rd*P.Cd*y[1]))
                self.data.peakWidth.append(t[-1])

    def updatePlotR(self, t:Iterable, y:Iterable, start:float=0):
        self.next.th = t[0] + start
        self.next.tt = t[-1] + start
        self.next.init = ((y[0, -1]/P.Cd - P.Vb)/P.Rd, 
                          (P.Rd*y[1, -1] - y[0, -1]/P.Cd + P.Vb)/(P.Rd*P.Rd*P.Cd))
        if self.plotBool:
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
            self.next.yh = np.array(headY).reshape((-1, 1))
            self.next.yt = np.array(tailY).reshape((-1, 1))
            self.parent.curve.canvas.draw()
            self.parent.curve.canvas._tkcanvas.update()
        if self.saveBool:
            if 'Raw' in self.savemode:
                self.data._time.append(t + start)
                self.data._data.append(y[1])

    def updatePlotNaiveIV(self):
        vMax = 200e-6 * P.Rd + P.Vb
        vList = np.arange(P.Vb, vMax, 0.001)
        iList = [0]
        for v in vList[1:]:
            iFin = (v - P.Vb)/(P.Rd)
            p10 = P.P10(iFin)
            if p10 > (P.LCR + P.DCR):
                iList.append((P.LCR + P.DCR)/p10 * iFin)
            else:
                iList.append(iFin)
        if self.plotBool:
            self.axes[0].plot(vList, iList, marker='', color=self.color)
            self.updatePlotConnection([0, P.Vb], [[0, 0]], show=True)
        if self.saveBool:
            self.data.dcCurrent = iList
            self.data.dcVoltage = vList

    def updatePlotConnection(self, t:Iterable, y:Iterable, show:Optional[bool]=False):
        for i, ax in enumerate(self.axes):
            ax.plot(t, y[i], marker='', color=self.color)
        if show:
            self.parent.curve.canvas.draw()

    def updatePlotFirst(self, t:float=0):
        self.next.th = t
        self.next.tt = t
        if self.plotBool:
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
            self.next.yh = np.array(headY).reshape((-1, 1))
            self.next.yt = np.array(tailY).reshape((-1, 1))


    def fplot(self, x, y, xtol, ytol):
        pass

    def createPlot(self, count:int):
        TITLE = {'RSIt': '$R_S \\quad I-t$', 'SPADVt': 'SPAD  $V-t$', 'SPADIt': 'SPAD  $I-t$', 'DCIV': 'DC  $I-V$', 'External': ''}
        if count == 1:
            self.axes = [self.parent.curve.figure.add_subplot(111)]
        else:
            self.axes = self.parent.curve.figure.subplots(math.ceil(count/2), 2).flatten()[:count]
        for pm, ax in zip(self.plotmode, self.axes):
            ax.set_title(TITLE[pm])
            
