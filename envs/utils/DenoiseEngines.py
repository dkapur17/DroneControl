import numpy as np
import scipy
from collections import deque
from pykalman import KalmanFilter

class LPFDenoiseEngine:

    def __init__(self, order:int, criticalFreq:float, ftype:str, freq:float) -> None:
        
        self.order = order
        self.criticalFreq = criticalFreq
        self.ftype = ftype
        self.b, self.a = scipy.signal.iirfilter(self.order, self.criticalFreq, fs=freq, btype="low", ftype=self.ftype)
        
        self._xs = deque([], maxlen=len(self.b))
        self._ys = deque([], maxlen=len(self.a)-1)

        self.observedHistory = []
        self.denoisedHistory = []
    
    # Empty call parameter for action
    def __call__(self, X:np.ndarray, _:np.ndarray) -> np.ndarray:
        self.observedHistory.append(X)
        denoisedX = self.process(X)
        self.denoisedHistory.append(denoisedX)
        return denoisedX

    def process(self, X:np.ndarray) -> np.ndarray:

        self._xs.appendleft(X)
        if len(self._xs) != len(self.b):
            self._ys.appendleft(X)
            return X
        else:
            y = np.dot(self.b, self._xs) - np.dot(self.a[1:], self._ys)
            y = y / self.a[0]
            self._ys.appendleft(y)
            return y

    # Empty call parameter for initPos
    def reset(self, _:np.ndarray) -> None:
        self._xs.clear()
        self._ys.clear()
        self.observedHistory.clear()
        self.denoisedHistory.clear()

    def __str__(self) -> str:

        return f"LPFDenoiseEngine({self.order}, {self.criticalFreq}, {self.ftype})"

class KFDenoiseEngine:

    def __init__(self, measurementNoise:float, dt:float, fixedAltitude:bool, initPos:np.ndarray, processNoise:float=0) -> None:

        self.fixedAltitude = fixedAltitude
        self.processNoise = processNoise
        
        if self.fixedAltitude:

            # state = [x, y, vx, vy]
            # observation = [x, y]
            # A = 4x4 matrix for state transition
            # C = 2x4 matrix for converting state into observation (I)
            # P0 = 4x4 
            # Q = 4x4 process noise covariance matrix
            # R = 2x2 measurement noise covariance matrix

            A = np.array([
                          [1, 0, dt, 0],
                          [0, 1, 0, dt],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]     
                        ])

            C = np.eye(4)[:2]

            x0 = np.array([initPos[0], initPos[1], 0, 0])
            P0 = np.eye(4)
            Q = np.eye(4) * processNoise**2 
            R = np.eye(2) * measurementNoise**2

        else:

            # state = [x, y, z, vx, vy, vz]
            # observation = [x, y, z]
            # A = 6x6 matrix for state transition
            # C = 3x6 matrix for converting state into observation (I)
            # P0 = 6x6 
            # Q = 6x6 process noise covariance matrix
            # R = 3x3 measurement noise covariance matrix

            A = np.array([
                          [1, 0, 0, dt, 0, 0],
                          [0, 1, 0, 0, dt, 0],
                          [0, 0, 1, 0, 0, dt],
                          [0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 1]
                        ])

            C = np.eye(6)[:3]

            x0 = np.array([initPos[0], initPos[1], initPos[2], 0, 0, 0])
            P0 = np.eye(6)
            Q = np.eye(6) * processNoise ** 2
            R = np.eye(3) * measurementNoise ** 2

        self.initFilter(A, C, x0, P0, Q, R)

        self.observedHistory = []
        self.denoisedHistory = []
    
        self.initConditions = [A, C, P0, Q, R]
        self.vdim = 2 if self.fixedAltitude else 3

    def __call__(self, X:np.ndarray, action:np.ndarray) -> np.ndarray:
        self.observedHistory.append(X)
        denoisedX = self.process(X, action)
        self.denoisedHistory.append(denoisedX)
        return denoisedX
        
    def process(self, z:np.ndarray, u:np.ndarray) -> np.ndarray:
        observation = z
        self.x_pred[self.vdim:] = u
        self.x_pred, self.P_pred = self.kf.filter_update(filtered_state_mean=self.x_pred, filtered_state_covariance=self.P_pred, observation=observation)

        return self.x_pred[:(2 if self.fixedAltitude else 3)].copy()

    def initFilter(self, A, C, x0, P0, Q, R):
        self.kf = KalmanFilter(transition_matrices=A, observation_matrices=C,
                                initial_state_mean=x0, initial_state_covariance=P0,
                                transition_covariance=Q, observation_covariance=R)

        # Save the variables needed later
        self.x_pred = x0
        self.P_pred = P0
        self.A = A

    def reset(self, initPos) -> None:
        self.observedHistory.clear()
        self.denoisedHistory.clear()

        A, C, P0, Q, R = self.initConditions

        if self.fixedAltitude:
            x0 = np.array([initPos[0], initPos[1], 0, 0])
        else:
            x0 = np.array([initPos[0], initPos[1], initPos[2], 0, 0, 0])

        self.initFilter(A, C, x0, P0, Q, R)
    
    def __str__(self) -> str:
        return f"KFDenoiseEngine({self.processNoise})"

        