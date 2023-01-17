import sys
sys.path.append("..")

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from envs.ObstacleAviary import ObstacleAviary
from envs.utils import ConfigManager
from envs.NoisyAviary import NoiseWrapper2
from envs.Denoise import KFDenoiser, LPFDenoiser

version='v1_practical2'


config = ConfigManager.loadConfig(f'../configs/{version}.json', training=True)

# denoiser = KFDenoiser(measurement_noise=0.1)

config_noise = config["noise"]
config_mean = config["mean"]
config_std_dev = config["std_dev"]
config_denoiser = config["denoiser"]
config_measurement_noise = config["measurement_noise"]

del config["noise"]
del config["mean"]
del config["std_dev"]
del config["denoiser"]
del config["measurement_noise"]


if config_noise == False:
    env = ObstacleAviary(**config)
else:
  if config_denoiser=="None":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=None)
  if config_denoiser=="LPFDenoiser":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=LPFDenoiser())
  elif config_denoiser=="KFDenoiser":
    env = NoiseWrapper2(env=ObstacleAviary(**config), noise_mean=config_mean, noise_stddev=config_std_dev, denoiser=KFDenoiser(measurement_noise=config_measurement_noise), reward_mech=None)


checkpoint_callback = CheckpointCallback(
  save_freq=1000000,
  save_path="logs",
  name_prefix=f"ppo_{version}",
)

agent = PPO('MlpPolicy', env, verbose=1)
agent.learn(10_000_000, callback=checkpoint_callback)
agent.save(f'models/ppo_{version}')
