import numpy as np

class Robot:
    
    def __init__(self, world_size_x, world_size_y, x = None, y = None, theta = None,):
        if x is None:
            x = np.random.randint(world_size_x)
        if y is None:
            y = np.random.randint(world_size_x)
        if theta is None:
            theta = np.random.randint(0, 360)
        self.world_size_x = world_size_x
        self.world_size_y = world_size_y
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta % 360)
    
    def move(self, rotation, translation, motion_noise):
        self.theta = np.random.normal((self.theta + rotation) % 360,, motion_noise) 
        self.x += np.random.normal(translation * np.cos(np.deg2rad(self.theta)), motion_noise)
        self.y += np.random.normal(translation * np.sin(np.deg2rad(self.theta)), motion_noise)
        self.x = max(min(self.world_size_x, self.x), 0)
        self.y = max(min(self.world_size_y, self.y), 0)

    def sense(self, noise_straight, noise_side):
        print(f"theta: {self.theta}")
        if (self.theta > 45 and self.theta < 135) or (self.theta < 315 and self.theta > 225):
            straight_laser = abs(self.y/np.sin(self.theta))
            side_laser = abs(self.x/np.sin(self.theta))
            print(f"sin: {np.sin(self.theta)}")
        else:
            straight_laser = abs(self.y/np.cos(self.theta))
            side_laser = abs(self.x/np.cos(self.theta))
            print(f"cos {np.cos(self.theta)}")

        print(f"straight {straight_laser}, side {side_laser}")
        print(f"x        {self.x}, y     {self.y}")
        print()
        noisy_straight = np.random.normal(straight_laser, noise_straight)
        noisy_side = np.random.normal(side_laser, noise_side)
        return [noisy_straight, noisy_side]

    def prob_normal_distribution(self, x, mean, variance):
        return 1/np.sqrt(2 * np.pi* variance)*np.exp(-(x-mean)**2/(2*variance))

    def prob_measurement(self, measurements, noises):
        simulated_measurements = self.sense(0,0)
        probability = 1.0
        for i_sensor in range(len(simulated_measurements)):
            probability *= self.prob_normal_distribution(measurements[i_sensor],simulated_measurements[i_sensor], noises[i_sensor])
        return probability

        
    def display_values(self):
        print(f"[x = {self.x:07.3f}, \t y = {self.y:07.3f}, \t theta = {self.theta:07.3f}]")
    
    def state(self):
        return [self.x,self.y,self.theta]
        