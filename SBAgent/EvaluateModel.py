import sys
sys.path.append("..")

import os
import argparse
from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("configFileName", help="Name of the environment config file.", type=str)
parser.add_argument("inputModelName", help="(base|finetuned + )Name of the model to load.", type=str)
parser.add_argument("--trials", default=100, help="Number of episodes to evaluate for.", type=int)
parser.add_argument("--gui", action=argparse.BooleanOptionalAction, help="Whether or not to show GUI")

args = parser.parse_args()

configFileName = args.configFileName
modelName = args.outputModelName

env = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', configFileName), gui=args.gui)
agent = PPO.load(os.path.join('models', modelName))

totalTrials = args.trails
successfulTrials = 0
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
