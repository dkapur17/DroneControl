import numpy as np
import traceback
import argparse
import json
from stable_baselines3 import PPO
from time import time, sleep

import pybullet_data

from envs.MocapAviary import MocapAviary
from envs.utils.PositionConstraint import PositionConstraint
from envs.utils.NoiseWrapper import NoiseWrapper, LPFDenoiseEngine, KFDenoiseEngine

URI = 'radio://0/80/2M'
controlPeriod = 10 #10ms

parser = argparse.ArgumentParser()

parser.add_argument("modelPath", help="Path to the Model", type=str)
parser.add_argument("mu", help="Mean of the Noise", type=float)
parser.add_argument("sigma", help="Standard Deviation of the Noise", type=float)
parser.add_argument("denoiser", help="Denoiser to Use", choices={'none', 'lpf', 'kf'}, type=str)

args = parser.parse_args()

envFile = {
    'none': f'../configs/NoDenoiserEnvFixed.json',
    'lpf': f'../configs/LPFDenoiserEnvFixed.json',
    'kf': f'../configs/KFDenoiserEnvFixed.json'
}[args.denoiser]

with open(envFile, 'r') as f:
    envConfig = json.load(f)

envConfig['noiseParameters']['mu'] = args.mu
envConfig['noiseParameters']['sigma'] = args.sigma

envConfig = argparse.Namespace(**envConfig)
geoFence = PositionConstraint(envConfig.xmin, envConfig.xmax, envConfig.ymin, envConfig.ymax, envConfig.zmin, envConfig.zmax)

coreEnv = MocapAviary(URI, geoFence, envConfig.obstacles, 0.5, controlPeriod)

noiseParameters = argparse.Namespace(**envConfig.noiseParameters)
denoiseEngineData = noiseParameters.denoiseEngine

if denoiseEngineData is not None:
    denoiseEngineData = argparse.Namespace(**denoiseEngineData)
    if denoiseEngineData.method == 'lpf':
        denoiseEngine = LPFDenoiseEngine(**denoiseEngineData.parameters, freq=envConfig.controlFreq)
    elif denoiseEngineData.method == 'kf':
        denoiseEngine = KFDenoiseEngine(noiseParameters.sigma, 1/envConfig.controlFreq, coreEnv.fixedAltitude, coreEnv.initPos, **denoiseEngineData.parameters)
    else:
        raise NotImplementedError(f"Denoise Method {denoiseEngineData.method} not implemented")
else:
    denoiseEngine = None

env = NoiseWrapper(coreEnv, envConfig.mu, envConfig.sigma, denoiseEngine)

agent = PPO.load(args.modelPath)

try:
    obs = env.reset()
    start_time = time()
    while True:
        sleep(controlPeriod/1000)
        env.render(mode='3d')
        action, _ = agent.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if done or time() - start_time > 10000:
            break

    env.close()

except Exception as e:
    print(e)
    print(traceback.format_exc())
    env.emergencyStop()
    env.close()