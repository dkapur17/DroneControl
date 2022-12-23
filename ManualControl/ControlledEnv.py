import sys
import matplotlib.pyplot as plt
import time
from ControllerAgent import ControllerAgent
sys.path.append("..")

import numpy as np

from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager

config = ConfigManager.loadConfig('configs/v1.json', training=False)

env = ObstacleAviary(**config)

agent = ControllerAgent()

done = False
rewards = []
states = []
obs = env.reset()
states.append(np.linalg.norm(obs))

print("Press Start to Start Simulation")
agent.wait_for_start()

while not done:
    action = agent.get_action()
    obs, reward, done, info = env.step(action)
    states.append(np.linalg.norm(obs))
    rewards.append(reward)
    env.render()
    time.sleep(0.01)
env.close()

plt.plot(range(len(states)), states)
plt.title("Distance to Target")
plt.show()

plt.plot(range(len(rewards)), rewards)
plt.title("Reward")
plt.show()