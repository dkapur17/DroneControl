import numpy as np
import gym
from typing import Union, Tuple
from tabulate import tabulate

from .DenoiseEngines import LPFDenoiseEngine, KFDenoiseEngine
from ..ObstacleAviary import ObstacleAviary

class GaussianNoiseGenerator:

    def __init__(self, mu=0, sigma=1, persistForSteps=10) -> None:
        self.mu = mu
        self.sigma = sigma

        self.currNoise = None
        self.currSteps = 0
        self.persistForSteps = persistForSteps

    def generateNoise(self, size=None) -> np.ndarray:
        
        self.currSteps += 1
        if self.currNoise is None:
            self.currNoise = np.random.normal(self.mu, self.sigma, size=size)

        if self.currSteps > self.persistForSteps:
            self.currNoise = np.random.normal(self.mu, self.sigma, size=size)
            self.currSteps = 0

        return self.currNoise

    def __str__(self) -> str:
        return f"~N({self.mu, self.sigma})"

class NoiseWrapper(gym.Wrapper):

    def __init__(self, env:ObstacleAviary, mu:float, sigma:float, persistForSteps:int, denoiseEngine:Union[None, LPFDenoiseEngine, KFDenoiseEngine]=None) -> None:

        super().__init__(env)
        self.denoiseEngine = denoiseEngine
        self.noiseGenerator = GaussianNoiseGenerator(mu, sigma, persistForSteps)

        self.observation_space = self.buildObservationSpace()

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

    def buildObservationSpace(self):

        # [dxt dyt dzt dxo dyo dzo]
        # Get rid of z axis values for fixedAltitude
        obsLowerBound = np.array([-np.inf] * (4 if self.fixedAltitude else 6))
        obsUpperBound = np.array([np.inf] * (4 if self.fixedAltitude else 6))

        return gym.spaces.Box(low=obsLowerBound, high=obsUpperBound, dtype=np.float32)

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

        # Compute processed observation from raw observation
        obs = self.env._computeProcessedObservation(obs)
        
        return obs
        

    def __str__(self) -> str:
        if self.env.randomizeObstaclesEveryEpisode:
            obstacleDetails = f"Random Obstacles per Episode ~ U({self.env.minObstacles}, {self.env.maxObstacles})"
        else:
            obstacleDetails = ', '.join([f"({x}, {y}, {z})" for x,y,z in self.env.obstacles])
        
        envDetails = {
            'Obstacles': obstacleDetails,
            'Fixed Altitude': self.env.fixedAltitude,
            'Noise': "None" if (self.noiseGenerator.mu, self.noiseGenerator.sigma) == (0, 0) else str(self.noiseGenerator), 
            'Denoiser': str(self.denoiseEngine),
        }

        return tabulate([(k,v) for (k,v) in envDetails.items()], tablefmt='pretty')
