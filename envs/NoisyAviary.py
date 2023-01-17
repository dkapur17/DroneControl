import gym
import numpy as np
from envs.Denoise import KFDenoiser, LPFDenoiser

class NoiseWrapper2(gym.Wrapper):
    def __init__(self, env, noise_mean=0, noise_stddev=0.01, denoiser=None, reward_mech=None):
        super().__init__(env)

        self.noise_mean = noise_mean
        self.noise_stddev = noise_stddev

        self.denoiser = denoiser

        self.prev_final_pos = None
        self.prev_noisy_pos = None
        self.prev_action = None

        self.reward_mech = reward_mech

    def reset(self):
        self.prev_final_pos = None
        self.prev_noisy_pos = None
        self.prev_action =  None
        if self.denoiser is not None:
            self.denoiser.reset()
        return self.env.reset()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        # print("orig_reward", reward)
        # adding noise to observation
        pos_xyz = self.env._getDroneStateVector(0)[:3]
        pos = pos_xyz[:2]
        pos_z = pos_xyz[2]
        # print("pos", pos)
        noise = np.random.normal(loc=self.noise_mean, scale=self.noise_stddev, size=pos.shape)
        # noise[2] = 0 # no noise on z direction  
        noisy_pos = pos + noise

        # print("noisy_pos", noisy_pos)


        if self.denoiser is None:
            final_pos = noisy_pos
        
        else:
            if self.prev_final_pos is None:
                self.denoiser.initiate(noisy_pos)
                final_pos = noisy_pos
            else:
                if isinstance(self.denoiser, KFDenoiser):
                    final_pos = self.denoiser.denoise(self.prev_final_pos, self.prev_noisy_pos, self.prev_action, action, noisy_pos)
                elif isinstance(self.denoiser, LPFDenoiser):
                    final_pos = self.denoiser.denoise(self.prev_final_pos, self.prev_noisy_pos, noisy_pos)
                else:
                    print("unknown denoioser")
                    exit(0)

        self.prev_final_pos = final_pos
        self.prev_noisy_pos = noisy_pos
        self.prev_action = action

        # print("final_pos", final_pos)

        final_pos = np.concatenate((final_pos, [pos_z]))
        final_obs = self.env._computeObs(final_pos)
        # print(self.denoiser.mu, self.denoiser.sigma)
        
        if self.reward_mech == "UT":
            reward = self.unscented_transform(self.denoiser.mu, self.denoiser.sigma, pos_z)
        elif self.reward_mech == "RewardFromDenoisedState":
            reward = self.env._computeReward(final_pos)
        elif self.reward_mech == None:
            reward = reward
        else:
            print("unkown reward calculation mechanism")
            exit(0)

        # print("final_obs", final_obs)
        # print("reward", reward, end="\n\n\n")

        
        return final_obs, reward, done, info
    
    def unscented_transform(self, mean, cov, pos_z, alpha=0.5, beta=2.0, kappa=3.0):
        n = mean.shape[0]
        #smaller alpha, closer the points are to the mean
        lambda_ = alpha**2 * (n + kappa) - n
        # print(lambda_)
        sigma_points = np.zeros((2*n+1, n))
        # print(sigma_points.shape)
        
        weights_mean = np.zeros(2*n+1)
        weights_cov = np.zeros(2*n+1)
        weights_mean[0] = lambda_/(n+lambda_)
        weights_cov[0] = weights_mean[0]+(1-alpha**2+beta)

        for i in range(1, 2*n+1):
            weights_mean[i] = 1/(2*(n+lambda_))
            weights_cov[i] = weights_mean[i]
        # print(cov)
        # print(n,lambda_,n + lambda_)
        sigma_points[0] = mean
        # print("mat", (n + lambda_)*cov)
        # print(np.linalg.eigvals((n + lambda_)*cov))
        chol = np.linalg.cholesky((n + lambda_)*cov)
        for i in range(n):
            sigma_points[i+1] = mean + chol[i]
            sigma_points[i+n+1] = mean - chol[i]

        # propagate sigma points through system function
        sigma_points_h = np.array([self.env._computeReward(np.concatenate((x, [pos_z]))) for x in sigma_points])

        # compute new mean and covariance
        mean_h = np.dot(weights_mean, sigma_points_h)
        # mean_h = np.sum(weights_mean[:, np.newaxis] * sigma_points_h, axis=0)
        # mean_h = np.mean(sigma_points_h, axis=0)
        cov_h = np.zeros_like(cov)
        for i in range(2*n + 1):
            cov_h += weights_cov[i] * np.dot((sigma_points_h[i] - mean_h), (sigma_points_h[i] - mean_h).T)
        # cov_h = np.cov(sigma_points_h.T, bias=True)

        return mean_h #, cov_h, sigma_points_h
