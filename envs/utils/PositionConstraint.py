import numpy as np

class PositionConstraint:

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def generateRandomPosition(self, padding:float=0):
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

    def generateRandomPositionOutsideRadius(self, center, radius):

        x_exc_min = max(center[0] - radius, self.xmin)
        x_exc_max = min(center[0] + radius, self.xmax)

        x1 = np.random.uniform(self.xmin, x_exc_min)
        x2 = np.random.uniform(x_exc_max, self.xmax)

        px1 = (x_exc_min - self.xmin)/((x_exc_min - self.xmin) + (self.xmax - x_exc_max))
        X = x1 if np.random.random() <= px1 else x2

        y_exc_min = max(center[1] - radius, self.ymin)
        y_exc_max = min(center[1] + radius, self.ymax)

        y1 = np.random.uniform(self.ymin, y_exc_min)
        y2 = np.random.uniform(y_exc_max, self.ymax)

        py1 = (y_exc_min - self.ymin)/((y_exc_min - self.ymin) + (self.ymax - y_exc_max))
        Y = y1 if np.random.random() <= py1 else y2

        z_exc_min = max(center[2] - radius, self.zmin)
        z_exc_max = min(center[2] + radius, self.zmax)

        z1 = np.random.uniform(self.zmin, z_exc_min)
        z2 = np.random.uniform(z_exc_max, self.zmax)

        pz1 = (z_exc_min - self.zmin)/((z_exc_min - self.zmin) + (self.zmax - z_exc_max))
        Z = z1 if np.random.random() <= pz1 else z2

        return np.array([X, Y, Z])


    def inXBounds(self, xVal):
        return self.xmin <= xVal <= self.xmax
    
    def inYBounds(self, yVal):
        return self.ymin <= yVal <= self.ymax

    def inZBounds(self, zVal):
        return self.zmin <= zVal <= self.zmax

    def inBounds(self, pos):
        return self.inXBounds(pos[0]) and self.inYBounds(pos[1]) and self.inZBounds(pos[2])

