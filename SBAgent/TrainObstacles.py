import sys
sys.path.append("..")

import numpy as np
from stable_baselines3 import TD3
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import PositionConstraint

sim_freq = 240
control_freq = 48
aggregate_phy_step = int(sim_freq/control_freq)

geoFence = PositionConstraint(0, 2, -0.5, 0.5, 0, 1)

env = ObstacleAviary(geoFence=geoFence, fixedAltitude=True, assistLearning=True, lenientUntil=500000, minObstacles=0, maxObstacles=3, showGeoFence=True, showTrajectory=True, freq=sim_freq, aggregatePhyStep=aggregate_phy_step)

n_actions = env.action_space.shape[-1]
action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=0.05*np.ones(n_actions))

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs/v4",
  name_prefix=f"td3_03ofa",
)

agent = TD3('MlpPolicy', env=env, verbose=1, action_noise=action_noise, learning_starts=100000)

agent.learn(10000000, callback=checkpoint_callback)

agent.save(f'models/v4/td3_03ofa')
