import numpy as np
import matplotlib.pyplot as plt
from robot import Robot

def generate_list_of_robots(n_robots, world_x, world_y, print_list):
    list_of_particle_robots = []

    for i_robot in range(n_robots):
        list_of_particle_robots.append(Robot(world_x, world_y))
        if print_list:
            list_of_particle_robots[i_robot].display_values()
    return list_of_particle_robots



def display_scatterplot(list_of_robots, real_robot):
    list_of_particle_states = []
    for robot in list_of_robots:
        list_of_particle_states.append(robot.state())
    list_of_particle_states_transp = np.transpose(list_of_particle_states)
    plt.figure()
    plt.scatter(list_of_particle_states_transp[0], list_of_particle_states_transp[1], c = list_of_particle_states_transp[2])
    real_state = real_robot.state()
    plt.plot(real_state[0], real_state[1],marker = 'x')
    plt.axis([0, WORLD_SIZE['x'], 0, WORLD_SIZE['y']])
    plt.show()

def move_motion_on_list_of_robots(list_of_robots, rotation, translation):
    for robot in list_of_robots:
        robot.move(rotation, translation)
    return list_of_robots

def probabilty_after_measurement_on_list(list_of_robots, measurements, noises):

    prob_list = []
    sum_of_probs = 0
    for robot in list_of_robots:
        probability = robot.prob_measurement(measurements, noises)
        sum_of_probs += probability
        prob_list.append(probability)
    print(sum_of_probs)
    return prob_list

def my_resample_list_of_robots(list_of_robots, weights):
    N = len(list_of_robots)
    new_robot_list = []
    cumulative_sum = np.cumsum(weights)
    for _ in range(N):
        index = 0
        beta = np.random.rand()*cumulative_sum[-1]
        while beta > cumulative_sum[index]:
            beta -= weights[index]
            index = (index + 1 ) % N
        new_robot_list.append(list_of_robots[index])
    return new_robot_list

def other_resample_list_of_robots(list_of_robots, weights):
    N = len(list_of_robots)
    new_robot_list = []
    index = np.random.randint(N)
    beta = 0.
    max_w = max(weights)
    for _ in range(N):
        beta += np.random.rand()*2*max_w
        while beta > weights[index]:
            beta -= weights[index]
            index = (index + 1 ) % N
        new_robot_list.append(list_of_robots[index])
    return new_robot_list


WORLD_SIZE = {'x': 100, 'y': 100}
N_PARTICLES = 1000

NOISE_STRAIGHT = 50
NOISE_SIDE = NOISE_STRAIGHT

rotations = [0.0, 1.0, 3]
translations = [2, 3, 5]

real_robot = Robot(WORLD_SIZE['x'], WORLD_SIZE['y'])

particles_of_robots = generate_list_of_robots(N_PARTICLES, WORLD_SIZE['x'], WORLD_SIZE['y'], False)
display_scatterplot(particles_of_robots, real_robot)
for time_step in range(len(rotations)):
    real_robot.move(rotations[time_step], translations[time_step])
    noisy_meas = real_robot.sense(NOISE_STRAIGHT, NOISE_SIDE)
    particles_of_robots = move_motion_on_list_of_robots(particles_of_robots, rotations[time_step], translations[time_step])
    weights = probabilty_after_measurement_on_list(particles_of_robots, noisy_meas, [NOISE_STRAIGHT, NOISE_SIDE])
    particles_of_robots = other_resample_list_of_robots(particles_of_robots, weights)
    
    display_scatterplot(particles_of_robots, real_robot)






