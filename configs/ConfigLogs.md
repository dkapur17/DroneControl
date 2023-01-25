# Config Logs

## [`sample.json`](./sample.json)

Sample config for reference and debugging. Parameters will keep changing.

## [`v1.json`](./v1.json)

* Description: Random Obstacles, No Noise, No Denoiser
* Geofence: `[(0, 2), (-0.5, 0.5), (0, 1)]`
* Randomized Obstacles ~ `[0, 4)`
* Randomize Starting Position
* Noise: `None`
* Denoiser: `None`

## [`v2.json`](./v2.json)

* Description: Random Obstacles, Noise, No Denoiser
* Geofence: `[(0, 2), (-0.5, 0.5), (0, 1)]`
* Randomized Obstacles ~ `[0, 4)`
* Randomize Starting Position
* Noise: $\mathcal{N}(0, 0.1)$
* Denoiser: `None`

## [`v3_lpf.json`](./v3_lpf.json)

* Description: Random Obstacles, Noise, LPF Denoiser
* Geofence: `[(0, 2), (-0.5, 0.5), (0, 1)]`
* Randomized Obstacles ~ `[0, 4)`
* Randomize Starting Position
* Noise: $\mathcal{N}(0, 0.1)$
* Denoiser: `LPFDenoiseEngine(2, 2, "bessel")`

## [`v3_kf.json`](./v3_kf.json)

* Description: Random Obstacles, Noise, KF Denoiser
* Geofence: `[(0, 2), (-0.5, 0.5), (0, 1)]`
* Randomized Obstacles ~ `[0, 4)`
* Randomize Starting Position
* Noise: $\mathcal{N}(0, 0.1)$
* Denoiser: `KFDenoiser(0)`
