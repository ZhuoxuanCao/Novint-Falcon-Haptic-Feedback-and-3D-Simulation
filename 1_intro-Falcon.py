from pyDhd import *
import numpy as np
import matplotlib.pyplot as plt

# Initialize the device
dhdOpen()
print("Device initialized. Please move the handle to explore the workspace.")
print("Press the device button to finish.")

# Initialize max and min values
px_max, py_max, pz_max = -np.inf, -np.inf, -np.inf
px_min, py_min, pz_min = np.inf, np.inf, np.inf

# Store position data
posx, posy, posz = [], [], []

# Main loop: Read handle position and record workspace limits
done = False
while not done:
    ret, px, py, pz = dhdGetPosition()  # Get current position
    if ret == 0:  # Check if device reading is successful
        # Update max and min values
        px_max, py_max, pz_max = max(px, px_max), max(py, py_max), max(pz, pz_max)
        px_min, py_min, pz_min = min(px, px_min), min(py, py_min), min(pz, pz_min)
        
        # Record data
        posx.append(px)
        posy.append(py)
        posz.append(pz)

        # Output real-time position
        print(f"Position: ({px:.2f}, {py:.2f}, {pz:.2f})")

    # Check exit condition
    done = dhdGetButton(0)

# Close the device
dhdClose()
print("Device closed.")

# Output workspace dimensions
print("\nWorkspace dimensions:")
print(f"x-axis: min = {px_min:.2f}, max = {px_max:.2f}")
print(f"y-axis: min = {py_min:.2f}, max = {py_max:.2f}")
print(f"z-axis: min = {pz_min:.2f}, max = {pz_max:.2f}")

# Visualize handle position distribution
plt.figure("Workspace Exploration")
plt.scatter(posx, posy, c=posz, cmap='viridis', marker='o')
plt.colorbar(label="z-axis (depth)")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("Workspace Position Distribution")
plt.grid(True)
plt.show()

# Save data to file
np.savetxt("workspace_data.csv", np.column_stack([posx, posy, posz]), delimiter=",", header="x,y,z", comments='')
print("Position data saved to 'workspace_data.csv'.")
