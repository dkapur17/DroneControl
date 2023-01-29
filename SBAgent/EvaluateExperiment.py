import sys
sys.path.append("..")

import os
import argparse
import json
import numpy as np
import random
from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
from tqdm import tqdm
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument("experimentConfigFile", help="Experiment Config File Path")
parser.add_argument("-t", "--trials", type=int, default=10, help="Number of episodes to evaluate for.")
parser.add_argument('--gui', action='store_true', help='Enable GUI')
parser.add_argument('--no-gui', action='store_false', dest='gui', help='Disable GUI')
args = parser.parse_args()

np.random.seed(42)
random.seed(42)

with open(args.experimentConfigFile, 'r') as f:
    experimentConfig = json.load(f)

experimentName = experimentConfig["name"]
trainEnvConfig = experimentConfig["trainParameters"]["config"]
evaluationEnvConfig = experimentConfig["evaluationParameters"]["config"]
modelName = experimentConfig["evaluationParameters"]["inputModelName"]

print(f"Running Evaluation on {experimentName}")

trainEnv = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', trainEnvConfig), gui=False)
print("Model trained on")
print(trainEnv)
trainEnv.close()
del trainEnv

print("Evaluating Model on")
env = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', evaluationEnvConfig), gui=args.gui)
print(env)

agent = PPO.load(os.path.join('models', modelName, 'best_model'))

totalTrials = args.trials
successfulTrials = 0
rewards = []
durations = []
nCollisions = 0
incompleteDistances = []
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
    elif info['reason'] == "collision":
        nCollisions +=1
    else:
        incompleteDistances.append(np.linalg.norm(obs[:(obs.shape[0]//2)]))
    
    rewards.append(episodeReward)
    durations.append(episodeDuration)

env.close()

evaluationResults = {
    'Success Rate': f"{successfulTrials/totalTrials * 100:.2f}%",
    'Collision Rate': f"{nCollisions/totalTrials * 100:.2f}%",
    'Mean Incompletion Distance': f"{sum(incompleteDistances)/len(incompleteDistances):.2f}m" if len(incompleteDistances) > 0 else "N/A",
    'Mean Reward': f"{sum(rewards)/len(rewards):.2f}",
    'Mean Episode Length': f"{sum(durations)/len(durations)}"
}

evaluationTable = [[k, v] for k,v in evaluationResults.items()]
print()
print(tabulate(evaluationTable, headers=["Metric", "Value"], tablefmt='github'))