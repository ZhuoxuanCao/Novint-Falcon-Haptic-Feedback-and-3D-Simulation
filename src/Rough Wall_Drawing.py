import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameter settings
A = 0.05  # Amplitude
fx = 2    # Frequency in x direction
fy = 2    # Frequency in y direction

# Define the range of x and y values
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)

# Calculate the z values based on the formula
Z = -0.02 + A * np.sin(2 * np.pi * fx * X) * np.cos(2 * np.pi * fy * Y)

# Create a 3D figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Add color bar
fig.colorbar(surf, shrink=0.5, aspect=10)

# Set title and axis labels
ax.set_title('Simulation of a Rough Sinusoidal Wall')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display the plot
plt.show()
