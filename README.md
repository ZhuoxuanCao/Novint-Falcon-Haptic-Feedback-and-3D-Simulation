# Haptic Interaction with Novint Falcon & 3D Simulation

## **Project Overview**
This project explores haptic interaction methods using the **Novint Falcon** haptic device, focusing on force feedback implementation and integration with a 3D simulation environment using **Blender**. The project consists of two primary parts:

### **Part 1: Novint Falcon Exploration**
1. **Workspace Analysis:**  
   - Determined the physical workspace dimensions of the Falcon by manually recording extreme positions along each axis.
   
2. **Virtual Spring-Damper System:**  
   - Implemented a force feedback model to simulate spring and damping effects, evaluating system response under varying damping coefficients.

3. **Dynamic System Identification:**  
   - Conducted free oscillation experiments to estimate key dynamic parameters such as damping ratio, natural frequency, and equivalent mass.

4. **Virtual Environment Implementation:**  
   - Developed force feedback simulations for virtual objects including:
     - Virtual walls (rigid, linear, and nonlinear force models)
     - Spheres and cylinders for complex interaction scenarios
     - Rough and sinusoidal surfaces for advanced feedback simulation

5. **Clickable Slider Mechanism:**  
   - Designed a virtual slider with a tactile click sensation to enhance the haptic experience.

---

### **Part 2: 3D Simulation Coupling**
1. **Direct Coupling Method:**  
   - Implemented direct force feedback between the Falcon and Blender, allowing real-time movement tracking and force response.

2. **Indirect Coupling Approach:**  
   - Introduced a virtual spring-damper system to mediate interactions, improving stability and realism in haptic feedback.

3. **Comparison of Coupling Strategies:**  
   - Analyzed the advantages and limitations of **Direct Haptic Assistance (DHA)** and **Indirect Haptic Assistance (IHA)**, assessing their impact on interaction quality and system performance.

---

## **Key Technologies**
- **Hardware:** Novint Falcon (3-DOF Haptic Device)
- **Software:** Python, Blender (3D simulation), haptic control libraries
- **Methodologies:** Force feedback modeling, system dynamics analysis, experimental evaluation

## **Results and Observations**
- Evaluated the Falcon's workspace and dynamic properties through experimental testing.
- Implemented multiple force feedback strategies to simulate realistic haptic interactions.
- Observed that nonlinear feedback models provide the best balance of stability and realism.
- Identified that indirect coupling with a 3D simulator enhances stability compared to direct coupling but requires more computational resources.

## **Future Work**
- Optimize the haptic rendering algorithms for real-time applications.
- Explore machine learning-based approaches for adaptive force feedback.
- Extend the system to support multi-DOF haptic interactions for immersive VR/AR applications.

