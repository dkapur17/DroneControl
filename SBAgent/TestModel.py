import sys
sys.path.append("..")

from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt

version = 'v1'

config = ConfigManager.loadConfig(f'configs/{version}.json')

env = ObstacleAviary(**config)

agent = PPO.load(f'models/ppo_{version}')

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
