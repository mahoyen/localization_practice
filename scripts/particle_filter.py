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
    #measurements = [25, 50]
    list_of_particle_states = []
    plt.figure()
    for robot in list_of_robots:
        list_of_particle_states.append(robot.state())
        plot_sense_arrow(robot)
    list_of_particle_states_transp = np.transpose(list_of_particle_states)
    real_state = real_robot.state()
    plt.scatter(list_of_particle_states_transp[0], list_of_particle_states_transp[1], c = list_of_particle_states_transp[2])
    plt.plot(real_state[0], real_state[1],marker = 'x')
    plot_sense_arrow(real_robot)
    plt.axis([0-PLOT_MARGIN, WORLD_SIZE['x']+PLOT_MARGIN, 0-PLOT_MARGIN, WORLD_SIZE['y']+PLOT_MARGIN])
    plt.show()

def plot_sense_arrow(robot):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    measurements = robot.sense(0,0)
    state = robot.state()
    theta_rad = np.deg2rad(state[2])
    
    plt.arrow(state[0], state[1],-measurements[0] * np.cos(theta_rad), -measurements[0]*np.sin(theta_rad), color = 'r')
    plt.arrow(state[0], state[1], measurements[1] * np.sin(theta_rad), -measurements[1]*np.cos(theta_rad), color = 'g')#colors[np.random.randint(7)])


def move_motion_on_list_of_robots(list_of_robots, rotation, translation, motion_noise):
    for robot in list_of_robots:
        robot.move(rotation, translation, motion_noise)
    return list_of_robots

def probabilty_after_measurement_on_list(list_of_robots, measurements, noises):

    prob_list = []
    sum_of_probs = 0
    for robot in list_of_robots:
        probability = robot.prob_measurement(measurements, noises)
        sum_of_probs += probability
        prob_list.append(probability)
    print(sum_of_probs)
    return np.divide(prob_list, sum_of_probs)

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

def np_resample_list_of_robots(list_of_robots, weights):
    return np.random.choice(list_of_robots, np.shape(list_of_robots), True, weights)


WORLD_SIZE = {'x': 100, 'y': 100}
N_PARTICLES = 100
PLOT_MARGIN = 20

NOISE_STRAIGHT = 5
NOISE_SIDE = NOISE_STRAIGHT
MOTION_NOISE = 3

RESAMPLING_NOISE = 7

rotations = [45, 45, 45, 45]
translations = [0, 0, 0, 0]

real_robot = Robot(WORLD_SIZE['x'], WORLD_SIZE['y'], 75,75,0)

particles_of_robots = generate_list_of_robots(N_PARTICLES, WORLD_SIZE['x'], WORLD_SIZE['y'], False)
display_scatterplot(particles_of_robots, real_robot)
for time_step in range(len(rotations)):
    real_robot.move(rotations[time_step], translations[time_step], MOTION_NOISE)
    noisy_meas = real_robot.sense(NOISE_STRAIGHT, NOISE_SIDE)
    particles_of_robots = move_motion_on_list_of_robots(particles_of_robots, rotations[time_step], translations[time_step], MOTION_NOISE)
    weights = probabilty_after_measurement_on_list(particles_of_robots, noisy_meas, [NOISE_STRAIGHT, NOISE_SIDE])
    particles_of_robots = np_resample_list_of_robots(particles_of_robots, weights)
    
    display_scatterplot(particles_of_robots, real_robot)






