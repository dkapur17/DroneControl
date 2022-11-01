from TD3 import TD3
import gym

env = gym.make('Pendulum-v1')

agent = TD3(env)
rewards, critic_losses, actor_losses = agent.learn(verbose=True)
