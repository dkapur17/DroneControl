import numpy as np
import pybullet as p
import pybullet_data

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.single_agent_rl.BaseSingleAgentAviary import BaseSingleAgentAviary, ActionType, ObservationType
from gym import spaces

from .utils import PositionConstraint

class ObstacleAviary(BaseSingleAgentAviary):

    CLOSE_TO_FINISH_REWARD = 5
    SUCCESS_REWARD = 1000
    COLLISION_PENALTY = -100

    SUCCESS_EPSILON = 0.1

    MINOR_SAFETY_BOUND_RADIUS = 0.3
    MAJOR_SAFETY_BOUND_RADIUS = 0.2
    COLLISION_BOUND_RADIUS = 0.07

    def __init__(self,
                 geoFence:PositionConstraint,
                 useSafetyBounds:bool=True,
                 minObstacles:int=2,
                 maxObstacles:int=7,
                 randomizeObstaclesEveryEpisode:bool=True,
                 assistLearning:bool=True,
                 lenientUntil:int=1000000,
                 fixedAltitude:bool=False,
                 episodeLength:int=1000,
                 showGeoFence:bool=False,
                 showTrajectory:bool=False,
                 showProximityLines:bool=False,
                 randomizeDronePosition:bool=False,
                 randomizeTargetPosition:bool=False,
                 gui:bool=False,
                 freq:int=240,
                 aggregatePhyStep:int=1):


        assert minObstacles <= maxObstacles

        self.fixedAltitude = fixedAltitude
        self.useSafetyBounds = useSafetyBounds   
        self.assistLearning = assistLearning     

        self.minObstacles = minObstacles
        self.maxObstacles = maxObstacles
        self.episodeLength = episodeLength
        self.lenientUntil = lenientUntil
        self.episodeStepCount = 0

        self.geoFence = geoFence

        self.randomizeDronePosition = randomizeDronePosition
        self.randomizeTargetPosition = randomizeTargetPosition
        self.randomizeObstaclesEveryEpisode = randomizeObstaclesEveryEpisode

        if not randomizeDronePosition:
            self.initPos = [self.geoFence.xmin + ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS, (self.geoFence.ymin + self.geoFence.ymax)/2, (self.geoFence.zmin + self.geoFence.zmax)/2]
        else:
            raise NotImplementedError()

        if not randomizeTargetPosition:
            self.targetPos = [self.geoFence.xmax - ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS, (self.geoFence.ymin + self.geoFence.ymax)/2, (self.geoFence.zmin + self.geoFence.zmax)/2]
        else:
            raise NotImplementedError()

        self.altitude = (self.geoFence.zmin + self.geoFence.zmax)/2

        self.showGeoFence = gui and showGeoFence
        self.showTrajectory = gui and showTrajectory
        self.showProximityLines = gui and showProximityLines

        self.trajectory = []

        self.obstaclePositions = []
        self.obstacles = []
        self.totalTimesteps = 0

        super().__init__(drone_model=DroneModel.CF2X,
                        initial_xyzs=np.array([self.initPos]),
                        initial_rpys=np.array([[0, 0, 0]]),
                        physics=Physics.PYB,
                        freq=freq,
                        aggregate_phy_steps=aggregatePhyStep,
                        gui=gui,
                        record=False,
                        obs=ObservationType.KIN,
                        act=ActionType.VEL)

        self._generateObstaclePositions()

        self.offsetLine = None
        self.targetLine = None

    def _observationSpace(self):

        # Drone Offset from target, and drone offset from nearest obstacle
        obsLowerBound = np.array([-np.inf] * (2 if self.fixedAltitude else 3) + [-np.inf, -np.inf, -np.inf])
        obsUpperBound = np.array([np.inf] * (2 if self.fixedAltitude else 3) + [np.inf, np.inf, np.inf])

        return spaces.Box(low=obsLowerBound, high=obsUpperBound, dtype=np.float32)

    def _actionSpace(self):
        
        # [vx, vy, vz, v_mag] or [vx, vy, v_mag] for fixed altitude
        actLowerBound = np.array([-1] * (3 if self.fixedAltitude else 4))
        actUpperBound = np.array([1] * (3 if self.fixedAltitude else 4))
        return spaces.Box(low=actLowerBound, high=actUpperBound, dtype=np.float32)

    def _computeObs(self):

        state = self._getDroneStateVector(0)
        pos = state[:3]

        offsetToTarget = self.targetPos - pos

        if self.fixedAltitude:
            offsetToTarget = offsetToTarget[:2]

        offsetToClosestObstacle = self._computeOffsetToClosestObstacle()
        observation = np.concatenate([offsetToTarget, offsetToClosestObstacle])

        return observation

    def reset(self):
        self.episodeStepCount = 0
        self.trajectory = []
        self.obstacles = []
        self.offsetLine = None
        self.targetLine = None
        
        p.resetSimulation(physicsClientId=self.CLIENT)
        self._housekeeping()
        self._updateAndStoreKinematicInformation()

        p.addUserDebugPoints([self.targetPos], [np.array([0, 1, 0])], pointSize=10, physicsClientId=self.CLIENT)
        
        if self.randomizeObstaclesEveryEpisode:
            self._generateObstaclePositions()

        self._spawnObstacles()

        if self.showGeoFence:
            self._drawGeoFence()

        return self._computeObs()


    def step(self, action):

        if self.fixedAltitude:
            action = np.insert(action, 2, 0)

        self.episodeStepCount += 1
        self.totalTimesteps += 1

        state = self._getDroneStateVector(0)
        pos = state[:3]
        self.trajectory.append(pos)

        if self.offsetLine is not None:
            p.removeUserDebugItem(self.offsetLine, physicsClientId=self.CLIENT)
        
        if self.targetLine is not None:
            p.removeUserDebugItem(self.targetLine, physicsClientId=self.CLIENT)

        offsetToClosestObstacle = self._computeOffsetToClosestObstacle()

        if self.showProximityLines:
            if np.linalg.norm(offsetToClosestObstacle) < ObstacleAviary.MAJOR_SAFETY_BOUND_RADIUS:
                self.offsetLine = p.addUserDebugLine(pos, pos + offsetToClosestObstacle, np.array([1, 0, 0]))
            elif np.linalg.norm(offsetToClosestObstacle) < ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS:
                self.offsetLine = p.addUserDebugLine(pos, pos + offsetToClosestObstacle, np.array([1, 1, 0]))

            if np.linalg.norm(self.targetPos - pos) < ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS:
                self.targetLine = p.addUserDebugLine(self.targetPos, pos, np.array([0, 1, 0]))
            

        if self.showTrajectory:
            self._drawTrajectory()

        return super().step(action)


    def _computeReward(self):

        state = self._getDroneStateVector(0)
        pos = state[:3]

        if np.linalg.norm(self.targetPos - pos) < ObstacleAviary.SUCCESS_EPSILON:
            return ObstacleAviary.SUCCESS_REWARD
        
        if np.linalg.norm(self.targetPos - pos) < ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS:
            return ObstacleAviary.CLOSE_TO_FINISH_REWARD

        offsetToClosestObstacle = self._computeOffsetToClosestObstacle()
        
        distToClosestObstacle = np.linalg.norm(offsetToClosestObstacle)
        
        if distToClosestObstacle < ObstacleAviary.COLLISION_BOUND_RADIUS:
            return ObstacleAviary.COLLISION_PENALTY

        majorBoundBreach = distToClosestObstacle < ObstacleAviary.MAJOR_SAFETY_BOUND_RADIUS and self.useSafetyBounds
        minorBoundBreach = distToClosestObstacle < ObstacleAviary.MINOR_SAFETY_BOUND_RADIUS and self.useSafetyBounds

        return np.linalg.norm(pos - self.initPos) - np.linalg.norm(self.targetPos - pos) - 10*majorBoundBreach - 2*minorBoundBreach


    def _computeOffsetToClosestObstacle(self):

        state = self._getDroneStateVector(0)
        pos = state[:3]
        x,y,z = pos

        # Check distance to all obstacles
        obstacleOffset = None
        
        for obstacle in self.obstacles:
            pointData = p.getClosestPoints(self.DRONE_IDS[0], obstacle, 100, -1, -1, physicsClientId=self.CLIENT)[0]
            offset = np.array(pointData[6]) - pos

            if obstacleOffset is None:
                obstacleOffset = offset
            else:
                obstacleOffset = min(obstacleOffset, offset, key=np.linalg.norm)

        # Check distance to boundaries
        xBoundDist = min(x - self.geoFence.xmin, self.geoFence.xmax - x)
        yBoundDist = min(y - self.geoFence.ymin, self.geoFence.ymax - y)
        zBoundDist = min(z - self.geoFence.zmin, self.geoFence.zmax - z)
        

        boundDists = [xBoundDist, yBoundDist, zBoundDist]

        if xBoundDist == min(boundDists):
            if x - self.geoFence.xmin < self.geoFence.xmax - x:
                fenceOffset = np.array([-(x - self.geoFence.xmin), 0, 0])
            else:
                fenceOffset = np.array([(self.geoFence.xmax - x), 0, 0])

        elif yBoundDist == min(boundDists):
            if y - self.geoFence.ymin < self.geoFence.ymax - y:
                fenceOffset = np.array([0, -(y - self.geoFence.ymin), 0])
            else:
                fenceOffset = np.array([0, (self.geoFence.ymax - y), 0])
        else:
            if z - self.geoFence.zmin < self.geoFence.zmax - z:
                fenceOffset = np.array([0, 0, -(z - self.geoFence.zmin)])
            else:
                fenceOffset = np.array([0, 0, (self.geoFence.zmax - z)])

        return fenceOffset if obstacleOffset is None else min(fenceOffset, obstacleOffset, key=np.linalg.norm) 

    def _computeDone(self):
        state = self._getDroneStateVector(0)
        pos = state[:3]

        if self.episodeLength != -1 and self.episodeStepCount >= self.episodeLength:
            return True

        if np.linalg.norm(self.targetPos - pos) < 0.1:
            return True

        offsetToClosestObstacle = self._computeOffsetToClosestObstacle()

        if np.linalg.norm(offsetToClosestObstacle) <= ObstacleAviary.COLLISION_BOUND_RADIUS:
            return True

        return False

    def _computeInfo(self):
        state = self._getDroneStateVector(0)
        pos = state[:3]

        if self.episodeLength != -1 and self.episodeStepCount >= self.episodeLength:
            return {'success': False}

        if np.linalg.norm(self.targetPos - pos) < 0.1:
            return {'success': True}

        offsetToClosestObstacle = self._computeOffsetToClosestObstacle()

        if np.linalg.norm(offsetToClosestObstacle) <= ObstacleAviary.COLLISION_BOUND_RADIUS:
            return {'success': False}

        return {}

    
    # Utility Functions
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

    def _generateObstaclePositions(self):
        self.obstaclePositions = []
        
        if self.assistLearning and self.totalTimesteps <= self.lenientUntil:
            nObstacles = 0
        else:
            nObstacles = np.random.randint(self.minObstacles, self.maxObstacles)
        for _ in range(nObstacles):
            # Position along all axes is uniform
            obstaclePos = self.geoFence.generateRandomPosition(padding=0.2)

            # Sample Y-axis position from normal distribution for more obstacles towards the middle of the path
            obstaclePos[1] = np.random.random() * (self.geoFence.ymax - self.geoFence.ymin - 0.4) + (self.geoFence.ymin + 0.2)

            if self.fixedAltitude:
                obstaclePos[2] = self.altitude + (np.random.random() - 0.5)*0.2
            
            self.obstaclePositions.append(obstaclePos)


    def _spawnObstacles(self):
        
        for obstaclePos in self.obstaclePositions:
            currObstacle = p.loadURDF('sphere_small.urdf', obstaclePos, globalScaling=(np.random.random()+0.5))
            p.changeDynamics(currObstacle, -1, mass=0)
            self.obstacles.append(currObstacle)