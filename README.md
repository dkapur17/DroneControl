# DroneControl

Code base for simulation and practical experimentation for autonomous drone obstacle avoidance with noise injection.

## Component Interactions

```mermaid
flowchart LR

%% Define all node components
subgraph NoiseWrapper
subgraph Environment
step["step()"]
stateProcessor["_computeProcessedState()"]
end
noiseGenerator["Noise Generator"]
denoiseEngine["Denoise Engine"]
end

policy["Policy"]

%% Define all connections
step -->|Raw State|noiseGenerator
noiseGenerator -->|Noisy Raw State|denoiseEngine
denoiseEngine -->|Denoised Raw State|stateProcessor
stateProcessor -->|Observation| policy
step -->|Reward| policy
policy -->|Action| denoiseEngine
policy -->|Action| step
```

## Designing an Experiment

An experiment has 2 parts:

1. Training phase: Choose an environment config to train a new agent on, and choose a model name to save the agent as after training.

2. Evaluation phase: Choose the model to evaluate, and the environment to evaluate it on. Notice that the environment that you evaluate the model on doesn't necessarily have to be the same as the one you trained it on.

To make an experiment, make a new config JSON in the `experimentConfigs/` directory. It should have the following shape:

```json
{
    "name": str,
    "trainParameters": {
        "config": str (Only the name of the config file. Must be in the configs directory),
        "outputModelName": str (base/finetuned + name of model. Must be in the SBAgent/models directory.)
    },
    "evaluationParameters": {
        "config": str (Only the name of the config file. Must be in the configs directory),
        "inputModelName": str (base/finetuned + name of model. Must be in the SBAgent/models directory.)
    }
}
```

Check out [experiment1.json](./experimentConfigs/experiment1.json) for reference.

From here, you do one of two things:

1. Train Step: Run `TrainDispatcher.py` to the model on the given environment. The script is written to dispatch a batch job on IIIT-H's HPC cluster, or on your local machine with the `--local` flag.

2. Evaluation Step: Run `SBAgent/EvaluateExperiment.py` to evaluate the model in the given environment.

Both these scripts take the experiment config file location as an argument.

## Making an environment config

To make an environment configuration, create a JSON in the `configs` directory of the following shape:

```json
{
    "xmin": float,
    "xmax": float,
    "ymin": float,
    "ymax": float,
    "zmin": float,
    "zmax": float,
    "provideFixedObstacles": bool,
    "obstacles": List[List[3]] or null,
    "minObstacles": int,
    "maxObstacles": int,
    "randomizeObstaclesEveryEpisode": bool,
    "fixedAltitude": bool,
    "episodeLength": int,
    "showDebugLines": bool,
    "randomizeDronePosition": bool,
    "simFreq": int,
    "controlFreq": int,
    "noiseParameters": {
        "mu": float,
        "sigma": float,
        "denoiseEngine": DenoiseEngineData
    }
}
```
### `DenoiseEngineData`

The following Denoise methods exist and the ways to add them into the experiment configuration:

#### 1. No Denoiser

To use no denoiser, just set `"denoiseEngine"` in the config JSON to `null`.

#### 2. Low Pass Filter

To use a Low Pass Filter as the Denoise Engine, set `"denoiseEngine"` to the following:

```JSON
{
    ...
    "denoiseEngine": {
        "method": "lpf",
        "parameters": {
            "order": int,
            "criticalFreq": float,
            "ftype": string
        }
    }
}
```

* `order`: Order of the filter. Can be thought of as the window size to consider while denoising the current observation.

* `criticalFreq`: Critical frequency of the underlying data. If you don't know what it means, just set it to `2`.

* `ftype`: Type of IIR to design. Options are `"bessel"` for Bessel/Thomson and `"butter"`, for Butterworth.

#### 3. Kalman Filter

To use a Kalman Filter as the Denoise Engine, set `"denoiseEngine"` to the following:

```JSON
{
    ...
    "denoiseEngine": {
        "method": "kf",
        "parameters": {
            "processNoise": float
        }
    }
}
```

* `processNoise`: Standard Deviation of the process noise.


## The Scripts

### `TrainDispatcher.py`

Used to perform the train phase of a given experiment. To run it, run:

```bash
python TrainDispatcher.py [-h] [-s STEPS] [--local] experimentConfigFile
```

* `experimentConfigFile` is path to the experiment configuration file.
* `-s` to specify the number of timesteps to train for. Defaults to 2,000,000.
* Add the `--local` flag to run the training on your local machine. If this flag is omitted, the script generates a batch job configuration and dispatches it on one of the nodes on IIIT-H's HPC.

### `SBAgent/EvaluateExperiment.py`

Used to perform the evaluation phase of a given experiment. To run it, run:

```bash
cd SBAgent
python EvaluateExperiment.py [-h] [-t TRIALS] [--gui] [--no-gui] experimentConfigFile
```

* `experimentConfigFile` is path to the experiment configuration file
* `-t` to specify the number of episodes used for evaluation. Defaults to 10.
* `--gui` or `--no-gui` to specify whether or not to render the simulation. If no flag is provided, then GUI is NOT launched by default.

### `SBAgent/EvaluateModel.py`

Used to evaluate a given model on a given environment. Allows flexibility outside of a defined experiment. To run it, run:

```bash
cd SBAgent
python EvaluateModel.py [-h] [-t TRIALS] [--gui] [--no-gui] configFileName inputModelPath
```
* `configFileName` is the name of the environment configuration file inside the `config` directory.
* `inputModelPath` is the path to the model to be evaluated.
* `-t` to specify the number of episodes used for evaluation. Defaults to 10.
* `--gui` or `--no-gui` to specify whether or not to render the simulation. If no flag is provided, then GUI is NOT launched by default.

### `SBAgent/TrainModel.py`

Used to train a model on a given environment. Allows flexibity outside of a defined experiment. Used internally by `TrainDispatcher.py`.


```bash
cd SBAgent
python TrainModel.py [-h] [-s STEPS] configFileName outputModelName
```

* `configFileName` is the name of the environment configuration file inside the `config` directory.
* `outputModelName` is the name to save the output model as. This must begin with either `base/` or `finetuned/` (for the current script it is should ideally always be `base/`) followed by the name of the model. The trained model is then saved in `SBAgent/models/<outputModelName>`.
* `-s` to specify the number of timesteps to train for. Default is 2,000,000.

## Evironment Configurations

Check out [ConfigLogs.md](./configs/ConfigLogs.md) for the description for every environement.

## Models

Check out [base/ModelLogs.md](./SBAgent/models/base/ModelLogs.md) for the description of every model trained from scratch.

Check out [finetuned/ModelLogs.md](./SBAgent/models/finetuned/ModelLogs.md) for the description of every model finetuned from an existing model.