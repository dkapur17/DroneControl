import sys
sys.path.append("..")

from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt
from envs.NoisyAviary import NoiseWrapper1,NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser


# version = 'v5_2d_lpf_0.05_0.1'
version = 'v5_2d_kf_0.1'
# version ='v5_2d_noise_0.01'



config = ConfigManager.loadConfig(f'../configs/{version}.json')

# denoiser=None
# denoiser = LPFDenoiser()
denoiser = KFDenoiser(measurement_noise=0.1)

# env = ObstacleAviary(**config)
# env = NoiseWrapper1(env=ObstacleAviary(**config), noise_mean=0, noise_stddev=0.05, denoiser=denoiser)
env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=0, noise_stddev=0.1, denoiser=denoiser)

# agent = PPO.load(f'models/ppo_{version}')
agent = PPO.load(f'logs/ppo_v5_2d_kf_0.1_8000000_steps.zip')



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
