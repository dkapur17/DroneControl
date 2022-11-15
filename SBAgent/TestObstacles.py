import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np
from stable_baselines3 import TD3
from envs.ObstacleAviary import ObstacleAviary 
from envs.utils import PositionConstraint

nObstacles = 0

sim_freq = 240
control_freq = 48
aggreagate_phy_steps = int(sim_freq/control_freq)

geoFence = PositionConstraint(-2, 2, -2, 2, 0.5, 2.5)

env = ObstacleAviary(geoFence=geoFence, nObstacles=nObstacles, episodeLength=1000, freq=sim_freq, aggregate_phy_steps=aggreagate_phy_steps, showTrajectory=True, gui=True, showGeoFence=True)

agent = TD3.load(f'models/sb_td3_{nObstacles}_obstacles', env=env)

done = False
rewards = []
states = []
obs = env.reset()
states.append(np.linalg.norm(obs))
while not done:
	action, _state = agent.predict(obs, deterministic=True)
	obs, reward, done, info = env.step(action)
	states.append(np.linalg.norm(obs))
	rewards.append(reward)
env.close()

plt.plot(range(len(states)), states)
plt.title("Distance to target")
plt.show()
plt.plot(range(len(rewards)), rewards)
plt.title("Reward")
plt.show()	
