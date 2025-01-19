from pyDhd import *
import numpy as np
import matplotlib.pyplot as plt

# Initialize the device
dhdOpen()

# Sphere parameters
x_c, y_c, z_c = 0.0, 0.0, 0.0  # Sphere center position
R = 0.05  # Sphere radius
k = 3000  # Stiffness coefficient
c = 50    # Damping coefficient

# Initialize 3D visualization
fig = plt.figure("3D Visualization")
fig3D = fig.add_subplot(111, projection='3d')
fig3D.set_xlabel('X Axis (m)')
fig3D.set_ylabel('Y Axis (m)')
fig3D.set_zlabel('Z Axis (m)')

# Plot the sphere surface
u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
sphere_x = x_c + R * np.sin(v) * np.cos(u)
sphere_y = y_c + R * np.sin(v) * np.sin(u)
sphere_z = z_c + R * np.cos(v)
fig3D.plot_surface(sphere_x, sphere_y, sphere_z, color='blue', alpha=0.3, label='Sphere')

# Record handle trajectory
trajectory_x, trajectory_y, trajectory_z = [], [], []

# Main loop
done = False
while not done:
    # Get handle position and velocity
    ret, px, py, pz = dhdGetPosition()
    ret, vx, vy, vz = dhdGetLinearVelocity()
    if ret != 0:
        continue  # Skip this iteration if data retrieval fails

    # Calculate distance from handle to sphere center
    dx, dy, dz = px - x_c, py - y_c, pz - z_c
    d = np.sqrt(dx**2 + dy**2 + dz**2)

    # Store trajectory data
    trajectory_x.append(px)
    trajectory_y.append(py)
    trajectory_z.append(pz)

    # Calculate repulsive force
    if d < R:  # Handle enters the sphere
        spring_force = -k * (d - R)
        damping_force = -c * (vx * dx / d + vy * dy / d + vz * dz / d)
        total_force = spring_force + damping_force
        Fx = total_force * dx / d
        Fy = total_force * dy / d
        Fz = total_force * dz / d
        dhdSetForce(Fx, Fy, Fz)
    else:
        dhdSetForce(0, 0, 0)

    # Check exit condition
    done = dhdGetButton(0)

# Close the device
dhdClose()

# Plot handle movement trajectory
fig3D.plot(trajectory_x, trajectory_y, trajectory_z, color='red', label='Handle Trajectory')
plt.legend()

# Display plot
plt.show()
