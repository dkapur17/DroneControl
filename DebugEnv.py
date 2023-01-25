import sys

import matplotlib.pyplot as plt
import numpy as np
from envs.utils.EnvBuilder import EnvBuilder

env = EnvBuilder.buildEnvFromConfig('configs/v1.json', gui=True)

for _ in range(3):
    done = False
    obs = env.reset()
    ep_len = 0
    xPos = []
    while not done:
        ep_len += 1
        obs, rew, done, info = env.step(np.array([np.random.uniform(0.5, 1), np.random.normal(0, 1), 0.5]))
        print(obs.shape)
        xPos.append(obs[0])
    print(f"Episode Length: {ep_len}")

    plt.title("Drone X Position")
    plt.plot(range(len(env.denoiseEngine.observedHistory)), [x[0] for x in env.denoiseEngine.observedHistory])
    plt.plot(range(len(env.denoiseEngine.denoisedHistory)), [x[0] for x in env.denoiseEngine.denoisedHistory])
    plt.legend(["Original", "Denoised"])
    plt.show()