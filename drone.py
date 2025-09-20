import numpy as np
from enum import Enum

# Define the two types of units
class DroneType(Enum):
    FRIENDLY = 1
    HOSTILE = 2

class Drone:
    def __init__(self, id, pos, velocity=None, type=DroneType.FRIENDLY):
        self.id = id
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity or [0.0, 0.0], dtype=float)
        self.type = type
        self.target_id = -1 # ID of the hostile drone this drone is currently targeting
        self.is_neutralized = False # NEW: Flag to indicate it has been hit
        self.blink_timer = 0.0      # NEW: Timer for blinking effect

    def distance_to(self, other_drone):
        """Calculates the Euclidean distance to another drone."""
        return np.linalg.norm(self.pos - other_drone.pos)

    def is_hostile(self):
        return self.type == DroneType.HOSTILE

    def __repr__(self):
        return f"Drone(ID={self.id}, Type={self.type.name}, Pos={self.pos.round(1)})"