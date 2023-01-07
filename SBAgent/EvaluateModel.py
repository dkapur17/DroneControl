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

version = 'v5_2d_lpf_0.05_0.1'
# version = 'v3'




config = ConfigManager.loadConfig(f'../configs/{version}.json')

# denoiser = None
denoiser = LPFDenoiser()
# denoiser = KFDenoiser(measurement_noise=0.1)

# env = ObstacleAviary(**config)
env = NoiseWrapper1(env=ObstacleAviary(**config), noise_mean=0, noise_stddev=0.1, denoiser=denoiser)
# env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=0, noise_stddev=0.05, denoiser=denoiser)

# agent = PPO.load(f'models/ppo_{version}')
agent = PPO.load(f'logs/ppo_v5_2d_noise_0.1_5000000_steps')


totalTrials = 1000
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
print(f"Mean Reward: {sum(rewards)/len(rewards):.2f}")
print(f"Minimum Reward: {min(rewards):.2f}")
print(f"Maximium Reward: {max(rewards):.2f}")
print(f"Mean Episode Duration: {sum(durations)/len(durations):.2f} steps")
print(f"Shortest Episode: {min(durations)} steps")
print(f"Longest Episode: {max(durations)} steps")
print(f"---------------------------------------------------------")
