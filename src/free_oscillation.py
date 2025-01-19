# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:04:38 2024

@author: UserTP
"""

from pyDhd import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Initialize the device
dhdOpen()
print("Device initialized. Move the handle to an initial displacement and release. Press the button to finish.")

# Data storage lists
positions = []  # Record position data
time_steps = []  # Time step recording

# Initialize time step
time_step = 0
done = False

# Wait for initial release
input("Move the handle to an initial displacement and press Enter to start recording...")

# Main loop: Record free oscillation
while not done:
    ret, px, _, _ = dhdGetPosition()  # Get position in X direction only
    if ret == 0:  # Check if device reading is successful
        positions.append(px)
        time_steps.append(time_step)
        time_step += 1

    # Stop applying force to allow free oscillation
    dhdSetForce(0, 0, 0)

    # Check exit condition
    done = dhdGetButton(0)

# Close the device
dhdClose()
print("Device closed.")

# Convert time steps to time
time_interval = 0.001  # Assume the device samples every millisecond
times = np.array(time_steps) * time_interval
positions = np.array(positions)

# Plot free oscillation curve
plt.figure("Free Oscillation Experiment")
plt.plot(times, positions, label="Measured Position", color='blue')
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Free Oscillation Curve")
plt.grid(True)
plt.legend()

# Free oscillation equation model
def oscillation_model(t, A, omega, gamma, phi, offset):
    """Damped sinusoidal model"""
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi) + offset

# Initial fitting parameters
A_guess = max(abs(positions))
omega_guess = 2 * np.pi / (times[np.argmax(positions)] - times[np.argmax(positions[1:])])
gamma_guess = 0.1  # Initial damping coefficient assumption
phi_guess = 0
offset_guess = np.mean(positions)

popt, _ = curve_fit(oscillation_model, times, positions,
                    p0=[A_guess, omega_guess, gamma_guess, phi_guess, offset_guess])

A, omega, gamma, phi, offset = popt

# Compute apparent mass and damping
k = omega ** 2  # Stiffness coefficient (omega^2 = k / m, assuming mass = 1)
m = 1  # Assume unit mass
c = 2 * gamma * m  # Damping coefficient

# Output results
print("\nFitted free oscillation parameters:")
print(f"Amplitude (A): {A:.4f}")
print(f"Angular frequency (omega): {omega:.4f}")
print(f"Damping coefficient (gamma): {gamma:.4f}")
print(f"Phase (phi): {phi:.4f}")
print(f"Offset (offset): {offset:.4f}")
print("\nCalculated results:")
print(f"Apparent stiffness (k): {k:.4f} N/m")
print(f"Apparent damping (c): {c:.4f} Ns/m")

# Plot fitted curve
fitted_positions = oscillation_model(times, *popt)
plt.plot(times, fitted_positions, label="Fitted Model", linestyle="--", color="red")
plt.legend()
plt.show()

# # Save data to file
# np.savetxt("free_oscillation_data.csv", np.column_stack([times, positions]), delimiter=",",
#            header="time,position", comments='')
# print("Data saved to 'free_oscillation_data.csv'.")
