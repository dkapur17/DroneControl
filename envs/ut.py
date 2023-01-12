import numpy as np

def unscented_transform(mean, cov, h, alpha=0.01, beta=2.0, kappa=0.0):
    n = mean.shape[0]
    #smaller alpha, closer the points are to the mean
    lambda_ = alpha**2 * (n + kappa) - n
    print(lambda_)
    sigma_points = np.zeros((2*n+1, n))
    print(sigma_points.shape)
    
    weights_mean = np.zeros(2*n+1)
    weights_cov = np.zeros(2*n+1)
    weights_mean[0] = lambda_/(n+lambda_)
    weights_cov[0] = weights_mean[0]+(1-alpha**2+beta)

    for i in range(1, 2*n+1):
        weights_mean[i] = 1/(2*(n+lambda_))
        weights_cov[i] = weights_mean[i]
    
    sigma_points[0] = mean
    chol = np.linalg.cholesky((n + lambda_)*cov)
    for i in range(n):
        sigma_points[i+1] = mean + chol[i]
        sigma_points[i+n+1] = mean - chol[i]

    # propagate sigma points through system function
    sigma_points_h = np.array([h(x) for x in sigma_points])

    # compute new mean and covariance
    print(sigma_points)
    print(weights_mean)
    print(sigma_points_h)
    mean_h = np.dot(weights_mean, sigma_points_h)
    print(mean_h)
    # mean_h = np.sum(weights_mean[:, np.newaxis] * sigma_points_h, axis=0)
    # mean_h = np.mean(sigma_points_h, axis=0)
    cov_h = np.zeros_like(cov)
    for i in range(2*n + 1):
        cov_h += weights_cov[i] * np.dot((sigma_points_h[i] - mean_h), (sigma_points_h[i] - mean_h).T)
    # cov_h = np.cov(sigma_points_h.T, bias=True)

    return mean_h, cov_h, sigma_points_h


mean = np.array([1.0, 2.0])
cov = np.array([[0.1, 0], [0, 0.1]])

def h(x):
    return x[0]**2 + x[1]**2

mean_h, cov_h, sigma_points_h = unscented_transform(mean, cov, h)
print(mean_h)
print(cov_h)
print(sigma_points_h)