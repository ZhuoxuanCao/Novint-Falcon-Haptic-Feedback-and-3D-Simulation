#!/usr/bin/env python3

from pyDhd import *
from utils import *
from time import time
import numpy as np

dhdOpen()
done = False

# Parameter definitions
k = 11000           # Stiffness coefficient
c = 15              # Initial damping coefficient
m = 0.1             # Virtual mass
yr = -0.02          # Wall position

x_max = 0.2
x_min = -0.2
z_max = 0.2
z_min = -0.2

posy = list()
Force_y = list()
temps = list()

# Time and dynamic damping
t0 = time()
previous_peak = None
current_peak = None
flag = True

while not done:
    # Get position and velocity
    ret, px, py, pz = dhdGetPosition()
    ret, vx, vy, vz = dhdGetLinearVelocity()
    
    # Detect dynamic damping
    if vy < 0 and (current_peak is None or py > current_peak):
        previous_peak = current_peak
        current_peak = py
        if previous_peak is not None and current_peak is not None:
            alpha = np.log(previous_peak / current_peak) / (2 * np.pi)
            c = 2 * np.sqrt(m * k) * alpha  # Dynamically adjust the damping coefficient
    

    if py > yr :
        flag = True
    elif py < yr and (px > x_max or px < x_min or pz > z_max or pz < z_min):
        flag = False
    else:
        flag = flag


    
    # Force feedback calculation
    if py <= yr and px < x_max and px > x_min and pz < z_max and pz > z_min and flag:
        damping_force = -c * vy
        spring_force = -k * (py - yr)
        fy = spring_force + damping_force
        dhdSetForce(0, fy, 0)
    else:
        fy = 0
        dhdSetForce(0, 0, 0)
    
    # Store data
    posy.append(py)
    Force_y.append(fy)
    temps.append(time() - t0)
    
    done = dhdGetButton(0)
    
dhdClose()

# Plot results
figure("Wall Force")
plot(temps, Force_y, 'blue', label='Force Y')
xlabel("Time (s)")
ylabel("Force (N)")
title("Force vs Time")
legend()

figure("Py - Fy")
plot(posy, Force_y, 'blue')
xlabel("Position Y (m)")
ylabel("Force (N)")
title("Force vs Position")

figure()
plot(temps, posy, 'blue', label='Position Y')
xlabel("Time (s)")
ylabel("Position Y (m)")
title("Position vs Time")
legend()
show()
