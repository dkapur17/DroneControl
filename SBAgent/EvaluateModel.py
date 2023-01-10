import sys
sys.path.append("..")

from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from stable_baselines3 import PPO
from tqdm import tqdm
from envs.NoisyAviary import NoiseWrapper1,NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser
import random
import numpy as np
random.seed(0)
np.random.seed(0)

version = 'v6_lpf_0.1_exp_avg_alpha=0.1'



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
    env = NoiseWrapper1(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=None)
  if config_denoiser=="LPFDenoiser":
    env = NoiseWrapper1(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=LPFDenoiser())
  elif config_denoiser=="KFDenoiser":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=KFDenoiser(measurement_noise=config_measurement_noise))

print(f'models/ppo_{version}')
agent = PPO.load(f'models/ppo_{version}')
# agent = PPO.load(f'logs/ppo_v6_kf_9000000_steps.zip')


totalTrials = 100
successfulTrials = 0
collisions = 0
unsuccessfulDistances = []
rewards = []
durations = []
for i in tqdm(range(totalTrials)):

    done = False
    episodeReward = 0
    episodeDuration = 0
    obs = env.reset()
    while not done:
        episodeDuration += 1
        action, _ = agent.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        episodeReward += reward

    if info['success']:
        successfulTrials += 1
    else:
        if info['reason'] == 'collision':
            collisions += 1
        else:
            distToTarget = np.linalg.norm(obs[:2])
            unsuccessfulDistances.append(distToTarget)
    
    rewards.append(episodeReward)
    durations.append(episodeDuration)

env.close()


print(f"---------------------------------------------------------")
print(f"EVALUATION STATISTICS")
print()
print(f"Success Rate: {successfulTrials/totalTrials * 100:.2f}%")
print(f"Collision Rate: {collisions/totalTrials * 100:.2f}%")
if len(unsuccessfulDistances) > 0:
    print(f"Mean Distance to Target: {sum(unsuccessfulDistances)/len(unsuccessfulDistances):.2f}")
else:
    print(f"Mean Distance to Target: N/A")
print(f"Mean Reward: {sum(rewards)/len(rewards):.2f}")
print(f"Minimum Reward: {min(rewards):.2f}")
print(f"Maximium Reward: {max(rewards):.2f}")
print(f"Mean Episode Duration: {sum(durations)/len(durations):.2f} steps")
print(f"Shortest Episode: {min(durations)} steps")
print(f"Longest Episode: {max(durations)} steps")
print(f"---------------------------------------------------------")
