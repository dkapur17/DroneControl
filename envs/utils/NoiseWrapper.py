import numpy as np
import gym
from typing import Union, Tuple
from tabulate import tabulate

from .DenoiseEngines import LPFDenoiseEngine, KFDenoiseEngine
from ..ObstacleAviary import ObstacleAviary
from ..MocapAviary import MocapAviary

class GaussianNoiseGenerator:

    def __init__(self, mu=0, sigma=1) -> None:
        self.mu = mu
        self.sigma = sigma

    def generateNoise(self, size=None) -> np.ndarray:
        
        return np.random.normal(self.mu, self.sigma, size=size)

    def __str__(self) -> str:
        return f"~N({self.mu}, {self.sigma})"

class NoiseWrapper(gym.Wrapper):

    def __init__(self, env:Union[ObstacleAviary,MocapAviary], mu:float, sigma:float, denoiseEngine:Union[None, LPFDenoiseEngine, KFDenoiseEngine]=None) -> None:

        super().__init__(env)
        self.denoiseEngine = denoiseEngine
        self.noiseGenerator = GaussianNoiseGenerator(mu, sigma)

        self.observation_space = self.buildObservationSpace()

    def step(self, action:np.ndarray) -> Tuple[np.ndarray, float, bool, dict]:

        obs, reward, done, info = self.env.step(action)

        obs = self.corruptObservation(obs)

        if self.denoiseEngine is not None:
            vel = self.computeVelocityFromAction(action)
            pos_dim = 2 if self.env.fixedAltitude else 3
            obs[:pos_dim] = self.denoiseEngine(obs[:pos_dim].copy(), vel)

        self.noisyTrajectory.append(np.array([obs[0], obs[1], self.altitude]) if self.fixedAltitude else obs[:3])

        # Compute processed observation from raw observation
        obs = self.env._computeProcessedObservation(obs)
        
        return obs, reward, done, info

    def buildObservationSpace(self):

        if not self.fixedAltitude:

            obsUpperBound = np.array([self.geoFence.xmax - self.geoFence.xmin, #dxt
                                        self.geoFence.ymax - self.geoFence.ymin, #dyt
                                        self.geoFence.zmax - self.geoFence.zmin, #dzt
                                        self.geoFence.xmax - self.geoFence.xmin, #dxo
                                        self.geoFence.ymax - self.geoFence.ymin, #dyo
                                        self.geoFence.zmax - self.geoFence.zmin, #dzo
                                    ])

        else:
            obsUpperBound = np.array([self.geoFence.xmax - self.geoFence.xmin, #dxt
                                        self.geoFence.ymax - self.geoFence.ymin, #dyt
                                        self.geoFence.xmax - self.geoFence.xmin, #dxo
                                        self.geoFence.ymax - self.geoFence.ymin, #dyo
                                    ])


        obsLowerBound = -obsUpperBound
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
        
        # Corrupting the initial observation
        obs = self.corruptObservation(obs)

        # Denoising the initial observation
        if self.denoiseEngine is not None:
            self.denoiseEngine.reset(self.env.initPos)
            pos_dim = 2 if self.env.fixedAltitude else 3
            obs[:pos_dim] = self.denoiseEngine(obs[:pos_dim].copy(), np.zeros(pos_dim))

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
