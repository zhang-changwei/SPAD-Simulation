import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from param import *
from spad import SPAD

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('SPAD')
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        self.displayParam()
        self.displaySPAD()
        self.displaySample()
        self.displayCurve()

        self.root.mainloop()

    def displayParam(self):
        gridT = ttk.Labelframe(self.root, text='Eletronic Params')
        gridT.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky='ew')
        
        self.va = tk.DoubleVar(value=P.Va)
        self.vb = tk.DoubleVar(value=P.Vb)
        self.rd = tk.DoubleVar(value=P.Rd)
        self.rl = tk.DoubleVar(value=P.Rl)
        self.rs = tk.DoubleVar(value=P.Rs)
        self.cd = tk.DoubleVar(value=P.Cd)
        self.cas = tk.DoubleVar(value=P.Cas)
        self.ccs = tk.DoubleVar(value=P.Ccs)

        ttk.Label(gridT, text='VA (V)').grid(row=0, column=0, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.va).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(gridT, text='VB (V)').grid(row=1, column=0, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.vb).grid(row=1, column=1, padx=2, pady=2)
        ttk.Label(gridT, text='RD (ohm)').grid(row=2, column=0, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.rd).grid(row=2, column=1, padx=2, pady=2)
        ttk.Label(gridT, text='RL (ohm)').grid(row=3, column=0, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.rl).grid(row=3, column=1, padx=2, pady=2)
        ttk.Label(gridT, text='RS (ohm)').grid(row=4, column=0, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.rs).grid(row=4, column=1, padx=2, pady=2)

        ttk.Label(gridT, text='CD (F)').grid(row=0, column=2, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.cd).grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(gridT, text='CCS (F)').grid(row=1, column=2, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.ccs).grid(row=1, column=3, padx=2, pady=2)
        ttk.Label(gridT, text='CAS (F)').grid(row=2, column=2, padx=2, pady=2)
        ttk.Entry(gridT, textvariable=self.cas, state='readonly').grid(row=2, column=3, padx=2, pady=2)

        ttk.Button(gridT, text='Set Param', command=self.setParam).grid(row=0, column=4, padx=10, pady=2)
        ttk.Button(gridT, text='Reset Param', command=self.resetParam).grid(row=1, column=4, padx=10, pady=2)
        ttk.Button(gridT, text='Simulate', command=self.simulate).grid(row=2, column=4, padx=10, pady=2)
        ttk.Button(gridT, text='Clear Plot', command=self.clearPlot).grid(row=3, column=4, padx=10, pady=2)

    def displaySPAD(self):
        gridM = ttk.Labelframe(self.root, text='SPAD Params')
        gridM.grid(row=1, column=0, padx=5, pady=(0, 5), ipadx=2, ipady=2, sticky='ew')

        self.lcr = tk.IntVar(value=P.LCR)
        self.dcr = tk.IntVar(value=P.DCR)
        self.step = tk.DoubleVar(value=P.Step)
        self.bin = tk.IntVar(value=P.Bin)
        self.iqc = tk.DoubleVar(value=P.IQCenter)
        self.iqs = tk.DoubleVar(value=P.IQSigma)
        self.approb = tk.DoubleVar(value=P.ApProb)
        self.apbeta = tk.DoubleVar(value=P.ApBeta)

        ttk.Label(gridM, text='Light Counting Rate (Hz)').grid(row=0, column=0, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.lcr).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(gridM, text='Dark Counting Rate (Hz)').grid(row=1, column=0, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.dcr).grid(row=1, column=1, padx=2, pady=2)
        ttk.Label(gridM, text='Simulation Step (s)').grid(row=2, column=0, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.step).grid(row=2, column=1, padx=2, pady=2)
        ttk.Label(gridM, text='Bin').grid(row=3, column=0, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.bin).grid(row=3, column=1, padx=2, pady=2)

        ttk.Label(gridM, text='Quench I Center (A)').grid(row=0, column=2, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.iqc, state='readonly').grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(gridM, text='Quench I Sigma (A)').grid(row=1, column=2, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.iqs, state='readonly').grid(row=1, column=3, padx=2, pady=2)
        ttk.Label(gridM, text='Afterpulse Prob').grid(row=2, column=2, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.approb, state='readonly').grid(row=2, column=3, padx=2, pady=2)
        ttk.Label(gridM, text='Afterpulse Beta').grid(row=3, column=2, padx=2, pady=2, sticky='e')
        ttk.Entry(gridM, textvariable=self.apbeta, state='readonly').grid(row=3, column=3, padx=2, pady=2)

    def displaySample(self):
        gridB = ttk.Labelframe(self.root, text='Simulation')
        gridB.grid(row=2, column=0, padx=5, pady=(0, 5), ipadx=2, ipady=2, sticky='ew')

        self.dur = tk.DoubleVar(value=0)
        self.plotCB = {
            'RSIt': tk.BooleanVar(value=True),
            'SPADVt': tk.BooleanVar(value=False),
            'SPADIt': tk.BooleanVar(value=False),
            'DCIV': tk.BooleanVar(value=False)
        }
        self.simRB = tk.StringVar(value='Q')
        self.stepRB = tk.BooleanVar(value=True)
        self.saveRB = tk.BooleanVar(value=False)

        ttk.Label(gridB, text='Duration (s)').grid(row=0, column=0, padx=2, pady=2, sticky='w')
        ttk.Entry(gridB, textvariable=self.dur).grid(row=1, column=0, padx=2, pady=2)
        
        ttk.Checkbutton(gridB, text='Plot RS I-t', variable=self.plotCB['RSIt']).grid(row=0, column=1, padx=2, pady=2, sticky='w')
        ttk.Checkbutton(gridB, text='Plot SPAD V-t', variable=self.plotCB['SPADVt']).grid(row=1, column=1, padx=2, pady=2, sticky='w')
        ttk.Checkbutton(gridB, text='Plot SPAD I-t', variable=self.plotCB['SPADIt']).grid(row=2, column=1, padx=2, pady=2, sticky='w')
        ttk.Checkbutton(gridB, text='Plot DC I-V', variable=self.plotCB['DCIV']).grid(row=3, column=1, padx=2, pady=2, sticky='w')

        ttk.Radiobutton(gridB, text='1 Pulse (Q)', value='Q', variable=self.simRB).grid(row=0, column=2, padx=2, pady=2, sticky='w')
        ttk.Radiobutton(gridB, text='1 Pulse (R)', value='R', variable=self.simRB).grid(row=1, column=2, padx=2, pady=2, sticky='w')
        ttk.Radiobutton(gridB, text='1 Pulse (QR)', value='QR', variable=self.simRB).grid(row=2, column=2, padx=2, pady=2, sticky='w')
        ttk.Radiobutton(gridB, text='Long Time', value='T', variable=self.simRB).grid(row=3, column=2, padx=2, pady=2, sticky='w')

        ttk.Radiobutton(gridB, text='Default Step', value=False, variable=self.stepRB).grid(row=0, column=3, padx=2, pady=2, sticky='w')
        ttk.Radiobutton(gridB, text='Custom Step', value=True, variable=self.stepRB).grid(row=1, column=3, padx=2, pady=2, sticky='w')

        ttk.Radiobutton(gridB, text='Not Save', value=False, variable=self.saveRB).grid(row=0, column=4, padx=2, pady=2, sticky='w')
        ttk.Radiobutton(gridB, text='Save', value=True, variable=self.saveRB).grid(row=1, column=4, padx=2, pady=2, sticky='w')

    def displayCurve(self):
        gridR = ttk.Frame(self.root)
        gridR.grid(row=0, column=1, rowspan=4, padx=(0, 5), pady=5, sticky='news')
        self.curve = MatForm(gridR, self)

        self.xlimCB = tk.BooleanVar(value=False)
        self.xlimL = tk.DoubleVar(value=0)
        self.xlimH = tk.DoubleVar(value=0)
        self.ylimCB = tk.BooleanVar(value=False)
        self.ylimL = tk.DoubleVar(value=0)
        self.ylimH = tk.DoubleVar(value=0)
        self.legendCB = tk.BooleanVar(value=False)
        self.legend = tk.StringVar(value="['C0'], ['legend']")
        self.color = tk.StringVar(value='C0')
        self.colorRollCB = tk.BooleanVar(value=False)
        COLORS = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

        gridRB = ttk.Frame(self.root)
        gridRB.grid(row=4, column=1, padx=(0, 5), pady=(0, 5), sticky='news')
        ttk.Checkbutton(gridRB, text='Xlim', variable=self.xlimCB).grid(row=0, column=0, padx=2, pady=2, sticky='w')
        ttk.Entry(gridRB, textvariable=self.xlimL).grid(row=0, column=1, padx=2, pady=2)
        ttk.Entry(gridRB, textvariable=self.xlimH).grid(row=0, column=2, padx=2, pady=2)
        ttk.Checkbutton(gridRB, text='Ylim', variable=self.ylimCB).grid(row=1, column=0, padx=2, pady=2, sticky='w')
        ttk.Entry(gridRB, textvariable=self.ylimL).grid(row=1, column=1, padx=2, pady=2)
        ttk.Entry(gridRB, textvariable=self.ylimH).grid(row=1, column=2, padx=2, pady=2)
        ttk.Checkbutton(gridRB, text='Legend', variable=self.legendCB).grid(row=2, column=0, padx=2, pady=2, sticky='w')
        ttk.Entry(gridRB, textvariable=self.legend).grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky='ew')
        ttk.Label(gridRB, text='Color').grid(row=0, column=3, padx=2, pady=2)
        ttk.Combobox(gridRB, textvariable=self.color, values=COLORS, state='readonly').grid(row=0, column=4, padx=2, pady=2)
        ttk.Checkbutton(gridRB, text='Roll', variable=self.colorRollCB).grid(row=0, column=5, padx=2, pady=2, sticky='w')
        ttk.Button(gridRB, text='Set', width=8, command=self.setPlot).grid(row=1, column=5, padx=2, pady=2, sticky='w')

    def simulate(self):
        self.setParam(silence=True)
        if not hasattr(self, 'SPAD'):
            self.SPAD = SPAD(parent=self)
        self.SPAD.config(hd=self.stepRB.get(), 
                         save=self.saveRB.get(), 
                         plotcount=self.plotCount,
                         plotmode=self.plotMode,
                         color=self.color.get())
        self.SPAD.start(duration=self.dur.get(), simumode=self.simRB.get())
        if self.colorRollCB.get():
            self.rollColor()

    def setParam(self, silence=False):
        P.Va = self.va.get()
        P.Vb = self.vb.get()
        P.Rd = self.rd.get()
        P.Rl = self.rl.get()
        P.Rs = self.rs.get()
        P.Cd = self.cd.get()
        P.Cas = self.cas.get()
        P.Ccs = self.ccs.get()

        P.LCR = self.lcr.get()
        P.DCR = self.dcr.get()
        P.Step = self.step.get()
        P.Bin = self.bin.get()
        P.IQCenter = self.iqc.get()
        P.IQSigma = self.iqs.get()
        P.ApProb = self.approb.get()
        P.ApBeta = self.apbeta.get()

        P.setInducedParam()
        if not silence:
            messagebox.showinfo('Set Param', 'Success!')

    def resetParam(self):
        P.setByPreset()
        self.va.set(P.Va)
        self.vb.set(P.Vb)
        self.rd.set(P.Rd)
        self.rl.set(P.Rl)
        self.rs.set(P.Rs)
        self.cd.set(P.Cd)
        self.cas.set(P.Cas)
        self.ccs.set(P.Ccs)

        self.lcr.set(P.LCR)
        self.dcr.set(P.DCR)
        self.step.set(P.Step)
        self.bin.set(P.Bin)
        self.iqc.set(P.IQCenter)
        self.iqs.set(P.IQSigma)
        self.approb.set(P.ApProb)
        self.apbeta.set(P.ApBeta)
        self.dur.set(0)

    def clearPlot(self):
        plt.clf()
        self.curve.canvas.draw()
        if hasattr(self, 'SPAD'):
            delattr(self, 'SPAD')

    def setPlot(self):
        if hasattr(self, 'SPAD') and hasattr(self.SPAD, 'axes'):
            if self.legendCB.get():
                linecolors, linelegends = eval(self.legend.get())
            for i, ax in enumerate(self.SPAD.axes):
                if self.xlimCB.get():
                    ax.set_xlim(self.xlimL.get(), self.xlimH.get())
                if self.ylimCB.get():
                    ax.set_ylim(self.ylimL.get(), self.ylimH.get())
                if self.legendCB.get():
                    lines = []
                    for lc in linecolors:
                        l, = ax.plot([], [], marker='', color=lc)
                        lines.append(l)
                    ax.legend(lines, linelegends)
            self.curve.canvas.draw()

    def rollColor(self):
        c = self.color.get()
        c = int(c[c.rfind('\d')]) + 1
        self.color.set('C' + str(c%10))

    @property
    def plotCount(self):
        count = 0
        for p in self.plotCB.values():
            if p.get():
                count += 1
        return count

    @property
    def plotMode(self):
        mode = []
        for k, v in self.plotCB.items():
            if v.get():
                mode.append(k)
        return mode

    def close(self):
        self.root.destroy()
        plt.close()


class MatForm:

    def __init__(self, master=None, parent=None):
        self._parent = parent
        self.master = master
        # self.canvas = tk.Canvas()
        self.createMatplotlib()
        self.createForm()

    @property
    def parent(self):
        return self._parent

    def createMatplotlib(self):
        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)

        x = np.arange(0, 2*np.pi, 0.1)
        y = np.sin(x)

        ax.plot(x, y)

    def createForm(self):
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        toolbar.update()
        self.canvas._tkcanvas.pack(fill='both', expand=True)


if __name__ == '__main__':
    App()