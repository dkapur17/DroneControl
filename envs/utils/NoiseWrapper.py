import numpy as np
import gym
from typing import Union, Tuple

from .DenoiseEngines import LPFDenoiseEngine, KFDenoiseEngine

class GaussianNoiseGenerator:

    def __init__(self, mu=0, sigma=1):
        self.mu = mu
        self.sigma = sigma

    def generateNoise(self, size=None):
        return np.random.normal(self.mu, self.sigma, size=size)

class NoiseWrapper(gym.Wrapper):

    def __init__(self, env:gym.Env, mu:float, sigma:float, denoiseEngine:Union[None, LPFDenoiseEngine, KFDenoiseEngine]=None) -> None:

        super().__init__(env)
        self.denoiseEngine = denoiseEngine
        self.noiseGenerator = GaussianNoiseGenerator(mu, sigma)

    def step(self, action:np.ndarray) -> Tuple[np.ndarray, float, bool, dict]:

        obs, reward, done, info = self.env.step(action)

        obs = self.corruptObservation(obs)

        if self.denoiseEngine is not None:
            obs = self.denoiseEngine(obs)
        
        return obs, reward, done, info

    def corruptObservation(self, obs:np.ndarray) -> np.ndarray:

        nx, ny, nz = self.noiseGenerator.generateNoise(3)
        if obs.shape[0] == 6:
            dxt, dyt, dzt, dxo, dyo, dzo = obs
        else:
            dxt, dyt, dxo, dyo, dzo = obs
            dzt = 0

        dxt += nx
        dyt += ny
        dzt += nz
        dxo += nx
        dyo += ny
        dzo += nz

        if obs.shape[0] == 6:
            obs = np.array([dxt, dyt, dzt, dxo, dyo, dzo])
        else:
            obs = np.array([dxt, dyt, dxo, dyo, dzo])

        return obs

    def reset(self) -> np.ndarray:

        if self.denoiseEngine is not None:
            self.denoiseEngine.clearHistory()
        
        return super().reset()