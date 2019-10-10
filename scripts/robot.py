import numpy as np

class Robot:
    
    def __init__(self, world_size_x, world_size_y, x = None, y = None, theta = None,):
        if x is None:
            x = np.random.randint(0, world_size_x)
        if y is None:
            y = np.random.randint(0, world_size_x)
        if theta is None:
            theta = np.random.randint(0, 360)
        self.world_size_x = world_size_x
        self.world_size_y = world_size_y
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta % 360)
    
    def move(self, rotation, translation):
        self.theta = (self.theta + rotation) % 360
        self.x += translation * np.cos(np.deg2rad(self.theta))
        self.y += translation * np.sin(np.deg2rad(self.theta))
        self.x = max(min(self.world_size_x, self.x), 0)
        self.y = max(min(self.world_size_y, self.y), 0)
        
    def display_values(self):
        print(f"[x = {self.x:07.3f}, \t y = {self.y:07.3f}, \t theta = {self.theta:07.3f}]")
    
    def return_state(self):
        return [self.x,self.y,self.theta]
        