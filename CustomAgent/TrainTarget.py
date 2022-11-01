import sys
sys.path.append("..")
sys.stdout = sys.stderr # For printing synchronously on HPC

import numpy as np
from envs.TargetAviary import TargetAviary
from envs.utils import PositionConstraint
from TD3 import TD3

sim_freq = 240
control_freq = 48
aggreagate_phy_steps = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = TargetAviary(geoFence=geoFence, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggreagate_phy_steps)

agent = TD3(env)
rewards, critic_losses, actor_losses = agent.learn(n_episodes=3000, verbose=True)

agent.save("models/td3_target")
