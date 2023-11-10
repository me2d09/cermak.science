import numpy as np
import matplotlib.pyplot as plt

# Define initial conditions
mass = 1.0
charge = 1.0
time_step = 0.01
total_time = 10.0

num_steps = int(total_time / time_step)
positions = np.zeros((num_steps, 3))
velocities = np.zeros((num_steps, 3))

positions[0] = [0.0, 0.0, 0.0]
velocities[0] = [0.0, 0.0, 1.0]
