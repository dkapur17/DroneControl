import sys
sys.path.append("..")

import os
import argparse
import json
import numpy as np
import random
import tempfile
from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
from tqdm import tqdm
from tabulate import tabulate

class NoStdStreams(object):
    def __init__(self,stdout = None, stderr = None):
        self.devnull = open(os.devnull,'w')
        self._stdout = stdout or self.devnull or sys.stdout
        self._stderr = stderr or self.devnull or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()


def evaluate(mu, sigma, denoiser, modelPath, trials, gui=False, fixed=False):

    seeds = np.load('evalSeeds.npy').tolist()

    envFile = {
        'none': f'../configs/NoDenoiserEnv{"Fixed" if fixed else ""}.json',
        'lpf': f'../configs/LPFDenoiserEnv{"Fixed" if fixed else ""}.json',
        'kf': f'../configs/KFDenoiserEnv{"Fixed" if fixed else ""}.json'
    }[denoiser]

    with open(envFile, 'r') as f:
        envConfig = json.load(f)

    envConfig['noiseParameters']['mu'] = mu
    envConfig['noiseParameters']['sigma'] = sigma

    with open('tempConfigFile.json', 'w') as f:
        json.dump(envConfig, f)

    with NoStdStreams():
        env = EnvBuilder.buildEnvFromConfig('tempConfigFile.json', gui=gui)
        print("Evaluating Model on")
        print(env)

    os.remove('tempConfigFile.json')

    agent = PPO.load(modelPath)

    totalTrials = trials
    successfulTrials = 0
    rewards = []
    durations = []
    nCollisions = 0
    incompleteDistances = []
    for i in range(totalTrials):

        np.random.seed(seeds[i])
        random.seed(seeds[i])

        done = False
        episodeReward = 0
        episodeDuration = 0
        distToTarget = []
        obs = env.reset()
        while not done:
            episodeDuration += 1
            action, _ = agent.predict(obs, deterministic=True)

            obs, reward, done, info = env.step(action)
            episodeReward += reward
            distToTarget.append(np.linalg.norm(obs[:(obs.shape[0]//2)]))
        if info['success']:
            successfulTrials += 1
        elif info['reason'] == "collision":
            nCollisions +=1
        else:
            incompleteDistances.append(info['dist'])
        
        rewards.append(episodeReward)
        durations.append(episodeDuration)

        print(f"Trial {i+1}/{totalTrials}. Current Success Rate: {(successfulTrials/(i+1))*100:.2f}%       ", end="\r", flush=True, file=sys.stderr)

    env.close()

    print()
    evaluationResults = {
        'Success Rate': f"{successfulTrials/totalTrials * 100:.2f}%",
        'Collision Rate': f"{nCollisions/totalTrials * 100:.2f}%",
        'Mean Incompletion Distance': f"{sum(incompleteDistances)/len(incompleteDistances):.2f}m" if len(incompleteDistances) > 0 else "N/A",
        'Mean Reward': f"{sum(rewards)/len(rewards):.2f}",
        'Mean Episode Length': f"{sum(durations)/len(durations)}"
    }

    evaluationTable = [[k, v] for k,v in evaluationResults.items()]

    return evaluationTable

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("modelPath", help="Path to the Model", type=str)
    parser.add_argument("mu", help="Mean of the Noise", type=float)
    parser.add_argument("sigma", help="Standard Deviation of the Noise", type=float)
    parser.add_argument("denoiser", help="Denoiser to Use", choices={'none', 'lpf', 'kf'}, type=str)

    parser.add_argument("-t", "--trials", type=int, default=10, help="Number of episodes to evaluate for.")
    parser.add_argument('--gui', action='store_true', help='Enable GUI')
    parser.add_argument('--no-gui', action='store_false', dest='gui', help='Disable GUI')
    parser.add_argument('--fixed', action='store_true', help='Use Fixed Obstacles')
    parser.add_argument('--random', action='store_false', dest='fixed', help='Use Randomized Obstacles')

    args = parser.parse_args()

    evaluationTable = evaluate(**vars(args))
    print()
    print(tabulate(evaluationTable, headers=["Metric", "Value"], tablefmt='github'))