import sys
sys.path.append("..")

import numpy as np
import torch
from stable_baselines3 import TD3
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import PositionConstraint

nObstacles = 0

np.random.seed(42)
torch.manual_seed(42)

sim_freq = 240
control_freq = 48
aggregate_phy_step = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = ObstacleAviary(geoFence=geoFence, nObstacles=nObstacles, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggregate_phy_step)

n_actions = env.action_space.shape[-1]
action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=0.05*np.ones(n_actions))

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs/",
  name_prefix=f"sb_td3_{nObstacles}_obstacles",
)

agent = TD3('MlpPolicy', env=env, verbose=1, action_noise=action_noise, learning_starts=100000, seed=5)

agent.learn(10000000, callback=checkpoint_callback)

agent.save(f'models/sb_td3_{nObstacles}_obstacles')
