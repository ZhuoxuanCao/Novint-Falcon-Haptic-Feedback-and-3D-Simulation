from pyDhd import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from time import time

# Initialize time
t0 = time()

# Data storage
temps = []  # Time
posy, forcey = [], []  # Position and force

# Initialize parameters
done = False
dhdOpen()

# Loop to read handle position and apply virtual force
while not done:
    ret, px, py, pz = dhdGetPosition()  # Get handle position

    # Determine position and apply force
    if py < -0.02:
        dhdSetForce(0, 20, 0)  # Apply an upward virtual force when Y < -0.02
    else:
        dhdSetForce(0, 0, 0)  # Otherwise, apply no force

    # Record data
    posy.append(py)    
    ret, fx, fy, fz = dhdGetForce()  # Get handle feedback force

    forcey.append(fy)
    temps.append(time() - t0)  # Record relative time
    done = dhdGetButton(0)  # Check if the button is pressed to end the loop

# Close the device
dhdClose()

# Plot Y position vs time
plt.figure("Y Position vs Time")
plt.plot(temps, posy, label="Y Position", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Y Position (m)")
plt.title("Y Position vs Time")
plt.legend()
plt.grid()

# Plot force vs time
plt.figure("Force vs Time")
plt.plot(temps, forcey, label="Force Y", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.title("Force vs Time")
plt.legend()
plt.grid()

# Plot force vs Y position
plt.figure("Force vs Position Y")
plt.plot(posy, forcey, label="Force vs Y Position", color="red")
plt.xlabel("Y Position (m)")
plt.ylabel("Force (N)")
plt.title("Force vs Position Y")
plt.legend()
plt.grid()

# Show all plots
plt.show()
