import numpy as np
import matplotlib.pyplot as plt
from robot import Robot

WORLD_SIZE = {'x': 100, 'y': 100}
N_PARTICLES = 100

def generate_list_of_robots(n_robots, world_x, world_y, print_list):
    list_of_particle_robots = []

    for i_robot in range(n_robots):
        list_of_particle_robots.append(Robot(world_x, world_y))
        if print_list:
            list_of_particle_robots[i_robot].display_values()
    return list_of_particle_robots



def display_scatterplot(list_of_robots):
    list_of_particle_states = []
    for robot in list_of_robots:
        list_of_particle_states.append(robot.return_state())
    list_of_particle_states_transp = np.transpose(list_of_particle_states)
    plt.figure()
    plt.scatter(list_of_particle_states_transp[0], list_of_particle_states_transp[1], c = list_of_particle_states_transp[2])
    plt.show()


list_of_robots = generate_list_of_robots(N_PARTICLES, WORLD_SIZE['x'], WORLD_SIZE['y'], True)

display_scatterplot(list_of_robots)






