import sys

import matplotlib.pyplot as plt
import numpy as np
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager

config = ConfigManager.loadConfig('configs/v1.json')

env = ObstacleAviary(**config)

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