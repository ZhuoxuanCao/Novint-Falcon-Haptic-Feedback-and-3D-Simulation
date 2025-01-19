"""
Simulating an infinite cylinder with force feedback using dhd functions
"""

from pyDhd import *
from utils import *
from time import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

dhdOpen()
done = False

# Parameter definitions
k = 2000           # Stiffness coefficient
c = 15             # Damping coefficient

# Define cylinder properties
cylinder_center = np.array([0, 0])  # Cylinder center at (x_c, y_c)
cylinder_radius = 0.03  # Cylinder radius
cylinder_height = 0.1   # Cylinder height

# Data storage
posx, posy, posz = [], [], []
force_x, force_y, force_z = [], [], []
temps = []

# Initialize time
t0 = time()

while not done:
    # Get handle position and velocity
    ret, px, py, pz = dhdGetPosition()
    ret, vx, vy, vz = dhdGetLinearVelocity()

    # Initialize force feedback
    fx, fy, fz = 0, 0, 0

    # Calculate distance to the cylinder center
    vector_to_center = np.array([px, py]) - cylinder_center
    distance_to_center = np.linalg.norm(vector_to_center)
    distance_to_surface = cylinder_radius - distance_to_center

    if distance_to_center < cylinder_radius:  # Handle is inside the cylinder
        # Calculate the outward normal vector
        if distance_to_center != 0:  # Avoid division by zero
            direction_to_outside = -vector_to_center / distance_to_center
        else:
            direction_to_outside = np.array([0, 0])  # No directional force at center
        
        # Calculate feedback force: pointing outward
        fx = -k * direction_to_outside[0] * abs(distance_to_surface) - c * vx
        fy = -k * direction_to_outside[1] * abs(distance_to_surface) - c * vy
    else:  # Handle is outside the cylinder, no force applied
        fx, fy, fz = 0, 0, 0

    # Apply force feedback
    dhdSetForce(fx, fy, fz)

    # Store data
    posx.append(px)
    posy.append(py)
    posz.append(pz)
    force_x.append(fx)
    force_y.append(fy)
    force_z.append(fz)
    temps.append(time() - t0)

    done = dhdGetButton(0)

dhdClose()

# Plot cylinder and robot trajectory
fig = plt.figure("Robot Trajectory and Cylinder")
ax = fig.add_subplot(111, projection='3d')

# Plot the cylinder
theta = np.linspace(0, 2 * np.pi, 50)  # Angles for the cylinder
z = np.linspace(-cylinder_height / 2, cylinder_height / 2, 50)  # Cylinder height range
theta, z = np.meshgrid(theta, z)

x = cylinder_radius * np.cos(theta) + cylinder_center[0]
y = cylinder_radius * np.sin(theta) + cylinder_center[1]

ax.plot_surface(x, y, z, color='b', alpha=0.3, edgecolor='none')  # Semi-transparent cylinder

# Plot the robot trajectory
ax.plot(posx, posy, posz, label="Trajectory", color='r')
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")
ax.set_zlabel("Z Position (m)")
ax.legend()

plt.title("Robot Trajectory Around Cylinder with 3D Cylinder Model")
plt.show()

# Generate high-resolution heatmaps
x_range = np.linspace(-0.05, 0.05, 200)  # 200 points for higher resolution
y_range = np.linspace(-0.05, 0.05, 200)
Fx_map = np.zeros((len(x_range), len(y_range)))
Fy_map = np.zeros((len(x_range), len(y_range)))

for i, px in enumerate(x_range):
    for j, py in enumerate(y_range):
        vector_to_center = np.array([px, py]) - cylinder_center
        distance_to_center = np.linalg.norm(vector_to_center)
        distance_to_surface = cylinder_radius - distance_to_center
        fx, fy = 0, 0

        if distance_to_center < cylinder_radius:  # Handle is inside the cylinder
            if distance_to_center != 0:  # Avoid division by zero
                direction_to_outside = -vector_to_center / distance_to_center
            else:
                direction_to_outside = np.array([0, 0])
            fx = -k * direction_to_outside[0] * abs(distance_to_surface)
            fy = -k * direction_to_outside[1] * abs(distance_to_surface)

        Fx_map[i, j] = fx
        Fy_map[i, j] = fy

# Plot heatmap - Force X
plt.figure("High Resolution Heatmap of Fx")
plt.contourf(x_range, y_range, Fx_map.T, levels=100, cmap='hot')  # Increase levels to 100
plt.colorbar(label="Force X (N)")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("High Resolution Heatmap of Force X")
plt.grid()

# Plot heatmap - Force Y
plt.figure("High Resolution Heatmap of Fy")
plt.contourf(x_range, y_range, Fy_map.T, levels=100, cmap='cool')  # Increase levels to 100
plt.colorbar(label="Force Y (N)")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("High Resolution Heatmap of Force Y")
plt.grid()

plt.show()
