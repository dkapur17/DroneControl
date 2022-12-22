import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import PositionConstraint

sim_freq = 240
control_freq = 48
aggregate_phy_step = int(sim_freq/control_freq)

geoFence = PositionConstraint(0, 2, -0.5, 0.5, 0, 1)

env = ObstacleAviary(geoFence=geoFence, fixedAltitude=True, lenientUntil=500, minObstacles=3, maxObstacles=5, gui=True, showGeoFence=True, showTrajectory=True, freq=sim_freq, aggregatePhyStep=aggregate_phy_step)

for _ in range(3):
    done = False
    obs = env.reset()
    ep_len = 0
    rewards = []
    while not done:
        ep_len += 1
        obs, rew, done, info = env.step(np.array([1, 0, 1]))
        rewards.append(rew)
    print(f"Episode Length: {ep_len}")
    plt.plot(range(len(rewards)), rewards)
    plt.show()