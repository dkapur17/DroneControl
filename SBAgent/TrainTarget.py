import sys
sys.path.append("..")

import numpy as np
from stable_baselines3 import TD3
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.TargetAviary import TargetAviary
from envs.utils import PositionConstraint

sim_freq = 240
control_freq = 48
aggreagate_phy_steps = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = TargetAviary(geoFence=geoFence, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggreagate_phy_steps)

n_actions = env.action_space.shape[-1]
action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=0.05*np.ones(n_actions))

checkpoint_callback = CheckpointCallback(
  save_freq=100000,
  save_path="./logs/",
  name_prefix="sb_td3_target",
)

agent = TD3('MlpPolicy', env=env, verbose=1, action_noise=action_noise, learning_starts=10000)

agent.learn(5000000, callback=checkpoint_callback)

agent.save('models/sb_td3_target')
