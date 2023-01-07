import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from envs.NoisyAviary import NoiseWrapper1, NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser

# version = 'v1'
version='v5_2d_noise_0.1'

config = ConfigManager.loadConfig(f'../configs/{version}.json', training=True)
denoiser= None
# denoiser = KFDenoiser(measurement_noise=0.1)

# env = ObstacleAviary(**config)
env = NoiseWrapper1(env=ObstacleAviary(**config), noise_mean=0, noise_stddev=0.1, denoiser=denoiser)
# env = NoiseWrapper2(ObstacleAviary(**config), noise_mean=config["noise_mean"], noise_stddev=config["noise_stddev"])

checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"ppo_{version}",
)

agent = PPO('MlpPolicy', env, verbose=1)
agent.learn(10_000_000, callback=checkpoint_callback)
agent.save(f'models/ppo_{version}')
