# Experiment Logs

## Experiment 1

Train without noise and denoiser. Evaluate without noise and denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/ConfigLogs.md#L7)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v1.json`](./configs/ConfigLogs.md#L7)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---
## Experiment 2

Train without noise and denoiser. Evaluate with noise but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/ConfigLogs.md#L7)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v2.json`](./configs/ConfigLogs.md#L16)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 3

Train without noise and denoiser. Evaluate with both noise and denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v1.json`](./configs/ConfigLogs.md#L7)
* Output Model: [`base/model1`](./SBAgent/models/base/model1.zip)

### Evaluation Parameters

* Environment Config: [`v3_lpf.json`](./configs/ConfigLogs.md#L25)
* Input Model: [`base/model1`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 4

Train with noise but no denoiser. Evaluate with noise but no denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2.json`](./configs/ConfigLogs.md#L16)
* Output Model: [`base/model2`](./SBAgent/models/base/model2.zip)

### Evaluation Parameters

* Environment Config: [`v2.json`](./configs/ConfigLogs.md#L16)
* Input Model: [`base/model2`](./SBAgent/models/base/model1.zip)

#### Evaluation Results
*TBD*

---

## Experiment 5

Train with noise but no denoiser. Evaluate with both noiser and denoiser.
### Train Parameters

* Training Type: Base
* Environment Config: [`v2.json`](./configs/ConfigLogs.md#L16)
* Output Model: [`base/model2`](./SBAgent/models/base/model2.zip)

### Evaluation Parameters

* Environment Config: [`v3_lpf.json`](./configs/ConfigLogs.md#L25)
* Input Model: [`base/model2`](./SBAgent/models/base/model2.zip)

#### Evaluation Results
*TBD*

---

## Experiment 6

Train with both noise and denoiser. Evaluate with both noise and denoiser.

* Training Type: Base
* Environment Config: [`v3_lpf.json`](./configs/ConfigLogs.md#L25)
* Output Model: [`base/model3`](./SBAgent/models/base/model3.zip)

### Evaluation Parameters

* Environment Config: [`v3_lpf.json`](./configs/ConfigLogs.md#L25)
* Input Model: [`base/model3`](./SBAgent/models/base/model3.zip)

#### Evaluation Results
*TBD*