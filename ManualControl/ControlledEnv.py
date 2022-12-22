import sys
import matplotlib.pyplot as plt
import time
from ControllerAgent import ControllerAgent
sys.path.append("..")

import numpy as np

from envs.TunnelAviary import ObstacleAviary
from envs.utils import PositionConstraint

nObstacles = 0

sim_freq = 240
control_freq = 48
aggregate_phy_step = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = ObstacleAviary(geoFence=geoFence, gui=True, nObstacles=nObstacles, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggregate_phy_step)

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