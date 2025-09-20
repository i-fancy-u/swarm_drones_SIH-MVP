import numpy as np
from drone import Drone, DroneType
from sensing import get_local_view 
from constants import (
    R_SENSE, R_THREAT, R_SAFE_SEP, MAX_SPEED, ZERO_VECTOR, 
    MAX_ACCELERATION, DELTA_TIME 
) 

# --- HELPER FUNCTIONS ---

def calculate_steering_force(current_velocity, desired_velocity, max_acceleration):
    """Calculates the acceleration vector required to smoothly transition 
    from the current velocity to the desired velocity, limited by max_acceleration.
    """
    steering_force = desired_velocity - current_velocity
    force_magnitude = np.linalg.norm(steering_force)
    
    if force_magnitude > max_acceleration:
        steering_force = (steering_force / force_magnitude) * max_acceleration
        
    return steering_force

def get_coordination_vector(current_drone: Drone, friendlies: list):
    """Calculates the vector to maintain swarm cohesion and separation (Boids-like)."""
    cohesion_vec = ZERO_VECTOR
    separation_vec = ZERO_VECTOR
    
    if not friendlies:
        return ZERO_VECTOR

    # 1. Separation (Anti-Collision) - Strongest weight
    for other in friendlies:
        distance = current_drone.distance_to(other)
        if distance < R_SAFE_SEP:
            away_vector = current_drone.pos - other.pos
            # Force is inverse square of distance, but clamped to avoid singularities
            separation_vec += away_vector / (distance**2 + 1e-6)
            
    # 2. Cohesion (Move towards the center of the local friendly mass)
    center_of_mass = np.mean([f.pos for f in friendlies], axis=0)
    cohesion_vec = center_of_mass - current_drone.pos
    
    # Apply weights: Separation is much higher priority than Cohesion
    return separation_vec * 2.0 + cohesion_vec * 0.5

# --- CORE ALGORITHM ---

def get_move_vector(current_drone: Drone, all_drones: list) -> np.ndarray:
    
    # 1. Perception
    local_view = get_local_view(current_drone, all_drones)
    friendlies = local_view['friendlies'] 
    hostiles = local_view['hostiles']
    all_friendlies = [current_drone] + friendlies

    # 2. Base Coordination (Defensive/Formation Vector)
    swarm_vector = get_coordination_vector(current_drone, friendlies)
    
    # Reset target ID for this drone
    current_drone.target_id = -1
    
    # Initialize desired_velocity to the safe formation speed
    desired_velocity = swarm_vector
    
    if hostiles:
        
        # Identify AVAILABLE Hostiles (NOT neutralized and NOT claimed)
        available_hostiles = [
            h for h in hostiles 
            if not h.is_neutralized and not h.is_claimed
        ]
        
        if available_hostiles:
            
            # Sort available hostiles by closeness to THIS friendly drone
            available_hostiles.sort(key=lambda h: current_drone.distance_to(h))
            
            # Iterate only through potential threats
            for hostile in available_hostiles:
                h_dist = current_drone.distance_to(hostile)

                # Condition 1: Must be an immediate threat to trigger an attack
                if h_dist < R_THREAT:
                    
                    # Condition 2: Check if THIS drone is the best choice (Closest)
                    all_nearby_friendlies = [f for f in all_friendlies if not f.is_neutralized]
                    
                    min_friendly_dist_to_hostile = min(
                        f.distance_to(hostile) for f in all_nearby_friendlies
                    )
                    
                    # If I am the closest (or tied) *AND* the hostile is not claimed, I ATTACK.
                    if abs(h_dist - min_friendly_dist_to_hostile) < 1.0 and not hostile.is_claimed: 
                        
                        # 1. LOCK THE TARGET (CLAIMING):
                        hostile.is_claimed = True 
                        current_drone.target_id = hostile.id
                        
                        # 2. CALCULATE ATTACK VECTOR (Aggressive Pursuit)
                        TIME_TO_LEAD = 1.0 
                        hostile_future_pos = hostile.pos + hostile.velocity * TIME_TO_LEAD 
                        target_vector_raw = hostile_future_pos - current_drone.pos 
                        
                        # Normalize and scale to MAX_SPEED for desired velocity
                        if np.linalg.norm(target_vector_raw) > 0:
                            target_vector = target_vector_raw / np.linalg.norm(target_vector_raw)
                        else:
                            target_vector = ZERO_VECTOR
                        
                        # Desired velocity is aggressive attack vector + small influence from formation
                        desired_velocity = target_vector * MAX_SPEED * 0.95 + swarm_vector * 0.05
                        
                        break # Exit loop immediately after claiming/attacking

        # If no attack was triggered, desired_velocity remains the default swarm_vector.

    # 3. Apply Steering Force (Prevents Oscillation)
    steering_force = calculate_steering_force(
        current_drone.velocity, 
        desired_velocity, 
        MAX_ACCELERATION
    )
    
    # Calculate the new velocity
    new_velocity = current_drone.velocity + steering_force * DELTA_TIME
    
    # Final clamping to MAX_SPEED
    if np.linalg.norm(new_velocity) > MAX_SPEED:
        new_velocity = (new_velocity / np.linalg.norm(new_velocity)) * MAX_SPEED
    
    return new_velocity