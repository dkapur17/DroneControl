import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from envs.NoisyAviary import NoisyObservation, NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser

version = 'v1'

config = ConfigManager.loadConfig(f'../configs/{version}.json', training=True)

denoiser = LPFDenoiser()

# env = NoiseWrapper2(ObstacleAviary(**config), noise_mean=0, noise_stddev=0.01)
env = NoisyObservation(ObstacleAviary(**config), noise_mean=0, noise_stddev=0.01)

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"ppo_{version}",
)

agent = PPO('MlpPolicy', env, verbose=1)
agent.learn(10_000_000, callback=checkpoint_callback)
agent.save(f'models/ppo_{version}')
