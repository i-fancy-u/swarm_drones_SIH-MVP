# 🚀 Swarm Drome Project: Decentralized Swarm Engagement Algorithm (DSEA)

## 💡 Problem Statement
[cite_start]Designing an Efficient Algorithm for Coordinated Swarm Engagement among Autonomous Drones aiming to neutralize an adversarial drone swarm[cite: 3].

## ✨ Solution Overview: The DSEA
[cite_start]The DSEA is a **Decentralized Swarm Algorithm for Counter-Drone Engagement** built to protect critical ground assets by autonomously intercepting hostile drone swarms[cite: 8, 14]. [cite_start]Our core innovation lies in creating a swarm that operates completely on **local decision-making without central control**, ensuring resilience in communication-denied environments[cite: 11, 16, 18].

### Key Innovations
* [cite_start]**Fully Decentralized Logic:** Each drone makes autonomous decisions based only on local sensor data (simulated Radar, LiDAR, Vision)[cite: 10, 18].
* [cite_start]**Adaptive Threat Assessment:** The algorithm includes a dynamic **Target Claiming** and coordination logic to prevent redundant attacks and ensure no enemy drone with ground attack capability is left unattended[cite: 15, 19].
* [cite_start]**Feasibility & Validation:** The algorithm is validated using a **stochastic simulation framework** that tests multiple threat scenarios[cite: 12, 20].

## 🛠️ Technical Stack (MVP)

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Programming Language** | [cite_start]**Python** [cite: 27] | Rapid prototyping and core logic implementation. |
| **Vector Math** | **NumPy** | Efficient handling of drone positions and velocity vectors. |
| **Simulation/Visualization** | **Pygame** | Simple, fast 2D visual representation of the engagement. |
| **Future Framework** | [cite_start]ROS, Gazebo [cite: 28] | Planned integration for advanced 3D physics and real-world deployment. |

## 📁 Project Structure

The project uses a simple, flat structure for rapid hackathon deployment:
## 💻 How to Run the MVP

### Prerequisites
You need Python 3.x installed.

1.  **Install Dependencies:**
    ```bash
    pip install numpy pygame
    ```

2.  **Execute the Simulation:**
    Run the master loop to start the visualization.
    ```bash
    python master_loop.py
    ```

The simulation will load the pre-configured scenario, and the friendly swarm will autonomously attempt to intercept and neutralize the adversarial swarm using the DSEA logic implemented in `coordination.py`.