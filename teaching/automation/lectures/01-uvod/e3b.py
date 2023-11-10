# Simulate the particle's motion in a magnetic field
for step in range(1, num_steps):
    lorentz_force = charge * np.cross(velocities[step - 1], [1.0, 0.0, 1.0])
    acceleration = lorentz_force / mass
    velocities[step] = velocities[step - 1] + acceleration * time_step
    positions[step] = positions[step - 1] + velocities[step] * time_step
