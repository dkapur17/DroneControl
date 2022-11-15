import numpy as np
import pybullet as p
import pybullet_data

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.single_agent_rl.BaseSingleAgentAviary import BaseSingleAgentAviary, ActionType, ObservationType
from gym import spaces
import inspect

from .utils import PositionConstraint

class ObstacleAviary(BaseSingleAgentAviary):

    def __init__(self,
                 geoFence:PositionConstraint,
                 nObstacles:int=1,
                 episodeLength:int=1500,
                 showGeoFence:bool=False,
                 showTrajectory:bool=False,
                 gui:bool=False,
                 freq=240,
                 aggregate_phy_steps=1,
                 actionType:ActionType=ActionType.VEL,
                 record=False,
                 lab_configuration=False,
                ):

        self.nObstacles = nObstacles
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

        self.obstacles = []
        self.obstacleScalingFactor = 3
        self.obstacleRadius = 0.03 # Radius from URDF
        self.obstacleRadius = self.obstacleScalingFactor * self.obstacleRadius
        
        self.hasCollided = False
        self.allowableObstacleProximity = 0.5
        self.labConfiguration = lab_configuration

    def _observationSpace(self):

        # OBS = (dxt, dyt, dzt, dxo, dyo, dzo)
        # Distance to target and distance to closest obstacle from current position
        obs_lower_bound = np.array([-np.inf, -np.inf, -np.inf] * (2 if self.nObstacles else 1))
        obs_upper_bound = np.array([np.inf, np.inf, np.inf] * (2 if self.nObstacles else 1))

        return spaces.Box(low=obs_lower_bound, high=obs_upper_bound, dtype=np.float32)


    def _computeObs(self):

        state = self._getDroneStateVector(0)
        pos = state[0:3]


        # For prematrue call to super().reset(), will call _computeObs again later
        try:
            targetOffset = self.targetPosition - pos
        except:
            return None

        if self.nObstacles:
            closestObstacleOffset = self._getClosestObstacleOffset()
            obsList = [targetOffset, closestObstacleOffset]
        else:
            obsList = [targetOffset]
        return np.concatenate(obsList)

    def _getClosestObstacleOffset(self):

        state = self._getDroneStateVector(0)
        pos = state[0:3]
        # Get offsets to all obstacles
        obstacleOffset = [p.getClosestPoints(self.getDroneIds()[0], obstacle, distance=10000)[0][6] - pos for obstacle in self.obstacles]
        # Sort by increasing magnitutde of vectors and keep the smallest one
        closestObstacleOffset = sorted(obstacleOffset, key=lambda x: np.linalg.norm(x))[0]

        return closestObstacleOffset

    def reset(self):

        self.hasCollided = False
        self.trajectory = []
        self.timestepCounter = 0

        # Call only required functions from super().reset()
        p.resetSimulation(physicsClientId=self.CLIENT)
        self._housekeeping()
        self._updateAndStoreKinematicInformation()

        self._spawnTarget()
        self._spawnObstacles()

        if self.showGeoFence:
            self._drawGeoFence()

        return self._computeObs()

    def _spawnTarget(self):

        self.targetPosition = self.geoFence.generateRandomPositionOutsideRadius(np.array([0, 0, 1]), 0.5)
        if self.targetId is not None:
            p.removeUserDebugItem(self.targetId, physicsClientId=self.CLIENT)
        
        self.targetId = p.addUserDebugPoints([self.targetPosition], [np.array([0, 1, 0.5])], pointSize=10, physicsClientId=self.CLIENT)

    def _spawnObstacles(self):

        self.obstaclePositions = []
        self.obstacles = []

        for _ in range(self.nObstacles):
            obstaclePos = self.geoFence.generateRandomPositionOutsideRadius(self.targetPosition, 2*self.obstacleRadius)
            while np.linalg.norm(obstaclePos - np.array([0, 0, 1])) < 2*self.obstacleRadius:
                obstaclePos = self.geoFence.generateRandomPositionOutsideRadius(self.targetPosition, 2*self.obstacleRadius)
            self.obstaclePositions.append(obstaclePos)
        
        for obsPos in self.obstaclePositions:
            currObstacle = p.loadURDF('sphere_small.urdf', obsPos, globalScaling=self.obstacleScalingFactor)
            p.changeDynamics(currObstacle, -1, mass=0)
            self.obstacles.append(currObstacle)
        

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

    def _drawTrajectory(self):

        if len(self.trajectory) > 3:
            p.addUserDebugLine(self.trajectory[-2], self.trajectory[-1])

    def step(self, action):

        self.timestepCounter += 1
        
        state = self._getDroneStateVector(0)
        pos = state[0:3]
        self.trajectory.append(pos)
        
        if self.showTrajectory:
            self._drawTrajectory()

        self.lastVelocity = self.currVelocity

        # Normalize the action
        if np.linalg.norm(action[0:3]) != 0:
            v_unit_vector = action[0:3] / np.linalg.norm(action[0:3])
        else:
            v_unit_vector = np.zeros(3)
        
        # Compute actual velocity from normalized action
        self.currVelocity = self.SPEED_LIMIT * np.abs(action[3]) * v_unit_vector

        # Physics step
        return super().step(action)

    def _checkCollision(self):

        for obstacle in self.obstacles:
            contactPoints = p.getContactPoints(self.getDroneIds()[0], obstacle, physicsClientId=self.CLIENT)
            if len(contactPoints):
                return True
        
        return False

    def _computeReward(self):
        state = self._getDroneStateVector(0)

        # Position Penalty
        distToTargetSq = np.linalg.norm(self.targetPosition - state[0:3])**2
        if distToTargetSq <= 0.001:
            positionReward = 1000
        else:
            positionReward = -0.8*distToTargetSq if distToTargetSq > 0.1 else 1/distToTargetSq

        positionReward = np.log(positionReward) if positionReward > 0 else positionReward

        # Collision Penalty
        collisionPenalty = 0 if not self._checkCollision() else -100000
        
        # Obstacle Proximity Penalty
        obstacleProximityPenalty = 0
        if not collisionPenalty and self.nObstacles:
            closestObstacleDist = np.linalg.norm(self._getClosestObstacleOffset())
            distToObstacleSq = closestObstacleDist ** 2
            if distToObstacleSq <= 0.01:
                obstacleProximityPenalty = -5000
            else:
                obstacleProximityPenalty = -0.5/distToObstacleSq

        # Jitter Penalty
        accelerationPenalty = -np.linalg.norm(self.currVelocity - self.lastVelocity)
        velocityPenalty = -np.linalg.norm(self.currVelocity)

        # Linear Combination
        return positionReward + obstacleProximityPenalty + 0.2*accelerationPenalty + 0.1*velocityPenalty + collisionPenalty

    def _computeDone(self):
        if self.timestepCounter >= self.episodeLength:
            return True
        return False
    
    def _computeInfo(self):
        return {}