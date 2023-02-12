# Model Registry

## [`model1`](./model1/)

Trained with randomized obstacles, no noise and no denoiser.

**Environment Config**: [0 Mean, 0 Std, No Denoiser](../../../configs/specifics/0m_0s_none.json)

## [`model2`](./model2/)

Trained with randomized obstacles, unbiased noise with standard deviation 0.5 and no denoiser.

**Environment Config**: [0 Mean, 0.5 Std, No Denoiser](../../../configs/specifics/0m_0.5s_none.json)

## [`model3`](./model3/)

Trained with randomized obstacles, biased noise with mean 0.1 and no denoiser.

**Environment Config**: [0.1 Mean, 0 Std, No Denoiser](../../../configs/specifics/0.1m_0s_none.json)

## [`model4`](./model4/)

Trained with randomized obstacles, biased noise with mean 0.1 and standard deviation 0.5 and no denoiser.

**Environment Config**: [0.1 Mean, 0.5 Std, No Denoiser](../../../configs/specifics/0.1m_0.5s_none.json)
