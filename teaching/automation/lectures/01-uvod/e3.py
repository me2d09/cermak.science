import numpy as np
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

# Simulate the particle's motion in a magnetic field
for step in range(1, num_steps):
    lorentz_force = charge * np.cross(velocities[step - 1], [1.0, 0.0, 1.0])
    acceleration = lorentz_force / mass
    velocities[step] = velocities[step - 1] + acceleration * time_step
    positions[step] = positions[step - 1] + velocities[step] * time_step

# Extract x and y positions for plotting
x_positions = positions[:, 0]
y_positions = positions[:, 2]

# Plot the trajectory
plt.figure(figsize=(8, 6))
plt.plot(x_positions, y_positions, label="Trajectory")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Particle Trajectory in Magnetic Field")
plt.legend()
plt.grid(True)
plt.show()
