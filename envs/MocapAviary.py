import numpy as np
import gym
import matplotlib.pyplot as plt
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.localization import Localization
from gym import spaces
from time import sleep
from typing import List
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.axes3d import Axes3D


from .utils.PositionConstraint import PositionConstraint
from .utils.MocapReader import MocapReader
from .utils.IntervalTimer import IntervalTimer

class MocapAviary(gym.Env):

    MAX_SPEED = 0.08
    
    CLOSE_TO_FINISH_REWARD = 5
    SUCCESS_REWARD = 1000
    COLLISION_PENALTY = -1000

    SUCCESS_EPSILON = 0.1

    MINOR_SAFETY_BOUND_RADIUS = 0.2
    MAJOR_SAFETY_BOUND_RADIUS = 0.1
    COLLISION_BOUND_RADIUS = 0.07

    DISTANCE_PENALTY = 4
    MINOR_SAFETY_PENALTY = 1
    MAJOR_SAFETY_PENALTY = 5

    def __init__(self, URI:str, geoFence:PositionConstraint, obstacles:List[np.ndarray]=[], defaultAltitude:float=0.5, loggingPeriod:int=10):


        cflib.crtp.init_drivers(enable_debug_driver=False)

        self.geoFence = geoFence
        self._currState = None
        self.action_space = self._actionSpace()
        self.observation_space = self._observationSpace()

        self.URI = URI
        self.loggingPeriod = loggingPeriod
        self.defaultAltitude = defaultAltitude
        self.obstacles = obstacles
        self.trajectory = []
        self.noisyTrajectory = []
        
        self.targetPos = np.array([self.geoFence.xmax - MocapAviary.MINOR_SAFETY_BOUND_RADIUS, (self.geoFence.ymin + self.geoFence.ymax)/2, defaultAltitude])
        self.initPos = np.array([self.geoFence.xmin + MocapAviary.MINOR_SAFETY_BOUND_RADIUS, (self.geoFence.ymin + self.geoFence.ymax)/2, self.defaultAltitude])


        self.scf = SyncCrazyflie(self.URI)
        self.scf.open_link()
        self.scf.wait_for_params()
        self.scf.cf.commander.set_client_xmode(True)

        self.mocap_reader = MocapReader()

        self.localizer = Localization(self.scf.cf)
        
        def logPosCallback():
            self._currState = self.mocap_reader.cur_pos
            self.localizer.send_extpos(self._currState)
            self.trajectory.append(self._currState)

        self.logger = IntervalTimer(loggingPeriod, logPosCallback)
        self.motionCommander = MotionCommander(self.scf, default_height=self.defaultAltitude)

    
    def _observationSpace(self):

        obsLowerBound = np.array([self.geoFence.xmin, #x
                                    self.geoFence.ymin, #y
                                    self.geoFence.xmin, #xt
                                    self.geoFence.ymin, #yt
                                    self.geoFence.xmin, #xo
                                    self.geoFence.ymin, #yo
                                ])

        obsUpperBound = np.array([self.geoFence.xmax, #x
                                    self.geoFence.ymax, #y
                                    self.geoFence.xmax, #xt
                                    self.geoFence.ymax, #yt
                                    self.geoFence.xmax, #xo
                                    self.geoFence.ymax, #yo
                                ])
        
        return spaces.Box(low=obsLowerBound, high=obsUpperBound, dtype=np.float32)

    def _actionSpace(self):
        actLowerBound = np.array([-1] * 3)
        actUpperBound = np.array([1] * 3)

        return spaces.Box(low=actLowerBound, high=actUpperBound, dtype=np.float32)

    def _getCurrentState(self):
        return self._currState.copy()
    
    def _computeObs(self):

        pos = self._getCurrentState()
        offsetToClosestObstacle, _ = self._computeOffsetToClosestObstacle()
        closestObstaclePos = offsetToClosestObstacle + pos
        observation = np.concatenate([pos[:2], self.targetPos[:2], closestObstaclePos[:2]])
        return observation

    def reset(self):

        self.trajectory = []
        self.noisyTrajectory = []

        self.motionCommander.take_off()
        sleep(2)

        print("Takeoff Completed")
        self.motionCommander.stop()

        self.logger.start()
        print("Logging Initiated")
        sleep(2)

        self.scf.cf.commander.send_position_setpoint(self.initPos[0], self.initPos[1], self.initPos[2], 0)
        sleep(2)
        

        plt.gcf().set_figheight((self.geoFence.ymax - self.geoFence.ymin) * 5)
        plt.gcf().set_figwidth((self.geoFence.xmax - self.geoFence.xmin) * 5)
        plt.gcf().canvas.manager.set_window_title("Trajectory")

        return self._computeObs()
    
    def step(self, action):

        vel = (action[:2] / np.linalg.norm(action[:2])) * np.abs(action[2]) * MocapAviary.MAX_SPEED

        self.motionCommander.start_linear_motion(vel[0], vel[1], 0, 0)
        return self._computeObs(), self._computeReward(), self._computeDone(), self._computeInfo()
    
    def render(self, mode='text'):

        if mode not in ['2d', '3d', 'text']:
            print(f"Unknown render mode: {mode}. Defaulting to text.")
            mode = 'text'

        if mode == '2d':
           
            plt.clf()
            plt.xlim(self.geoFence.xmin, self.geoFence.xmax)
            plt.ylim(self.geoFence.ymin, self.geoFence.ymax)

            plt.xticks(np.arange(self.geoFence.xmin, self.geoFence.xmax + 0.1, 0.1))
            plt.yticks(np.arange(self.geoFence.ymin, self.geoFence.ymax + 0.1, 0.1))
            plt.grid()

            atomic_trajectory = self.trajectory.copy()
            atomic_noisy_trajectory = self.noisyTrajectory.copy()
            plt.plot([p[0] for p in atomic_trajectory], [p[1] for p in atomic_trajectory], 'r')
            plt.scatter([p[0] for p in atomic_noisy_trajectory], [p[1] for p in atomic_noisy_trajectory], 'g',s=[20])
            plt.scatter([self._currState[0]], [self._currState[1]], marker='>', s=[400], color='black')

            plt.scatter([self.initPos[0]], [self.initPos[1]], marker='x')

            for obstacle in self.obstacles:
                obs_circle = plt.Circle((obstacle[0], obstacle[1]), obstacle[2], color='red')
                plt.gca().add_artist(obs_circle)

            plt.scatter([self.targetPos[0]], [self.targetPos[1]], marker='*')
            target_success_radius = plt.Circle((self.targetPos[0], self.targetPos[1]), MocapAviary.SUCCESS_EPSILON, fill=False)
            plt.gca().add_artist(target_success_radius)

        elif mode == '3d':
           
            plt.clf()
            ax = plt.axes(projection='3d', azim=180, elev=90)
            ax.set_box_aspect(aspect=None, zoom=1.6)

            ax.w_xaxis.line.set_color("red")
            ax.w_yaxis.line.set_color("green")
            ax.w_zaxis.line.set_color("blue")

            x_scale = self.geoFence.xmax - self.geoFence.xmin
            y_scale = self.geoFence.ymax - self.geoFence.ymin
            z_scale = self.geoFence.zmax - self.geoFence.zmin

            scale=np.diag([x_scale, y_scale, z_scale, 1.0])
            scale=scale*(1.0/scale.max())
            scale[3,3]=1.0

            def short_proj():
                return np.dot(Axes3D.get_proj(ax), scale)

            ax.get_proj = short_proj
            
            ax.set_xlim(self.geoFence.xmin, self.geoFence.xmax)
            ax.set_ylim(self.geoFence.ymin, self.geoFence.ymax)
            ax.set_zlim(self.geoFence.zmin, self.geoFence.zmax)
            ax.set_xticks(np.arange(self.geoFence.xmin, self.geoFence.xmax + 0.1, 0.1))
            ax.set_yticks(np.arange(self.geoFence.ymin, self.geoFence.ymax + 0.1, 0.1))
            ax.set_zticks(np.arange(self.geoFence.zmin, self.geoFence.zmax + 0.1, 0.1))
            
            ax.scatter3D([self.initPos[0]], [self.initPos[1]], [self.initPos[2]], marker='x')
            ax.scatter3D([self.targetPos[0]], [self.targetPos[1]], [self.targetPos[2]], marker='*')
            atomic_noisy_trajectory = self.noisyTrajectory.copy()
            ax.scatter3D([p[0] for p in atomic_noisy_trajectory], [p[1] for p in atomic_noisy_trajectory], [p[2] for p in atomic_noisy_trajectory], s=1)
            atomic_trajectory = self.trajectory.copy()
            ax.plot3D([p[0] for p in atomic_trajectory], [p[1] for p in atomic_trajectory], [p[2] for p in atomic_trajectory])
            ax.scatter3D([self.current_true_state[0]], [self.current_true_state[1]], [self.current_true_state[2]], marker='^', s=225)

            points_whole_ax = 5 * 0.8 * 72    # 1 point = dpi / 72 pixels
            for obs in self.obstacles:
                c = np.array([obs[0], obs[1], self.defaultAltitude])
                r = obs[2]
                points_radius = 2 * r / 1.0 * points_whole_ax

                ax.scatter3D(c[0], c[1], c[2], marker='o', s=points_radius**2)


            plt.pause(0.0001)

        else:
            pos = self._getCurrentState()
            offsetToClosestObstacle, closestObstacle = self._computeOffsetToClosestObstacle()
            print(f"Drone Position: {pos}")
            print(f"Offset To Target: {self.targetPos - pos}")
            print(f"Closest Obstacle: {closestObstacle}")
            print(f"Offset To Closest Obstacle: {offsetToClosestObstacle}")

    def _computeOffsetToClosestObstacle(self):
        
        pos = self._getCurrentState()
        x,y,z = pos

        obstacleOffset = None

        closestObstacle = None
        for i, obstacle in enumerate(self.obstacles):
            offset = np.array([obstacle[0], obstacle[1], self.defaultAltitude]) - pos
            dist_to_obstacle_surface = np.linalg.norm(offset) - obstacle[2]
            offset = (offset / np.linalg.norm(offset)) * dist_to_obstacle_surface

            if obstacleOffset is None:
                obstacleOffset = offset
                closestObstacle = i
            elif np.linalg.norm(offset) < np.linalg.norm(obstacleOffset):
                obstacleOffset = offset
                closestObstacle = i

        
        xBoundDist = min(x - self.geoFence.xmin, self.geoFence.xmax - x)
        yBoundDist = min(y - self.geoFence.ymin, self.geoFence.ymax - y)
        zBoundDist = min(z - self.geoFence.zmin, self.geoFence.zmax - z)

        boundDists = [xBoundDist, yBoundDist, zBoundDist]

        closestWall = None
        if xBoundDist == min(boundDists):
            if x - self.geoFence.xmin < self.geoFence.xmax - x:
                fenceOffset = np.array([-(x - self.geoFence.xmin), 0, 0])
                closestWall = 'Back'
            else:
                fenceOffset = np.array([(self.geoFence.xmax - x), 0, 0])
                closestWall = 'Front'

        elif yBoundDist == min(boundDists):
            if y - self.geoFence.ymin < self.geoFence.ymax - y:
                fenceOffset = np.array([0, -(y - self.geoFence.ymin), 0])
                closestWall = 'Right'
            else:
                fenceOffset = np.array([0, (self.geoFence.ymax - y), 0])
                closestWall = 'Left'
        else:
            if z - self.geoFence.zmin < self.geoFence.zmax - z:
                fenceOffset = np.array([0, 0, -(z - self.geoFence.zmin)])
                closestWall = 'Bottom'
            else:
                fenceOffset = np.array([0, 0, (self.geoFence.zmax - z)])
                closestWall = 'Top'

        if obstacleOffset is None:
            return fenceOffset, f'{closestWall} Wall'
        elif np.linalg.norm(fenceOffset) < np.linalg.norm(obstacleOffset):
            return fenceOffset, f'{closestWall} Wall'
        else:
            return obstacleOffset, f'Obstacle {closestObstacle}'

    def _computeReward(self):
        
        pos = self._getCurrentState()

        if np.linalg.norm(self.targetPos - pos) < MocapAviary.SUCCESS_EPSILON:
            return MocapAviary.SUCCESS_REWARD
        
        if np.linalg.norm(self.targetPos - pos) < MocapAviary.MINOR_SAFETY_BOUND_RADIUS:
            return MocapAviary.CLOSE_TO_FINISH_REWARD

        offsetToClosestObstacle, _ = self._computeOffsetToClosestObstacle()
        distToClosestObstacle = np.linalg.norm(offsetToClosestObstacle)

        if distToClosestObstacle < MocapAviary.COLLISION_BOUND_RADIUS:
            return MocapAviary.COLLISION_PENALTY

        majorBoundBreach = distToClosestObstacle < MocapAviary.MAJOR_SAFETY_BOUND_RADIUS
        minorBoundBreach = distToClosestObstacle < MocapAviary.MINOR_SAFETY_BOUND_RADIUS

        return -MocapAviary.DISTANCE_PENALTY*np.linalg.norm(self.targetPos - pos)\
                -MocapAviary.MAJOR_SAFETY_PENALTY*majorBoundBreach\
                -MocapAviary.MINOR_SAFETY_PENALTY*minorBoundBreach
    
    def _computeDone(self):

        pos = self._getCurrentState()

        if np.linalg.norm(self.targetPos - pos) <= MocapAviary.SUCCESS_EPSILON:
            self.motionCommander.stop()
            print("Reached Target!")
            return True
        
        offsetToClosestObstacle, _ = self._computeOffsetToClosestObstacle()
        
        if np.linalg.norm(offsetToClosestObstacle) <= MocapAviary.COLLISION_BOUND_RADIUS:
            print("Collided With Obstacle!")
            return True

        return False

    def _computeInfo(self):

        pos = self._getCurrentState()

        if np.linalg.norm(self.targetPos - pos) < MocapAviary.SUCCESS_EPSILON:
            return {'success': True}
        
        offsetToClosestObstacle, closestObstacle = self._computeOffsetToClosestObstacle()

        if np.linalg.norm(offsetToClosestObstacle) <= MocapAviary.COLLISION_BOUND_RADIUS:
            return {'success': False}

        return {'closest_obstacle': closestObstacle}


    def close(self):
        self.motionCommander.land()
        self.logger.stop()
        self.scf.close_link()
        plt.show()

    def emergencyStop(self):
        print("Emergency Stop Initiated!")
        self.scf.cf.commander.send_stop_setpoint()