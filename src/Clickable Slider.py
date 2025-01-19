from pyDhd import *
import numpy as np
import matplotlib.pyplot as plt
from time import time

# Initialize the device
dhdOpen()

# Track parameters
y_min, y_max = -0.08, 0.08  # Track range
A = 0.05                   # Amplitude (groove depth)
f_y = 12.0                 # Frequency (groove spacing)
k_spring = 1000            # Spring stiffness coefficient of the track (N/m)
c_damping = 20             # Damping coefficient (N·s/m)

# Haptic ball parameters
sphere_center = np.array([0.0, -0.02, -0.02])  # Ball center position
sphere_radius = 0.015                          # Ball radius
k_sphere = 8000                                # Spring stiffness of the ball

# Data storage
positions_y = []  # Record handle Y-axis position
positions_z = []  # Record handle Z-axis position
forces_x = []     # Record force in X direction
forces_y = []     # Record force in Y direction
forces_z = []     # Record force in Z direction
times = []        # Record time

# Main loop
done = False
start_time = time()
while not done:
    # Get handle position and velocity
    ret, px, py, pz = dhdGetPosition()
    ret, vx, vy, vz = dhdGetLinearVelocity()
    if ret != 0:
        continue  # Skip the loop if data retrieval fails

    # Compute the height of the track surface
    z_surface = A * np.sin(2 * np.pi * f_y * py) + 0.04

    # Compute the surface normal vector
    dz_dy = 2 * np.pi * f_y * A * np.cos(2 * np.pi * f_y * py)  # Gradient of z with respect to y
    norm = np.sqrt(dz_dy**2 + 1)  # Magnitude of normal vector
    normal_vector = np.array([0, -dz_dy / norm, 1 / norm])  # Normal vector direction

    # Calculate offset from handle to surface
    delta_vector = np.array([0, 0, pz - z_surface])

    # Compute spring force along the normal vector
    spring_force = -k_spring * np.dot(delta_vector, normal_vector) * normal_vector

    # Compute damping force along the normal vector
    velocity_vector = np.array([0, vy, vz])
    damping_force = -c_damping * np.dot(velocity_vector, normal_vector) * normal_vector

    # Total force initialized with track force
    total_force = spring_force + damping_force

    # Calculate the distance from handle to ball center
    handle_position = np.array([px, py, pz])
    sphere_offset = handle_position - sphere_center
    distance_to_sphere = np.linalg.norm(sphere_offset)

    # If handle enters the ball range, apply additional spring force
    if distance_to_sphere < sphere_radius:
        sphere_normal = sphere_offset / distance_to_sphere  # Unit normal vector on the ball surface
        sphere_force = -k_sphere * (distance_to_sphere - sphere_radius) * sphere_normal
        total_force += sphere_force

    # Set force feedback
    dhdSetForce(total_force[0], total_force[1], total_force[2])

    # Record data
    current_time = time() - start_time
    positions_y.append(py)
    positions_z.append(pz)
    forces_x.append(total_force[0])
    forces_y.append(total_force[1])
    forces_z.append(total_force[2])
    times.append(current_time)

    # Check exit condition
    done = dhdGetButton(0)

# Close the device
dhdClose()

# Plot results
plt.figure("Force Z vs Time")
plt.plot(times, forces_z, label="Force Z (N)")
plt.xlabel("Time (s)")
plt.ylabel("Force Z (N)")
plt.title("Force Z vs Time")
plt.legend()

plt.figure("Position Z vs Time")
plt.plot(times, positions_z, label="Position Z (m)")
plt.xlabel("Time (s)")
plt.ylabel("Position Z (m)")
plt.title("Position Z vs Time")
plt.legend()

plt.figure("Surface vs Position Y")
y_values = np.linspace(y_min, y_max, 500)
z_surface_values = A * np.sin(2 * np.pi * f_y * y_values) + 0.04
plt.plot(y_values, z_surface_values, label="Surface Z (m)")
plt.scatter(positions_y, positions_z, color='red', label="Handle Position", s=5)
plt.xlabel("Position Y (m)")
plt.ylabel("Surface/Position Z (m)")
plt.title("Surface vs Handle Position")
plt.legend()

plt.show()
