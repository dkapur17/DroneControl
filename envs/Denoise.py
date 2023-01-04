import numpy as np


class KFDenoiser:
    def __init__(self, state_size, action_size, process_noise, measurement_noise) -> None:
        self.mu = np.zeros(state_size)
        self.sigma = np.zeros((state_size, state_size))

        # KF matrices
        self.A = np.eye(state_size)
        self.B = np.array((state_size, action_size))
        self.C = np.eye(state_size)

        # Noise covariance matrices
        self.R = np.eye(state_size) * process_noise
        self.Q = np.eye(state_size) * measurement_noise


    def initiate(self, obs):
        self.mu = obs

    def reset(self):
        self.mu = np.zeros_like(self.mu)
        self.sigma = np.zeros_like(self.sigma)


    def denoise(self, prev_final_obs, prev_noisy_obs, prev_action, cur_action, cur_noisy_obs):
        # prediction
        mu_bar = self.A @ self.mu + self.B @ cur_action
        sigma_bar = self.A @ self.sigma @ self.A.T + self.R

        # correction
        K = sigma_bar @ self.C.T @ np.linalg.inv(self.C @ sigma_bar @ self.C.T + self.Q)
        self.mu = mu_bar + K * (cur_noisy_obs - self.C @ mu_bar)
        self.sigma = (1 - K * self.C) @ sigma_bar

        return self.mu

        
      
class LPFDenoiser:
    def __init__(self) -> None:
        cutoff_freq=0.05
        control_freq=48
        a=2*np.pi*cutoff_freq
        aT=(1/control_freq)*a 
    
    def initiate(self, obs):
        pass

    def reset(self):
        pass

    def denoise(self, prev_final_obs, prev_noisy_obs, cur_noisy_obs):
        yf= (((2-self.aT)/(2+self.aT))*prev_final_obs) + ((self.aT/(2+self.aT))*(cur_noisy_obs + prev_noisy_obs))
        return yf

