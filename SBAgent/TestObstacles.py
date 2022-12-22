import sys
sys.path.append("..")
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import PositionConstraint
from stable_baselines3 import TD3
import numpy as np
import matplotlib.pyplot as plt


sim_freq = 240
control_freq = 48
aggregate_phy_step = int(sim_freq / control_freq)


geoFence = PositionConstraint(0, 2, -0.5, 0.5, 0, 1)

env = ObstacleAviary(geoFence=geoFence, episodeLength=-1, fixedAltitude=True, assistLearning=False, gui=True, minObstacles=0,
                     maxObstacles=1, showGeoFence=True, showTrajectory=True, freq=sim_freq, aggregatePhyStep=aggregate_phy_step)

agent = TD3.load(f'models/v4/td3_03ofa', env=env)

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
