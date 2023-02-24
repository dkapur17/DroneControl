import os
import sys
import argparse
import numpy as np
import itertools
from tabulate import tabulate
from EvaluateModel import evaluate
from joblib import Parallel, delayed
from multiprocessing import Manager
import threading
import tempfile
from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
import json
import random
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("modelPath", help="Path to the Model", type=str)
parser.add_argument("-t", "--trials", type=int, default=1000, help="Number of episodes to evaluate the model for in each environment.")
args = parser.parse_args()

manager = Manager()
sharedMem = manager.dict()
processCompleted = False

def printUpdate():
    while not processCompleted:
        sleep(0.1)
        i = 0
        for k, v in sorted(sharedMem.items()):
            comb, success, completed, total = v
            if completed == total:
                continue
            print(f"Process {k} {comb} -> Iteration {completed}/{total}: Success Rate = {(success/completed if completed else 0)*100:.2f}%               ", file=sys.stderr)
            i += 1
        print("\33[2K\033[F"*i, end='', file=sys.stderr)


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


def evaluateOnCombination(process, comb):
    mu, sigma, denoiser = comb
    denoiser = denoiser.lower()
    seeds = np.load('evalSeeds.npy').tolist()

    envFile = {
        'none': '../configs/NoDenoiserEnv.json',
        'lpf': '../configs/LPFDenoiserEnv.json',
        'kf': '../configs/KFDenoiserEnv.json'
    }[denoiser]

    with open(envFile, 'r') as f:
        envConfig = json.load(f)

    envConfig['noiseParameters']['mu'] = mu
    envConfig['noiseParameters']['sigma'] = sigma

    tempConfigFile = tempfile.NamedTemporaryFile()

    with open(tempConfigFile.name, 'w') as f:
        json.dump(envConfig, f)

    with NoStdStreams():
        env = EnvBuilder.buildEnvFromConfig(tempConfigFile.name, gui=False)
        print("Evaluating Model on")
        print(env)

    agent = PPO.load(args.modelPath)
    totalTrials = args.trials
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

        sharedMem[process] = (comb, successfulTrials, i+1, totalTrials)

    env.close()

    evaluationResults = {
        'Success Rate': f"{successfulTrials/totalTrials * 100:.2f}%",
        'Collision Rate': f"{nCollisions/totalTrials * 100:.2f}%",
        'Mean Incompletion Distance': f"{sum(incompleteDistances)/len(incompleteDistances):.2f}m" if len(incompleteDistances) > 0 else "N/A",
        'Mean Reward': f"{sum(rewards)/len(rewards):.2f}",
        'Mean Episode Length': f"{sum(durations)/len(durations)}"
    }

    sharedMem[process] = (comb, successfulTrials, totalTrials, totalTrials)

    return [[k, v] for k,v in evaluationResults.items()]

def printResultsMarkdown(mus, sigmas, denoisers, results):

    print("# Evaluation Results")
    print(f"**Model**: `{args.modelPath}`")
    print(f"mus = {mus}, sigmas = {sigmas}, denoisers = {denoisers}")
    i = 0
    for mu in mus:
        for sigma in sigmas:
            for denoiser in denoisers:
                res = results[i]
                i += 1
                print(f"### $\mu = {mu}$ | $\sigma = {sigma}$ | Denoiser = `{denoiser}`\n")
                print(tabulate(res, headers=["Metric", "Value"], tablefmt='github'))
                print("---\n")



if __name__ == "__main__":

    mus = np.arange(0, 0.31, 0.01)
    sigmas = [0]
    denoisers = ['None', 'LPF', 'KF']

    combinations = itertools.product(mus, sigmas, denoisers)

    print(f"Evaluation on Model {args.modelPath}", file=sys.stderr)
    print(file=sys.stderr)
    print(f"Total Processes: {len(mus)*len(sigmas)*len(denoisers)}", file=sys.stderr)
    
    printThread = threading.Thread(target=printUpdate)
    printThread.start()
    
    results = Parallel(n_jobs=12)(delayed(evaluateOnCombination)(i, c) for i, c in enumerate(combinations))
    processCompleted = True
    
    printThread.join()

    printResultsMarkdown(mus, sigmas, denoisers, results)
