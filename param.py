import numpy as np

class QuenchParam:

    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.Tq = None

class RecoverParam:

    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.Tr = None
    
class Param:

    PRESET = [
        {
            'Step': 1e-9,
            'Bin': 1e6,
            'SR': 1e6,
            'LCR': 5e4,
            'DCR': 1e3,
            'IQCenter': 1e-4,
            'IQSigma': 4e-6,
            'ApProb': 1e-2,
            'ApBeta': None,
            'Cas': 0,
            'Ccs': 20e-12,
            'Rd': 500,
            'Cd': 10e-12,
            'Rl': 100e3,
            'Rs': 8.2e3,
            'Va': 45,
            'Vb': 43.7
        }
    ]

    def __init__(self, index=0):
        self.setByPreset(index)

    def setByPreset(self, index=0):
        p = iter(self.PRESET[index].values())
        self.Step = next(p) # Simulation Step
        self.Bin = next(p)
        self.SR = next(p) # SampleRate (Plot Step)
        self.LCR = next(p)
        self.DCR = next(p)
        self.IQCenter = next(p)
        self.IQSigma = next(p) # +-3sigma
        self.ApProb = next(p)
        self.ApBeta = next(p)
        self.Cas = next(p)
        self.Ccs = next(p)
        self.Rd = next(p)
        self.Cd = next(p)
        self.Rl = next(p)
        self.Rs = next(p)
        self.Va = next(p)
        self.Vb = next(p)
        self.setInducedParam()

    @property
    def StepInv(self):
        return 1/self.Step

    @property
    def SwitchOnProb(self):
        return (self.LCR + self.DCR)/self.StepInv

    @property
    def Imax(self):
        return (self.Va - self.Vb) / self.Rd

    def setInducedParam(s):
        s.Q = QuenchParam()
        s.Q.A = (s.Cd/s.Ccs*s.Rd + s.Rs + s.Rd)/(s.Rs*s.Rd*s.Cd)
        s.Q.B = 1/(s.Rs*s.Rd*s.Ccs*s.Cd)
        s.Q.C = (s.Va - s.Vb)/(s.Rl*s.Rs*s.Rd*s.Ccs*s.Cd)
        s.Q.Tq = s.Rd*s.Cd*(1+s.Rs/s.Rl) + s.Ccs*(s.Rs+s.Rd)
        s.R = RecoverParam()
        s.R.A = (s.Ccs/s.Cd*s.Rl + s.Rl + s.Rs)/(s.Ccs*s.Rs*s.Rl)
        s.R.B = 1/(s.Cd*s.Ccs*s.Rs*s.Rl)
        s.R.C = s.Va/(s.Ccs*s.Rs*s.Rl)
        s.R.Tr = (s.Cd +s.Ccs)*s.Rl + s.Cd*s.Rs


P = Param()
rng = np.random.default_rng()