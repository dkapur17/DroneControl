# Experiment Logs

## Experiment 1

Train without noise and denoiser. Evaluate without noise and denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v1.json`](./configs/v1.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---
## Experiment 2A

Train without noise and denoiser. Evaluate with noise (0.01) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---
## Experiment 2B

Train without noise and denoiser. Evaluate with noise (0.05) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---
## Experiment 2C

Train without noise and denoiser. Evaluate with noise (0.1) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3A

Train without noise and denoiser. Evaluate with both noise (0.01) and denoiser(LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3B

Train without noise and denoiser. Evaluate with both noise (0.05) and denoiser (LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3C

Train without noise and denoiser. Evaluate with both noise (0.1) and denoiser (LPF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3D

Train without noise and denoiser. Evaluate with both noise (0.01) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3E

Train without noise and denoiser. Evaluate with both noise (0.05) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3F

Train without noise and denoiser. Evaluate with both noise (0.1) and denoiser (KF).
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/v1.json)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 4A

Train with noise (0.01) but no denoiser. Evaluate with noise (0.01) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Output Model: [`base/model2_0.01`](./SBAgent/models/base/model2_0.01.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.01.json`](./configs/v2_0.01.json)
* Input Model: [`base/model2_0.01`](./SBAgent/models/base/model2_0.01.zip)

#### Evaluation Results
*TBD*

---

## Experiment 4B

Train with noise (0.05) but no denoiser. Evaluate with noise (0.05) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Output Model: [`base/model2_0.05`](./SBAgent/models/base/model2_0.05.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.05.json`](./configs/v2_0.05.json)
* Input Model: [`base/model2_0.05`](./SBAgent/models/base/model2_0.05.zip)

#### Evaluation Results
*TBD*

---

## Experiment 4C

Train with noise (0.1) but no denoiser. Evaluate with noise (0.1) but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Output Model: [`base/model2_0.1`](./SBAgent/models/base/model2_0.1.zip)

### Evaluation Parameters

* Environment Config: [`v2_0.1.json`](./configs/v2_0.1.json)
* Input Model: [`base/model2_0.1`](./SBAgent/models/base/model2_0.1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5A

Train with both noise (0.01) and denoiser (LPF). Evaluate with both noise (0.01) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Output Model: [`base/model3_0.01_lpf`](./SBAgent/models/base/model3_0.01_lpf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.01_lpf.json`](./configs/v3_0.01_lpf.json)
* Input Model: [`base/model3_0.01_lpf`](./SBAgent/models/base/model3_0.01_lpf.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5B

Train with both noise (0.05) and denoiser (LPF). Evaluate with both noise (0.05) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Output Model: [`base/model3_0.05_lpf`](./SBAgent/models/base/model3_0.05_lpf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.05_lpf.json`](./configs/v3_0.05_lpf.json)
* Input Model: [`base/model3_0.05_lpf`](./SBAgent/models/base/model3_0.05_lpf.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5C

Train with both noise (0.1) and denoiser (LPF). Evaluate with both noise (0.1) and denoiser (LPF).

* Training Type: Base
* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Output Model: [`base/model3_0.1_lpf`](./SBAgent/models/base/model3_0.1_lpf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.1_lpf.json`](./configs/v3_0.1_lpf.json)
* Input Model: [`base/model3_0.1_lpf`](./SBAgent/models/base/model3_0.1_lpf.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5D

Train with both noise (0.01) and denoiser (KF). Evaluate with both noise (0.01) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Output Model: [`base/model3_0.01_kf`](./SBAgent/models/base/model3_0.01_kf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.01_kf.json`](./configs/v3_0.01_kf.json)
* Input Model: [`base/model3_0.01_kf`](./SBAgent/models/base/model3_0.01_kf.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5E

Train with both noise (0.05) and denoiser (KF). Evaluate with both noise (0.05) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Output Model: [`base/model3_0.05_kf`](./SBAgent/models/base/model3_0.05_kf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.05_kf.json`](./configs/v3_0.05_kf.json)
* Input Model: [`base/model3_0.05_kf`](./SBAgent/models/base/model3_0.05_kf.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5F

Train with both noise (0.1) and denoiser (KF). Evaluate with both noise (0.1) and denoiser (KF).

* Training Type: Base
* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Output Model: [`base/model3_0.1_kf`](./SBAgent/models/base/model3_0.1_kf.zip)

### Evaluation Parameters

* Environment Config: [`v3_0.1_kf.json`](./configs/v3_0.1_kf.json)
* Input Model: [`base/model3_0.1_kf`](./SBAgent/models/base/model3_0.1_kf.zip)

#### Evaluation Results
*TBD*

