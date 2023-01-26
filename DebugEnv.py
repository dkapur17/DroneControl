import matplotlib.pyplot as plt
import numpy as np
from envs.utils.EnvBuilder import EnvBuilder
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("configFileName", help="Name (and only the name) of the environment configuration file", type=str)
args = parser.parse_args()

env = EnvBuilder.buildEnvFromConfig(f'configs/{args.configFileName}', gui=True)

print(env.observation_space.shape)
print(env.observation_space.sample())

for _ in range(3):
    done = False
    obs = env.reset()
    ep_len = 0
    xPos = []
    while not done:
        ep_len += 1
        obs, rew, done, info = env.step(np.array([np.random.uniform(-0.5, 1), np.random.normal(0, 1), 0.5]))
        xPos.append(obs[0])
    print(f"Episode Length: {ep_len}")

    if env.denoiseEngine is not None:
        plt.title("Drone X Position")
        plt.plot(range(len(env.denoiseEngine.observedHistory)), [x[0] for x in env.denoiseEngine.observedHistory])
        plt.plot(range(len(env.denoiseEngine.denoisedHistory)), [x[0] for x in env.denoiseEngine.denoisedHistory])
        plt.legend(["Original", "Denoised"])
        plt.show()