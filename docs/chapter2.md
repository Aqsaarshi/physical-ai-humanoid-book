# Chapter 2: Robotics Fundamentals

## 2.1 Definition of Robotics
Robotics is an interdisciplinary field that integrates computer science, engineering, and artificial intelligence to design, construct, operate, and apply robots. Robots are programmable machines capable of carrying out a complex series of actions automatically or semi-automatically. They are designed to interact with the physical world, often performing tasks that are dangerous, dull, dirty, or difficult for humans.

### What is a Robot?
A robot is typically defined as an autonomous or semi-autonomous electromechanical device that can sense its environment, process information, and perform physical actions. Modern definitions often emphasize programmability and the ability to adapt to varying conditions.

### Types of Robots
Robots come in various forms and are classified based on their application, mobility, or structure:
-   **Industrial Robots**: Used in manufacturing for tasks like assembly, welding, painting, and material handling (e.g., robotic arms).
-   **Mobile Robots**: Capable of moving in their environment, including wheeled robots (AGVs), legged robots (humanoids, quadrupeds), and aerial robots (drones).
-   **Humanoid Robots**: Designed to resemble the human body, often for human-robot interaction or tasks requiring human-like manipulation.
-   **Medical Robots**: Used in surgery (e.g., Da Vinci surgical system), rehabilitation, and patient care.
-   **Service Robots**: Perform tasks for humans in domestic or professional settings (e.g., vacuum cleaners, delivery robots).

## 2.2 Robot Anatomy
Understanding the physical structure of a robot is crucial for designing and controlling it. The anatomy typically includes manipulators, end-effectors, joints, and links.

### Manipulators
A manipulator is the 'arm' of a robot, consisting of a series of links connected by joints. Its purpose is to position and orient an end-effector at a desired location in the workspace.

### End-effectors
An end-effector is the tool or gripper attached to the last link of a robot manipulator. It is designed to interact with the environment to perform specific tasks, such as grasping objects, welding, or painting.

### Joints and Links
-   **Links**: These are the rigid bodies that make up the robot's structure (e.g., forearm, upper arm). They provide the physical framework.
-   **Joints**: These connect the links and allow relative motion between them. Common types include:
    -   **Revolute (Rotational) Joint**: Allows rotational motion around an axis (like a hinge).
    -   **Prismatic (Linear) Joint**: Allows translational motion along an axis (like a piston).

## 2.3 Robot Kinematics (Introduction)
Kinematics is the study of motion without considering the forces that cause it. In robotics, kinematics is fundamental for understanding how a robot's joints relate to the position and orientation of its end-effector.

### Forward Kinematics
Forward kinematics involves calculating the position and orientation of the end-effector given the known joint angles (or positions) of the robot. This is a direct calculation, typically using geometric transformations (rotation and translation matrices).

### Inverse Kinematics
Inverse kinematics is the reverse problem: calculating the required joint angles (or positions) to achieve a desired position and orientation of the end-effector. This is often more complex than forward kinematics as it can have multiple solutions, no solutions, or singularities.


## Example
### Forward Kinematics for a 2-DOF Planar Arm

**Concept**: This example illustrates how to calculate the end-effector position of a simple 2-Degrees-Of-Freedom (DOF) planar robot arm using forward kinematics. A planar arm moves in a 2D plane.

**Robot Description**:
-   Two links, `L1` and `L2`.
-   Two revolute joints, `θ1` and `θ2`.
-   `L1` is connected to the base by joint `θ1`.
-   `L2` is connected to the end of `L1` by joint `θ2`.

**Assumptions**:
-   The base of the robot is at the origin (0,0).
-   Angles `θ1` and `θ2` are measured from the positive X-axis.

**Calculations**:
Let the coordinates of the end of `L1` be `(x1, y1)` and the end-effector (end of `L2`) be `(xe, ye)`.

1.  **Position of the end of L1**:
    -   `x1 = L1 * cos(θ1)`
    -   `y1 = L1 * sin(θ1)`

