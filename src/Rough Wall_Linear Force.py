from pyDhd import *
from utils import *
from time import time
import numpy as np

dhdOpen()
done = False

# Parameter definitions
k = 1000           # Stiffness
c = 15             # Initial damping coefficient
m = 0.1            # Virtual mass

# Define wall boundaries
x_max = 0.1
x_min = -0.1
y_max = 0.1
y_min = -0.1

# Corrugated wall parameters
A = 0.005          # Amplitude (depth of corrugation)
fx = 300.0         # Frequency in x-direction
fy = 300.0         # Frequency in y-direction

# Data storage
posz = list()
Force_z = list()
temps = list()

# Time initialization
t0 = time()

while not done:
    # Get position and velocity
    ret, px, py, pz = dhdGetPosition()
    ret, vx, vy, vz = dhdGetLinearVelocity()

    # Dynamically compute the wall height zr(px, py)
    zr = -0.02 + A * np.sin(2 * np.pi * fx * px) * np.cos(2 * np.pi * fy * py)

    # Force feedback calculation
    if pz <= zr and px < x_max and px > x_min and py < y_max and py > y_min:
        # If the handle penetrates the wall, calculate feedback force
        damping_force = -c * vz
        spring_force = -k * (pz - zr)
        fz = spring_force + damping_force
        dhdSetForce(0, 0, fz)
    else:
        # If outside the wall or not touching, apply no feedback force
        fz = 0
        dhdSetForce(0, 0, 0)

    # Store data
    posz.append(pz)
    Force_z.append(fz)
    temps.append(time() - t0)

    done = dhdGetButton(0)

dhdClose()

# Plot results
figure("Wall Force")
plot(temps, Force_z, 'blue', label='Force Z')
xlabel("Time (s)")
ylabel("Force (N)")
title("Force vs Time")
legend()

figure("Pz - Fz")
plot(posz, Force_z, 'blue')
xlabel("Position Z (m)")
ylabel("Force (N)")
title("Force vs Position")
show()

figure()
plot(temps, posz, 'blue', label='Position Z')
xlabel("Time (s)")
ylabel("Position Z (m)")
title("Position vs Time")
show()
