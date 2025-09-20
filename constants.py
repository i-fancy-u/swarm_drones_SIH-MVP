import numpy as np

# Simulation Time Step (Coordinated with Member C)
DELTA_TIME = 0.1  # Seconds per simulation tick

# Drone Capabilities
MAX_SPEED = 30.0  # Units/sec (e.g., m/s)
MAX_ACCELERATION = 10.0 # Units/sec^2

# Range Constants (Coordinated with Member F)
R_SENSE = 100.0   # Sensing Range (Radius for Lidar/Radar perception)
R_THREAT = 30.0   # Threatening Range (1 second of flight at max speed)
R_INTERCEPT = 5.0 # Effective 'kill' distance (collision/proximity fuse)
R_SAFE_SEP = 10.0 # Minimum distance between friendly drones (anti-collision)

# Vector Constants
ZERO_VECTOR = np.array([0.0, 0.0])