import sys
sys.path.append("..")

import os
import argparse
import numpy as np
from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
from tqdm import tqdm
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument("configFileName", help="Name of the environment config file.", type=str)
parser.add_argument("inputModelPath", help="Path to model to evaluate", type=str)
parser.add_argument("-t", "--trials", default=100, help="Number of episodes to evaluate for.", type=int)
parser.add_argument('--gui', action='store_true', help='Enable GUI')
parser.add_argument('--no-gui', action='store_false', dest='gui', help='Disable GUI')
args = parser.parse_args()

configFileName = args.configFileName
modelName = args.inputModelPath

env = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', configFileName), gui=args.gui)
agent = PPO.load(modelName)

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
print(tabulate(evaluationTable, headers=["Metric", "Value"], tablefmt='github'))