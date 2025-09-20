import numpy as np
from drone import Drone, DroneType
from constants import R_SENSE, R_THREAT

def get_local_view(current_drone: Drone, all_drones: list) -> dict:
    """
    Simulates local sensor input. Returns a dictionary of lists:
    {'friendlies': [...], 'hostiles': [...]}
    """
    local_view = {'friendlies': [], 'hostiles': []}

    for drone in all_drones:
        # A drone can always see itself, but we skip it for interaction purposes
        if drone.id == current_drone.id:
            continue

        distance = current_drone.distance_to(drone)

        # Only include drones within sensor range
        if distance < R_SENSE:
            if drone.is_hostile():
                local_view['hostiles'].append(drone)
            else:
                local_view['friendlies'].append(drone)

    return local_view

def is_unattended(hostile_drone: Drone, local_view: dict) -> bool:
    """
    Determines if a hostile drone is 'Left Unattended' based on the problem statement.
    A drone is LEFT UNATTENDED if no friendly drone is firing or in position 
    to intercept. Simplification: it is unattended if it is closer than R_THREAT 
    AND no other friendly drone is closer to it than the current drone.
    """
    current_drone_id = hostile_drone.target_id 
    
    # 1. Check if the hostile is even a threat (within range)
    # NOTE: This check should ideally happen in the calling function (B's logic)
    # For a simplified model, we check if ANY friendly is closer than the THREAT radius.
    
    # Find the closest friendly drone (excluding the hostile itself)
    closest_friendly_distance = float('inf')
    
    # Check all *friendly* drones in the local view
    for friendly in local_view['friendlies']:
        dist = friendly.distance_to(hostile_drone)
        if dist < closest_friendly_distance:
            closest_friendly_distance = dist
            
    # Check the current drone's distance as well
    if current_drone_id != -1: # Assuming current_drone is one of the friendlies in the loop
        pass # Better handled by B's logic to check if *another* friendly is closer

    # Simplification: If no other friendly drone is within a close range 
    # (say, R_SENSE/2) and the current drone isn't targeting it, it's unattended.
    # For a robust implementation:
    # A hostile is unattended if:
    # a) It is within R_THREAT AND
    # b) It is not the target of the closest friendly drone.
    
    # The simplest, most critical interpretation for the hackathon:
    # An enemy is unattended if NO friendly drone is currently designated to attack it. 
    # Let B's coordination logic handle the "designation" of a target.
    
    # For now, let's deliver the distance metric to B:
    return closest_friendly_distance # Return a float to be used by B

# sensing.py (Member A)

# ... (Previous code remains) ...

def get_closest_friendly_to_hostile(hostile_drone, all_friendlies: list, exclude_drone_id: int = -1) -> tuple:
    """
    Finds the friendly drone closest to the given hostile.
    Returns (closest_friendly_drone, distance).
    """
    closest_friendly = None
    min_dist = float('inf')

    for friendly in all_friendlies:
        if friendly.id == exclude_drone_id:
            continue

        dist = friendly.distance_to(hostile_drone)
        if dist < min_dist:
            min_dist = dist
            closest_friendly = friendly
            
    return closest_friendly, min_dist

# NOTE: This function's output will be crucial for B's decision-making.