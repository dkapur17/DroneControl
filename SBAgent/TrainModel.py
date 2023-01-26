import sys
sys.path.append("..")

import os
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.utils.EnvBuilder import EnvBuilder


parser = argparse.ArgumentParser()
parser.add_argument("configFileName", help="Name of the environment config file.", type=str)
parser.add_argument("outputModelName", help="(base|finetuned + )Name to save the model with.", type=str)
parser.add_argument("-s", "--steps", default=2_000_000, help="Number of timesteps to train for", type=int)
args = parser.parse_args()

configFileName = args.configFileName
modelName = args.outputModelName
n_steps = args.steps

assert modelName.startswith('base') or modelName.startswith('finetuned'), "Model name must include base/finetuned"

env = EnvBuilder.buildEnvFromConfig(os.path.join('..', 'configs', configFileName), gui=False)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path=os.path.join("checkpoints", modelName),
  name_prefix=f"chkpt",
)

agent = PPO('MlpPolicy', env, verbose=1, tensorboard_log=os.path.join('logs', modelName))
agent.learn(n_steps, callback=checkpoint_callback, tb_log_name="train_logs")
agent.save(os.path.join('models', modelName))