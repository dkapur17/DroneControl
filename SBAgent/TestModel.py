import sys
sys.path.append("..")

from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt
from envs.utils.EnvBuilder import EnvBuilder

config_name = "v1"
model_name = "baseline"

env = EnvBuilder.buildEnvFromConfig(f'../configs/{config_name}.json', gui=True)

agent = PPO.load(f'models/{model_name}')

done = False
rewards = []
states = []
obs = env.reset()
states.append(np.linalg.norm(obs))
while not done:
    action, _state = agent.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    states.append(np.linalg.norm(obs))
    rewards.append(reward)
env.close()

plt.plot(range(len(states)), states)
plt.title("Distance to target")
plt.show()
plt.plot(range(len(rewards)), rewards)
plt.title("Reward")
plt.show()
