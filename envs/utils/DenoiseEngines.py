import numpy as np
import scipy
from collections import deque

class LPFDenoiseEngine:

    def __init__(self, order, criticalFreq, ftype, freq):
        
        self.order = order
        self.b, self.a = scipy.signal.iirfilter(order, criticalFreq, fs=freq, btype="low", ftype=ftype)
        
        self._xs = deque([], maxlen=len(self.b))
        self._ys = deque([], maxlen=len(self.a)-1)

        self.observedHistory = []
        self.denoisedHistory = []
    
    def __call__(self, X):
        self.observedHistory.append(X)
        denoisedX = self.process(X)
        self.denoisedHistory.append(denoisedX)
        return denoisedX

    def process(self, X):

        self._xs.appendleft(X)
        if len(self._xs) != len(self.b):
            self._ys.appendleft(X)
            return X
        else:
            y = np.dot(self.b, self._xs) - np.dot(self.a[1:], self._ys)
            y = y / self.a[0]
            self._ys.appendleft(y)
            return y

    def clearHistory(self):
        self._xs.clear()
        self._ys.clear()
        self.observedHistory.clear()
        self.denoisedHistory.clear()

class KFDenoiseEngine:

    def __init__(self):
        pass