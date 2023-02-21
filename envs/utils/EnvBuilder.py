import json
from argparse import Namespace

from .PositionConstraint import PositionConstraint
from ..ObstacleAviary import ObstacleAviary
from .NoiseWrapper import NoiseWrapper

from .DenoiseEngines import LPFDenoiseEngine, KFDenoiseEngine

class EnvBuilder:

    @staticmethod
    def buildEnvFromConfig(configPath, gui=False):
        with open(configPath, 'r') as f:
            configData = json.load(f)

        # When EnvBuilder is used, the environment is always encapsulated in the NoiseWrapper, which expects observation returned to be raw
        configData['returnRawObservations'] = True

        configData = Namespace(**configData)
        geoFence = PositionConstraint(configData.xmin, configData.xmax, configData.ymin, configData.ymax, configData.zmin, configData.zmax)
        configData.geoFence = geoFence

        del configData.xmin
        del configData.xmax
        del configData.ymin
        del configData.ymax
        del configData.zmin
        del configData.zmax

        # Save the noise parameters
        noiseParameters = Namespace(**configData.noiseParameters)

        # Delete them from config
        del configData.noiseParameters
        configData.gui = gui
        
        # Build the environment first, as some of its variables are needed in the denoise Engine
        innerEnv = ObstacleAviary(**vars(configData))

        denoiseEngineData = noiseParameters.denoiseEngine

        if denoiseEngineData is not None:
            denoiseEngineData = Namespace(**denoiseEngineData)
            if denoiseEngineData.method == 'lpf':
                denoiseEngine = LPFDenoiseEngine(**denoiseEngineData.parameters, freq=configData.controlFreq)
            elif denoiseEngineData.method == 'kf':
                denoiseEngine = KFDenoiseEngine(noiseParameters.sigma, 1/configData.controlFreq, innerEnv.fixedAltitude, innerEnv.initPos, **denoiseEngineData.parameters)
            else:
                raise NotImplementedError(f"Denoise Method {denoiseEngineData.method} not implemented")
        else:
            denoiseEngine = None

        env = NoiseWrapper(innerEnv, noiseParameters.mu, noiseParameters.sigma, denoiseEngine)

        return env