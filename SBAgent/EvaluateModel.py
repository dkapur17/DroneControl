import sys
sys.path.append("..")

from envs.utils.EnvBuilder import EnvBuilder
from stable_baselines3 import PPO
from tqdm import tqdm

config_name = "v1"
model_name = "baseline"

env = EnvBuilder(f'../configs/{config_name}.json', gui=True)
agent = PPO.load(f'models/{model_name}')

totalTrials = 10
successfulTrials = 0
rewards = []
durations = []
for i in tqdm(range(totalTrials)):

    done = False
    episodeReward = 0
    episodeDuration = 0
    obs = env.reset()
    while not done:
        episodeDuration += 1
        action, _ = agent.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        episodeReward += reward

    if info['success']:
        successfulTrials += 1
    
    rewards.append(episodeReward)
    durations.append(episodeDuration)

env.close()


print(f"---------------------------------------------------------")
print(f"EVALUATION STATISTICS")
print()
print(f"Success Rate: {successfulTrials/totalTrials * 100:.2f}%")
print(f"Mean Reward: {sum(rewards)/len(rewards):.2f}")
print(f"Minimum Reward: {min(rewards):.2f}")
print(f"Maximium Reward: {max(rewards):.2f}")
print(f"Mean Episode Duration: {sum(durations)/len(durations):.2f} steps")
print(f"Shortest Episode: {min(durations)} steps")
print(f"Longest Episode: {max(durations)} steps")
print(f"---------------------------------------------------------")
