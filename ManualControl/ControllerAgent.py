import numpy as np
from XboxController import XboxController

class ControllerAgent:

    def __init__(self):
        self.joy = XboxController()

    def wait_for_start(self):
        while not self.joy.read()['start']:
            pass

    def get_action(self):

        vX = self.joy.read()['rightJoystickY']
        vY = self.joy.read()['rightJoystickX']
        vZ = self.joy.read()['leftJoystickY']

        return np.array([vX, vY, vZ, 1])

    