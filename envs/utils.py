import numpy as np

class PositionConstraint:

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def generateRandomPosition(self, padding=0):
        x = np.random.uniform(self.xmin + padding, self.xmax - padding)
        y = np.random.uniform(self.ymin + padding, self.ymax - padding)
        z = np.random.uniform(self.zmin + padding, self.zmax - padding)

        return np.array([x, y, z])

    def generateRandomPositionWithinRadius(self, center, radius):

        direction = np.random.randn(3)
        direction = direction / np.linalg.norm(direction)
        direction = direction * radius

        generated_point = center + direction

        generated_point[0] = np.clip(generated_point[0], self.xmin, self.xmax)
        generated_point[1] = np.clip(generated_point[1], self.ymin, self.ymax)
        generated_point[2] = np.clip(generated_point[2], self.zmin, self.zmax)
        
        return generated_point

    def inXBounds(self, xVal):
        return self.xmin <= xVal <= self.xmax
    
    def inYBounds(self, yVal):
        return self.ymin <= yVal <= self.ymax

    def inZBounds(self, zVal):
        return self.zmin <= zVal <= self.zmax