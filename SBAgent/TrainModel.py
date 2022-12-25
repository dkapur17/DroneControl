import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager

version = 'v2'

config = ConfigManager.loadConfig(f'../configs/{version}.json', training=True)

env = ObstacleAviary(**config)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"ppo_{version}",
)

agent = PPO('MlpPolicy', env, verbose=1)
agent.learn(10_000_000, callback=checkpoint_callback)
agent.save(f'models/ppo_{version}')
