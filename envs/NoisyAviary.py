import gym
import numpy as np

class NoiseWrapper1(gym.ObservationWrapper):
    def __init__(self, env, noise_mean=0, noise_stddev=0.01, denoiser=None):
        super().__init__(env)
        self.observation_space = env._observationSpace()

        self.noise_mean = noise_mean
        self.noise_stddev = noise_stddev

        self.denoiser = denoiser

        self.prev_final_obs = None
        self.prev_noisy_obs = None
        self.env = env


    def reset(self):
        self.prev_final_obs = None
        self.prev_noisy_obs = None
        if self.denoiser is not None:
            self.denoiser.reset()
        return self.env.reset()


    def observation(self, obs):
        noisy_obs = obs + np.random.normal(loc=self.noise_mean, scale=self.noise_stddev, size=obs.shape)

        if self.denoiser is None:
            final_obs = noisy_obs
        else:
            if self.prev_final_obs is None:
                self.denoiser.initiate(noisy_obs)
                final_obs = noisy_obs
            else:
                final_obs = self.denoiser.denoise(self.prev_final_obs, self.prev_noisy_obs, noisy_obs)

        self.prev_final_obs = final_obs
        self.prev_noisy_obs = noisy_obs
        return final_obs


# TODO
class NoiseWrapper2(gym.Wrapper):
    def __init__(self, env, noise_mean=0, noise_stddev=0.01, denoiser=None):
        super().__init__(env)

        self.noise_mean = noise_mean
        self.noise_stddev = noise_stddev

        self.denoiser = denoiser

        self.prev_final_obs = None
        self.prev_noisy_obs = None
        self.prev_action = None

    def reset(self):
        self.prev_final_obs = None
        self.prev_noisy_obs = None
        self.prev_action =  None
        if self.denoiser is not None:
            self.denoiser.reset()
        return self.env.reset()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        # adding noise to observation
        print("OBS", obs)
        print("prev_final_obs", self.prev_final_obs)
        print("curr_action", action)
        noisy_obs = obs + np.random.normal(loc=self.noise_mean, scale=self.noise_stddev, size=obs.shape)
        print("Noisy OBS",noisy_obs)
        # denoise if available
        if self.denoiser is None:
            final_obs = noisy_obs
        
        else:
            if self.prev_final_obs is None:
                self.denoiser.initiate(noisy_obs)
                final_obs = noisy_obs
            else:
                final_obs = self.denoiser.denoise(self.prev_final_obs, self.prev_noisy_obs, self.prev_action, action, noisy_obs)
        print("Final OBS", final_obs, end='\n\n')    
        self.prev_final_obs = final_obs
        self.prev_noisy_obs = noisy_obs
        self.prev_action = action
        
        return final_obs, reward, done, info