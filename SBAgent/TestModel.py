import sys
sys.path.append("..")

from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt
from envs.NoisyAviary import NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser


version = 'v1_practical'


config = ConfigManager.loadConfig(f'../configs/{version}.json')

config_noise = config["noise"]
config_mean = config["mean"]
config_std_dev = config["std_dev"]
config_denoiser = config["denoiser"]
config_measurement_noise = config["measurement_noise"]

del config["noise"]
del config["mean"]
del config["std_dev"]
del config["denoiser"]
del config["measurement_noise"]


if config_noise == False:
    env = ObstacleAviary(**config)
else:
  if config_denoiser=="None":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=None)
  if config_denoiser=="LPFDenoiser":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=LPFDenoiser())
  elif config_denoiser=="KFDenoiser":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=KFDenoiser(measurement_noise=config_measurement_noise), reward_mech=None)

agent = PPO.load(f'models/ppo_{version}')



done = False
rewards = []
states = []
obs = env.reset()
states.append(np.linalg.norm(obs[:2]))

while not done:
    action, _state = agent.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    print("Outside", obs)
    states.append(np.linalg.norm(obs[:2]))
    rewards.append(reward)
env.close()

plt.plot(range(len(states)), states)
plt.title("Distance to target")
plt.show()
plt.plot(range(len(rewards)), rewards)
plt.title("Reward")
plt.show()
