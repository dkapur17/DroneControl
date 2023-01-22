import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.utils.EnvBuilder import EnvBuilder

config_name = "v1"
input_model_name = "baseline"
output_model_name = "finetuned"
n_steps = 1_000_000

env = EnvBuilder.buildEnvFromConfig(f'../configs/{config_name}.json', gui=False)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"{output_model_name}",
)

agent = PPO.load(f'models/{input_model_name}')
agent.learn(n_steps, callback=checkpoint_callback)
agent.save(f'models/{output_model_name}')