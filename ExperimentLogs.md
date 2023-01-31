# Experiment Logs

## [Experiment 1](./experimentConfigs/experiment1.json)

Train without noise and denoiser. Evaluate without noise and denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v1.json`](./configs/v1.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

<!-- 
| Metric                     | Value   |
|----------------------------|---------|
| Success Rate               | 73.50%  |
| Collision Rate             | 26.50%  |
| Mean Incompletion Distance | N/A     |
| Mean Reward                | -20.25  |
| Mean Episode Length        | 261.744 | 
-->


| Metric                     | Value   |
|----------------------------|---------|
| Success Rate               | 71.50%  |
| Collision Rate             | 28.50%  |
| Mean Incompletion Distance | N/A     |
| Mean Reward                | -50.37  |
| Mean Episode Length        | 256.19  |

---
## [Experiment 2A](./experimentConfigs/experiment2a.json)

Train without noise and denoiser. Evaluate with noise (0.01) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

| Metric                     | Value   |
|----------------------------|---------|
| Success Rate               | 71.00%  |
| Collision Rate             | 29.00%  |
| Mean Incompletion Distance | N/A     |
| Mean Reward                | -67.18  |
| Mean Episode Length        | 259.582 |

---
## [Experiment 2B](./experimentConfigs/experiment2b.json)

Train without noise and denoiser. Evaluate with noise (0.05) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

| Metric                     | Value   |
|----------------------------|---------|
| Success Rate               | 70.20%  |
| Collision Rate             | 29.80%  |
| Mean Incompletion Distance | N/A     |
| Mean Reward                | -83.37  |
| Mean Episode Length        | 259.929 |

---
## [Experiment 2C](./experimentConfigs/experiment2c.json)

Train without noise and denoiser. Evaluate with noise (0.1) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3A](./experimentConfigs/experiment3a.json)

Train without noise and denoiser. Evaluate with both noise (0.01) and denoiser(LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3B](./experimentConfigs/experiment3b.json)

Train without noise and denoiser. Evaluate with both noise (0.05) and denoiser (LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3C]((./experimentConfigs/experiment3c.json))

Train without noise and denoiser. Evaluate with both noise (0.1) and denoiser (LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3D]((./experimentConfigs/experiment3d.json))

Train without noise and denoiser. Evaluate with both noise (0.01) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3E](./experimentConfigs/experiment3e.json)

Train without noise and denoiser. Evaluate with both noise (0.05) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 3F](./experimentConfigs/experiment3f.json)

Train without noise and denoiser. Evaluate with both noise (0.1) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1)

### Evaluation Parameters

* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1)

#### Evaluation Results

*TBD*

---

## [Experiment 4A](./experimentConfigs/experiment4a.json)

Train with noise (0.01) but no denoiser. Evaluate with noise (0.01) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Output Model: [`base/model2_0.01`](./SBAgent/models/base/model2_0.01)

### Evaluation Parameters

* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Input Model: [`base/model2_0.01`](./SBAgent/models/base/model2_0.01)

#### Evaluation Results

*TBD*

---

## [Experiment 4B](./experimentConfigs/experiment4b.json)

Train with noise (0.05) but no denoiser. Evaluate with noise (0.05) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Output Model: [`base/model2_0.05`](./SBAgent/models/base/model2_0.05)

### Evaluation Parameters

* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Input Model: [`base/model2_0.05`](./SBAgent/models/base/model2_0.05)

#### Evaluation Results

*TBD*

---

## [Experiment 4C](./experimentConfigs/experiment4c.json)

Train with noise (0.1) but no denoiser. Evaluate with noise (0.1) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Output Model: [`base/model2_0.1`](./SBAgent/models/base/model2_0.1)

### Evaluation Parameters

* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Input Model: [`base/model2_0.1`](./SBAgent/models/base/model2_0.1)


#### Evaluation Results

*TBD*

---

## [Experiment 5A](./experimentConfigs/experiment5a.json)

Train with both noise (0.01) and denoiser (LPF). Evaluate with both noise (0.01) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Output Model: [`base/model3_0.01_lpf`](./SBAgent/models/base/model3_0.01_lpf)

### Evaluation Parameters

* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Input Model: [`base/model3_0.01_lpf`](./SBAgent/models/base/model3_0.01_lpf)

#### Evaluation Results
*TBD*

---

## [Experiment 5B](./experimentConfigs/experiment5b.json)

Train with both noise (0.05) and denoiser (LPF). Evaluate with both noise (0.05) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Output Model: [`base/model3_0.05_lpf`](./SBAgent/models/base/model3_0.05_lpf)

### Evaluation Parameters

* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Input Model: [`base/model3_0.05_lpf`](./SBAgent/models/base/model3_0.05_lpf)

#### Evaluation Results
*TBD*

---

## [Experiment 5C](./experimentConfigs/experiment5c.json)

Train with both noise (0.1) and denoiser (LPF). Evaluate with both noise (0.1) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Output Model: [`base/model3_0.1_lpf`](./SBAgent/models/base/model3_0.1_lpf)

### Evaluation Parameters

* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Input Model: [`base/model3_0.1_lpf`](./SBAgent/models/base/model3_0.1_lpf)

#### Evaluation Results
*TBD*

---

## [Experiment 5D](./experimentConfigs/experiment5d.json)

Train with both noise (0.01) and denoiser (KF). Evaluate with both noise (0.01) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Output Model: [`base/model3_0.01_kf`](./SBAgent/models/base/model3_0.01_kf)

### Evaluation Parameters

* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Input Model: [`base/model3_0.01_kf`](./SBAgent/models/base/model3_0.01_kf)

#### Evaluation Results
*TBD*

---

## [Experiment 5E](./experimentConfigs/experiment5e.json)

Train with both noise (0.05) and denoiser (KF). Evaluate with both noise (0.05) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Output Model: [`base/model3_0.05_kf`](./SBAgent/models/base/model3_0.05_kf)

### Evaluation Parameters

* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Input Model: [`base/model3_0.05_kf`](./SBAgent/models/base/model3_0.05_kf)

#### Evaluation Results
*TBD*

---

## [Experiment 5F](./experimentConfigs/experiment5f.json)

Train with both noise (0.1) and denoiser (KF). Evaluate with both noise (0.1) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Output Model: [`base/model3_0.1_kf`](./SBAgent/models/base/model3_0.1_kf)

### Evaluation Parameters

* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Input Model: [`base/model3_0.1_kf`](./SBAgent/models/base/model3_0.1_kf)

#### Evaluation Results
*TBD*