2.  **Position of the end-effector (xe, ye)**:
    To find the end-effector position, we add the contribution of `L2` relative to `L1`.
    -   `xe = x1 + L2 * cos(θ1 + θ2)`
    -   `ye = y1 + L2 * sin(θ1 + θ2)`

**Practical Application**: If `L1 = 1m`, `L2 = 0.5m`, `θ1 = 30°` (`π/6 rad`), `θ2 = 60°` (`π/3 rad`):
-   `x1 = 1 * cos(π/6) ≈ 0.866 m`
-   `y1 = 1 * sin(π/6) = 0.5 m`

-   `xe = 0.866 + 0.5 * cos(π/6 + π/3) = 0.866 + 0.5 * cos(π/2) = 0.866 + 0.5 * 0 = 0.866 m`
-   `ye = 0.5 + 0.5 * sin(π/6 + π/3) = 0.5 + 0.5 * sin(π/2) = 0.5 + 0.5 * 1 = 1.0 m`

Thus, the end-effector is approximately at `(0.866 m, 1.0 m)`.

This example demonstrates how known joint angles and link lengths can be used to determine the exact position of a robot's tool center point.
## Diagram

### Figure 2.1: 2-DOF Planar Robot Arm Anatomy

**Description**: A line drawing illustrating a 2-DOF planar robot arm. It should show:
1.  **Base**: Fixed at the origin.
2.  **Joint 1 (θ1)**: A revolute joint at the base, allowing rotation of Link 1.
3.  **Link 1 (L1)**: A rigid body extending from Joint 1.
4.  **Joint 2 (θ2)**: A revolute joint at the end of Link 1, allowing rotation of Link 2 relative to Link 1.
5.  **Link 2 (L2)**: A rigid body extending from Joint 2.
6.  **End-Effector**: At the end of Link 2.

Angles `θ1` and `θ2` should be clearly labeled, along with lengths `L1` and `L2`. Coordinate axes (X and Y) should also be shown for reference.

## Mini-Task

### Analyze a Robot's Joint Types

**Objective**: Examine a real-world robot and identify its joint types and their degrees of freedom.

**Instructions**:
1.  **Choose a robot**: Select a robot (e.g., a robotic arm from a manufacturing video, a humanoid robot, or even a toy robot).
2.  **Identify joints**: For each moving part, determine if the joint is revolute (rotational) or prismatic (linear).
3.  **Count DOFs**: Sum the degrees of freedom for all joints to determine the total DOFs of the robot's manipulator.

**Example**: For a simple SCARA robot, you might identify two revolute joints for planar movement and one prismatic joint for vertical movement, totaling 3 DOFs for manipulation.

## Quiz

1.  Which of the following fields is *not* a primary component of robotics?
    a)  Computer Science
    b)  Engineering
    c)  Artificial Intelligence
    d)  Astrology
    *Answer: d)*

2.  What is the primary function of a robot's end-effector?
    a)  To control the robot's internal power supply.
    b)  To sense the robot's joint angles.
    c)  To interact with the environment to perform specific tasks.
    d)  To provide structural support to the robot arm.
    *Answer: c)*

3.  A joint that allows rotational motion around an axis is called a:
    a)  Prismatic joint
    b)  Revolute joint
    c)  Fixed joint
    d)  Spherical joint
    *Answer: b)*

4.  The process of calculating the end-effector position given the known joint angles is known as:
    a)  Inverse kinematics
    b)  Forward dynamics
    c)  Inverse dynamics
    d)  Forward kinematics
    *Answer: d)*

5.  Which of the following is often more complex in robotics, potentially having multiple solutions or singularities?
    a)  Forward Kinematics
    b)  Forward Dynamics
    c)  Inverse Kinematics
    d)  Inverse Dynamics
    *Answer: c)*

## References

-   Siciliano, B., Khatib, O., & SpringerLink. (2016). *Springer Handbook of Robotics* (2nd ed.). Springer.
-   Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. John Wiley & Sons.
-   Corke, P. I. (2017). *Robotics, Vision and Control: Fundamental Algorithms in MATLAB*. Springer.
-   Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Prentice Hall.
