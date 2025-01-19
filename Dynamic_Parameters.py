"""To quantify the system’s dynamic characteristics, 
we calculated the damping ratio, natural frequency"""

import numpy as np
import matplotlib.pyplot as plt
from pyDhd import *
import time  # Replace dhdGetTime with Python's time module

# Initialize parameters
dhdOpen()
k = 800  # Stiffness (N/m)
sampling_time = 0.001  # Sampling time (s)

# Data recording
positions = []
times = []
start_time = time.time()  # Get start time using the time module

# Apply initial displacement (manually move the handle)
print("Please manually move the handle to a position and release it to trigger free oscillation.")
while len(positions) < 10000:  # Collect 5000 data points
    ret, px, py, pz = dhdGetPosition()
    positions.append(px)  # Record x-axis position
    times.append(time.time() - start_time)  # Get relative time by subtracting start time
    dhdSetForce(-k * px, -k * py, -k * pz)  # High-stiffness spring force
    if dhdGetButton(0):  # Exit when the button is pressed
        break

dhdClose()

# Convert to NumPy arrays
positions = np.array(positions)
times = np.array(times)

# Plot oscillation curve
plt.figure("Free Oscillation")
plt.plot(times, positions, label="Position (m)")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Free Oscillation Curve")
plt.grid()
plt.legend()
plt.show()

from scipy.signal import find_peaks

# Identify peaks
peaks_idx, _ = find_peaks(positions, height=0.001, distance=10)
peaks = positions[peaks_idx]

# Verify peaks
if len(peaks) < 2:
    plt.figure("Raw Position Data")
    plt.plot(times, positions)
    plt.title("Raw Oscillation Data")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.grid()
    plt.show()
    raise ValueError(f"Not enough valid peaks found for damping ratio calculation, detected peaks: {len(peaks)}")

# Calculate damping ratio
log_dec = np.log(peaks[:-1] / peaks[1:])  # Logarithmic decrement
zeta = log_dec.mean() / (2 * np.pi)  # Average damping ratio

# Calculate natural frequency and mass
times_peaks = times[peaks_idx]  # Time corresponding to peaks
periods = np.diff(times_peaks)  # Time intervals between adjacent peaks
omega_n = 2 * np.pi / np.mean(periods)  # Natural frequency
mass = k / omega_n**2  # Mass

# Output results
print(f"Damping ratio ζ = {zeta:.4f}")
print(f"Natural frequency ω_n = {omega_n:.2f} rad/s")
print(f"Mass m = {mass:.4f} kg")
