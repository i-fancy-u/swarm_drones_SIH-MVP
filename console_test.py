import numpy as np
from drone import Drone, DroneType
from coordination import get_move_vector
from constants import DELTA_TIME, MAX_SPEED, R_INTERCEPT

def run_test_scenario():
    """Simulates a 2 Friendly vs 1 Hostile scenario for a few steps."""
    
    # Define Scenario: 
    # Friendly 1: Attacker
    # Friendly 2: Defender (farther away)
    # Hostile: Incoming threat
    
    drones = [
        Drone(id=1, pos=[0.0, 0.0], type=DroneType.FRIENDLY),
        Drone(id=2, pos=[50.0, 50.0], type=DroneType.FRIENDLY),
        Drone(id=3, pos=[120.0, 0.0], velocity=[-20.0, 0.0], type=DroneType.HOSTILE) # Incoming
    ]
    
    print("--- Initial State ---")
    for d in drones:
        print(d)

    NUM_STEPS = 10 
    for step in range(1, NUM_STEPS + 1):
        
        # Calculate new velocities for FRIENDLY drones (using A & B's core function)
        friendly_moves = {}
        for d in drones:
            if d.is_hostile():
                continue # Hostiles move according to their own simple logic
            
            # Get the desired next velocity from our algorithm
            desired_velocity = get_move_vector(d, drones)
            
            # Simple physics: apply this as the new velocity (ignoring acceleration limits for this simple test)
            friendly_moves[d.id] = desired_velocity

        # Update all drone positions (Simple Euler integration)
        for d in drones:
            if d.is_hostile():
                # Simple Hostile Logic: Keep its current velocity
                d.pos += d.velocity * DELTA_TIME
            else:
                d.velocity = friendly_moves[d.id]
                d.pos += d.velocity * DELTA_TIME

        # Print Status
        print(f"\n--- Step {step} / {NUM_STEPS} ---")
        for d in drones:
            # Check for engagement (simple collision)
            if d.is_hostile() and d.distance_to(drones[0]) < R_INTERCEPT:
                 print(f"!!! ENGAGEMENT: Hostile {d.id} neutralized by F1!")
                 drones.remove(d)
                 break
            print(f"[{d.type.name}] ID={d.id} Pos={d.pos.round(1)}, Target={d.target_id}")
            
if __name__ == "__main__":
    run_test_scenario()

# console_test.py (A & B)

# ... (Import and setup remains the same) ...

def run_handoff_scenario():
    """Simulates 3 Friendlies vs 1 Hostile to test that only F1 attacks."""
    
    drones = [
        # F1: Closest attacker (should engage)
        Drone(id=1, pos=[10.0, 0.0], type=DroneType.FRIENDLY), 
        # F2: Closer to F1 (cohesion/separation) but farther from H (should defend/form)
        Drone(id=2, pos=[15.0, 5.0], type=DroneType.FRIENDLY), 
        # F3: Out of range (should only care about swarm cohesion)
        Drone(id=3, pos=[80.0, 50.0], type=DroneType.FRIENDLY), 
        # Hostile H: Incoming threat within R_THREAT of F1 and F2
        Drone(id=4, pos=[40.0, 0.0], velocity=[-10.0, 0.0], type=DroneType.HOSTILE) 
    ]
    
    print("--- Testing Handoff (F1 should attack, F2 should defend/follow) ---")

    NUM_STEPS = 5 
    for step in range(1, NUM_STEPS + 1):
        # ... (Movement calculation loop remains the same) ...
        # ... (Position update loop remains the same) ...
        
        print(f"\n--- Step {step} ---")
        for d in drones:
             # ... (Engagement check) ...
             # CRITICAL CHECK: Print the target ID to confirm handoff!
             print(f"[{d.type.name}] ID={d.id} Pos={d.pos.round(1)}, **Target={d.target_id}**")
             
if __name__ == "__main__":
    run_handoff_scenario() # Run the new test