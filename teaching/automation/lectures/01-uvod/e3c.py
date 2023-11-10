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
