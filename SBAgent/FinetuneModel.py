import sys
sys.path.append("..")

import os
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.utils.EnvBuilder import EnvBuilder

parser = argparse.ArgumentParser()
parser.add_argument("configFileName", help="Name of the environment config file.", type=str)
parser.add_argument("inputModelName", help="(base|finetuned + )Name of the model to load.", type=str)
parser.add_argument("outputModelName", help="(base|finetuned + )Name to save the model with.", type=str)
parser.add_argument("--steps", default=10_000_000, help="Number of timesteps to finetune for", type=int)
args = parser.parse_args()

configFileName = args.configFileName
inputModelName = args.inputModelName
outputModelName = args.outputModelName
n_steps = args.steps

env = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', configFileName), gui=False)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=outputModelName,
)

agent = PPO.load(os.path.join('models', inputModelName))
agent.learn(n_steps, callback=checkpoint_callback)
agent.save(os.path.join('model', outputModelName))