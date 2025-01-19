from pyDhd import *
import numpy as np
import matplotlib.pyplot as plt

# Initialize the device
dhdOpen()
print("Device initialized. Press the device button to finish.")

# Spring and damping parameters
k = 800  # Spring stiffness coefficient
c = 20    # Damping coefficient

# Data storage lists
posx, posy, posz = [], [], []  # Handle position
forcex, forcey, forcez = [], [], []  # Applied force
time_steps = []  # Time recording

# Initialize variables
done = False
time_step = 0

# Main loop: Simulate virtual spring and damper
while not done:
    ret, px, py, pz = dhdGetPosition()  # Get handle position
    ret, velx, vely, velz = dhdGetLinearVelocity()  # Get handle velocity

    if ret == 0:  # Check if device reading is successful
        # Compute virtual force
        fx = -k * px - c * velx
        fy = -k * py - c * vely
        fz = -k * pz - c * velz

        # Record data
        posx.append(px)
        posy.append(py)
        posz.append(pz)
        forcex.append(fx)
        forcey.append(fy)
        forcez.append(fz)
        time_steps.append(time_step)

        # Apply force to the device
        dhdSetForce(fx, fy, fz)

        # Output debug information
        print(f"Time: {time_step} | Position: ({px:.2f}, {py:.2f}, {pz:.2f}) | Force: ({fx:.2f}, {fy:.2f}, {fz:.2f})")

        # Update time
        time_step += 1

    # Check exit condition
    done = dhdGetButton(0)

# Close the device
dhdClose()
print("Device closed.")

# Plotting section
plt.figure("Position vs Force (X-axis)")
plt.plot(posx, forcex, label="X-axis", color='red')
plt.xlabel("Position (m)")
plt.ylabel("Force (N)")
plt.title(f"Position vs Force (X-axis) (k={k}, c={c})")  # Dynamically add stiffness and damping information
plt.grid(True)
plt.legend()

plt.figure("Position over Time")
plt.plot(time_steps, posx, label="X-axis", color='red')
plt.plot(time_steps, posy, label="Y-axis", color='blue')
plt.plot(time_steps, posz, label="Z-axis", color='green')
plt.xlabel("Time Steps")
plt.ylabel("Position (m)")
plt.title(f"Position vs Time (k={k}, c={c})")  # Dynamically add stiffness and damping information
plt.grid(True)
plt.legend()

plt.figure("Force over Time")
plt.plot(time_steps, forcex, label="X-axis", color='red')
plt.plot(time_steps, forcey, label="Y-axis", color='blue')
plt.plot(time_steps, forcez, label="Z-axis", color='green')
plt.xlabel("Time Steps")
plt.ylabel("Force (N)")
plt.title(f"Force vs Time (k={k}, c={c})")  # Dynamically add stiffness and damping information
plt.grid(True)
plt.legend()

plt.show()

# # Save data to file
# np.savetxt("spring_damper_data.csv", np.column_stack([time_steps, posx, posy, posz, forcex, forcey, forcez]),
#            delimiter=",", header="time,posx,posy,posz,forcex,forcey,forcez", comments='')
# print("Data saved to 'spring_damper_data.csv'.")
