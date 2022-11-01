import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np
from TD3 import TD3
from envs.TargetAviary import TargetAviary
from envs.utils import PositionConstraint

sim_freq = 240
control_freq = 48
aggreagate_phy_steps = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = TargetAviary(geoFence=geoFence, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggreagate_phy_steps, gui=True, showTrajectory=True, showGeoFence=True)

agent = TD3(env)
agent.load('models/td3_target')

done = False
rewards = []
states = []
obs = env.reset()
states.append(np.linalg.norm(obs))
obs = agent.tensorify(obs).float()

while not done:
    action = agent.select_action(obs)
    obs, reward, done, info = env.step(action)
    states.append(np.linalg.norm(obs))
    obs = agent.tensorify(obs).float()
    rewards.append(reward)
env.close()

plt.plot(range(len(states)), states)
plt.title("Distance to target")
plt.show()
plt.plot(range(len(rewards)), rewards)
plt.title("Reward")
plt.show()	
