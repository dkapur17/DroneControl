import numpy as np


class LPFDenoiser:
    def __init__(self) -> None:
        # cutoff_freq=0.07
        control_freq=48
        # a=2*np.pi*cutoff_freq
        # self.aT=(1/control_freq)*a
        # self.aT=(1/control_freq)*a 
        self.aT=4/18 
    
    def initiate(self, obs):
        pass

    def reset(self):
        pass

    def denoise(self, prev_final_obs, prev_noisy_obs, cur_noisy_obs):
        yf= (((2-self.aT)/(2+self.aT))*prev_final_obs) + ((self.aT/(2+self.aT))*(cur_noisy_obs + prev_noisy_obs))
        return yf

# TODO
class KFDenoiser:
    def __init__(self, measurement_noise, freq=48, process_noise=0.01, state_size=5, action_size=2) -> None:
        self.mu = np.zeros(state_size)
        self.sigma = np.zeros((state_size, state_size))

        # KF matrices
        self.A = np.eye(state_size)
        self.B = np.zeros((state_size, action_size))
        self.B[0][0] = self.B[1][1] = self.B[2][0] = self.B[3][1] = -1 / freq
        self.C = np.eye(state_size)

        # Noise covariance matrices
        self.R = np.eye(state_size) * process_noise
        self.Q = np.eye(state_size) * measurement_noise

        self.action_size = action_size


    def initiate(self, obs):
        self.mu = obs

    def reset(self):
        self.mu = np.zeros_like(self.mu)
        self.sigma = np.zeros_like(self.sigma)
        # self.sigma = self.Q.copy()



    def denoise(self, prev_final_obs, prev_noisy_obs, prev_action, cur_action, cur_noisy_obs):
        print("Mu: ", self.mu)
        print("Sigma: ", self.sigma)
        pa = prev_action[:-1] * prev_action[-1]
        ca = cur_action[:-1] * cur_action[-1]

        # prediction
        mu_bar = self.A @ self.mu + self.B @ ca
        sigma_bar = self.A @ self.sigma @ self.A.T + self.R

        print("Mu_bar: ", mu_bar)
        print("Sigma_bar: ", sigma_bar)


        # correction
        K = sigma_bar @ self.C.T @ np.linalg.pinv(self.C @ sigma_bar @ self.C.T + self.Q)
        self.mu = mu_bar + K @ (cur_noisy_obs - self.C @ mu_bar)
        self.sigma = (1 - K @ self.C) @ sigma_bar

        print("K: ",K)
        print("Mu denoise: ", self.mu)
        print("Sigma denoise: ", self.sigma)

        return self.mu

        