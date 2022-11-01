import numpy as np
import pybullet as p

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.single_agent_rl.BaseSingleAgentAviary import BaseSingleAgentAviary, ActionType, ObservationType
from gym import spaces

from .utils import PositionConstraint

class TargetAviary(BaseSingleAgentAviary):

    def __init__(self,
                 geoFence:PositionConstraint,
                 episodeLength:int=1500,
                 showGeoFence:bool=False,
                 showTrajectory:bool=False,
                 gui:bool=False,
                 freq=240,
                 aggregate_phy_steps=1,
                 actionType:ActionType=ActionType.VEL,
                 record=False
                ):

        super().__init__(drone_model=DroneModel.CF2X,
                         initial_xyzs=np.array([[0, 0, 1]]),
                         initial_rpys=np.array([[0, 0, 0]]),
                         physics=Physics.PYB,
                         freq=freq,
                         aggregate_phy_steps=aggregate_phy_steps,
                         gui=gui,
                         record=record,
                         obs=ObservationType.KIN,
                         act=actionType
                         )
        
        self.geoFence = geoFence
        self.showGeoFence = showGeoFence
        self.showTrajectory = showTrajectory

        self.trajectory = []

        self.targetPosition = None
        self.targetId = None

        self.episodeLength = episodeLength
        self.timestepCounter = 0

        self.lastVelocity = None
        self.currVelocity = np.array([0, 0, 0])


    def _observationSpace(self):        
        # OBS = (dx, dy, dz)
        obs_lower_bound = np.array([-np.inf, -np.inf, -np.inf])
        obs_upper_bound = np.array([np.inf, np.inf, np.inf])

        return spaces.Box(low=obs_lower_bound, high=obs_upper_bound, dtype=np.float32)

    def _computeObs(self):
        
        state = self._getDroneStateVector(0)
        pos = state[0:3]
        return self.targetPosition - pos


    def reset(self):

        self.targetPosition = self.geoFence.generateRandomPosition()
        
        super().reset()

        if self.targetId is not None:
            p.removeUserDebugItem(self.targetId, physicsClientId=self.CLIENT)

        self.targetId = p.addUserDebugPoints([self.targetPosition], [np.array([0, 1, 0.5])], pointSize=10, physicsClientId=self.CLIENT)
        
        self.trajectory = []
        self.timestepCounter = 0


        if self.showGeoFence:
            self._drawGeoFence()
        
        return self._computeObs()


    def _drawGeoFence(self):

        pc = self.geoFence
        p.addUserDebugLine([pc.xmin, pc.ymin, pc.zmin], [pc.xmax, pc.ymin, pc.zmin], lineWidth=3)
        p.addUserDebugLine([pc.xmin, pc.ymin, pc.zmin], [pc.xmin, pc.ymin, pc.zmax], lineWidth=3)
        p.addUserDebugLine([pc.xmin, pc.ymin, pc.zmin], [pc.xmin, pc.ymax, pc.zmin], lineWidth=3)

        p.addUserDebugLine([pc.xmax, pc.ymin, pc.zmax], [pc.xmin, pc.ymin, pc.zmax], lineWidth=3)
        p.addUserDebugLine([pc.xmax, pc.ymin, pc.zmax], [pc.xmax, pc.ymax, pc.zmax], lineWidth=3)
        p.addUserDebugLine([pc.xmax, pc.ymin, pc.zmax], [pc.xmax, pc.ymin, pc.zmin], lineWidth=3)

        p.addUserDebugLine([pc.xmin, pc.ymax, pc.zmax], [pc.xmin, pc.ymin, pc.zmax], lineWidth=3)
        p.addUserDebugLine([pc.xmin, pc.ymax, pc.zmax], [pc.xmax, pc.ymax, pc.zmax], lineWidth=3)
        p.addUserDebugLine([pc.xmin, pc.ymax, pc.zmax], [pc.xmin, pc.ymax, pc.zmin], lineWidth=3)

        p.addUserDebugLine([pc.xmax, pc.ymax, pc.zmin], [pc.xmax, pc.ymin, pc.zmin], lineWidth=3)
        p.addUserDebugLine([pc.xmax, pc.ymax, pc.zmin], [pc.xmin, pc.ymax, pc.zmin], lineWidth=3)
        p.addUserDebugLine([pc.xmax, pc.ymax, pc.zmin], [pc.xmax, pc.ymax, pc.zmax], lineWidth=3)

        for xlim in [pc.xmin, pc.xmax]:
            for ylim in [pc.ymin, pc.ymax]:
                for zlim in [pc.zmin, pc.zmax]:
                    p.addUserDebugText(f"({xlim}, {ylim}, {zlim})", np.array([xlim, ylim, zlim]), textSize=1)

    def step(self, action):
        
        self.timestepCounter += 1
        state = self._getDroneStateVector(0)
        pos = state[0:3]
        self.trajectory.append(pos)
        if self.showTrajectory and len(self.trajectory) > 3:
            p.addUserDebugLine(self.trajectory[-2], self.trajectory[-1])

        self.lastVelocity = self.currVelocity

        if np.linalg.norm(action[0:3]) != 0:
            v_unit_vector = action[0:3] / np.linalg.norm(action[0:3])
        else:
            v_unit_vector = np.zeros(3)
        
        self.currVelocity = self.SPEED_LIMIT * np.abs(action[3]) * v_unit_vector

        return super().step(action)

    def _computeReward(self):
        state = self._getDroneStateVector(0)

        dist_to_target = np.linalg.norm(self.targetPosition - state[0:3])**2
        if dist_to_target <= 0.001:
            positionReward = 1000
        else:
            positionReward = -0.8*dist_to_target if dist_to_target > 0.1 else 1/dist_to_target

        positionReward = np.log(positionReward) if positionReward > 0 else positionReward
        
        accelerationPenalty = np.linalg.norm(self.currVelocity - self.lastVelocity)
        velocityPenalty = np.linalg.norm(self.currVelocity)

        return positionReward - 0.2*accelerationPenalty - 0.1*velocityPenalty

    def _computeDone(self):
        if self.timestepCounter >= self.episodeLength:
            return True
        return False
    
    def _computeInfo(self):
        return {}
