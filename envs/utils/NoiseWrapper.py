import numpy as np
import gym
from typing import Union, Tuple

from .DenoiseEngines import LPFDenoiseEngine, KFDenoiseEngine
from ..ObstacleAviary import ObstacleAviary

class GaussianNoiseGenerator:

    def __init__(self, mu=0, sigma=1):
        self.mu = mu
        self.sigma = sigma

    def generateNoise(self, size=None):
        return np.random.normal(self.mu, self.sigma, size=size)

class NoiseWrapper(gym.Wrapper):

    def __init__(self, env:ObstacleAviary, mu:float, sigma:float, denoiseEngine:Union[None, LPFDenoiseEngine, KFDenoiseEngine]=None) -> None:

        super().__init__(env)
        self.denoiseEngine = denoiseEngine
        self.noiseGenerator = GaussianNoiseGenerator(mu, sigma)

    def step(self, action:np.ndarray) -> Tuple[np.ndarray, float, bool, dict]:

        obs, reward, done, info = self.env.step(action)

        obs = self.corruptObservation(obs)

        if self.denoiseEngine is not None:
            vel = self.computeVelocityFromAction(action)
            pos_dim = 2 if self.env.fixedAltitude else 3
            obs[:pos_dim] = self.denoiseEngine(obs[:pos_dim].copy(), vel)

        # Compute processed observation from raw observation
        obs = self.env._computeProcessedObservation(obs)
        
        return obs, reward, done, info

    def computeVelocityFromAction(self, action):

        vel_dim = 2 if self.env.fixedAltitude else 3
        
        if np.linalg.norm(action[:vel_dim]) != 0:
            v_unit_vector = action[:vel_dim] / np.linalg.norm(action[:vel_dim])
        else:
            v_unit_vector = np.zeros(vel_dim)
        vel = self.env.SPEED_LIMIT * np.abs(action[-1]) * v_unit_vector

        return vel

    def corruptObservation(self, obs:np.ndarray) -> np.ndarray:

        noise = self.noiseGenerator.generateNoise(2 if self.env.fixedAltitude else 3)
        obs[:noise.shape[0]] += noise
        return obs

    def reset(self) -> np.ndarray:

        obs = super().reset()
        
        if self.denoiseEngine is not None:
            self.denoiseEngine.reset(self.env.initPos)
        
        return obs
        