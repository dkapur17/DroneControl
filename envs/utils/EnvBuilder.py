import json
from argparse import Namespace

from .PositionConstraint import PositionConstraint
from ..ObstacleAviary import ObstacleAviary
from .NoiseWrapper import NoiseWrapper

from .DenoiseEngines import LPFDenoiseEngine

class EnvBuilder:

    @staticmethod
    def buildEnvFromConfig(configPath, gui=False):
        with open(configPath, 'r') as f:
            configData = json.load(f)

        configData = Namespace(**configData)
        geoFence = PositionConstraint(configData.xmin, configData.xmax, configData.ymin, configData.ymax, configData.zmin, configData.zmax)
        configData.geoFence = geoFence

        del configData.xmin
        del configData.xmax
        del configData.ymin
        del configData.ymax
        del configData.zmin
        del configData.zmax

        noiseParameters = Namespace(**configData.noiseParameters)

        denoiseEngineData = noiseParameters.denoiseEngine

        if denoiseEngineData is not None:
            denoiseEngineData = Namespace(**denoiseEngineData)
            if denoiseEngineData.method == 'lpf':
                denoiseEngine = LPFDenoiseEngine(**denoiseEngineData.parameters, freq=configData.controlFreq)
            else:
                raise NotImplementedError(f"Denoise Method {denoiseEngineData.method} not implemented")


        del configData.noiseParameters
        configData.gui = gui
        
        innerEnv = ObstacleAviary(**vars(configData))

        env = NoiseWrapper(innerEnv, noiseParameters.mu, noiseParameters.sigma, denoiseEngine)

        return env