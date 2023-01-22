import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.utils.EnvBuilder import EnvBuilder

config_name = "baseline"
model_name = "baseline"
n_steps = 10_000_000


env = EnvBuilder.buildEnvFromConfig(f'../configs/{config_name}.json', gui=False)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"{model_name}",
)

agent = PPO('MlpPolicy', env, verbose=1)
agent.learn(n_steps, callback=checkpoint_callback)
agent.save(f'models/{model_name}')
