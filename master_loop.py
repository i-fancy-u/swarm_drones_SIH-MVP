import pygame
import numpy as np
import time # Needed for the final stability fix

# Imports from constants, scenario_data
from constants import MAX_SPEED, R_INTERCEPT, DELTA_TIME
from scenario_data import INITIAL_DRONE_DATA 

# Imports from A & B (Logic)
from drone import Drone, DroneType
from coordination import get_move_vector 

# Imports from D (Visualization)
from visualization import draw_simulation, setup_display, set_screen_mode

# --- GLOBAL VARIABLES ---
is_paused = False 
running = True 
FPS = 30 # Set a safe maximum FPS

# --- C1: Initialization ---
def initialize_drones():
    """Converts F's raw data into a list of Drone objects."""
    drones = []
    for data in INITIAL_DRONE_DATA:
        d_type = DroneType.FRIENDLY if data[3] == 'FRIENDLY' else DroneType.HOSTILE
        # data[4] is the initial velocity vector
        drones.append(Drone(id=data[0], pos=[data[1], data[2]], velocity=data[4], type=d_type))
    return drones

# --- C2: Physics & Engagement ---
def handle_physics_update(drones):
    """Updates the position of ALL drones and checks engagement, removing both involved parties."""
    hostiles_to_remove = []
    friendlies_to_remove = []
    
    for drone_i in drones:
        
        # Skip physics for any drone already scheduled for removal this tick
        if drone_i.is_neutralized: 
            drone_i.blink_timer += DELTA_TIME
            continue

        # 1. Update Position
        drone_i.pos += drone_i.velocity * DELTA_TIME

        # 2. Check Engagement (Hostile vs. Friendly)
        if drone_i.is_hostile():
            for drone_j in drones:
                # Check against live friendly drones that aren't already marked for removal
                if not drone_j.is_hostile() and not drone_j.is_neutralized:
                    
                    if drone_i.distance_to(drone_j) < R_INTERCEPT:
                        
                        # Hostile is neutralized (Set blink flag)
                        if not drone_i.is_neutralized:
                            drone_i.is_neutralized = True
                            
                        # Friendly drone is also sacrificed (Mark for removal)
                        if drone_j not in friendlies_to_remove: 
                            friendlies_to_remove.append(drone_j) 

                        print(f"Engagement: Hostile {drone_i.id} neutralized, Friendly {drone_j.id} lost.")
                        break # Move to the next hostile drone

    # Final cleanup of removed drones (This logic is simpler for the hackathon)
    drones[:] = [d for d in drones if d not in friendlies_to_remove]
    
    # Clean up neutralized hostiles that have finished blinking (or just remove them)
    drones[:] = [d for d in drones if not d.is_neutralized or d.blink_timer < 0.5]
    
    return drones

# --- C3: The Master Loop ---
def main_simulation_loop():
    global is_paused, running # Declare globals
    
    # 1. SETUP DISPLAY (The fix for the hang)
    setup_display() 
    time.sleep(0.1) 
    screen = set_screen_mode() 
    
    drones = initialize_drones()
    clock = pygame.time.Clock()
    
    simulation_active = True
    simulation_time = 0.0

    while running:
        
        # 1. EVENT HANDLING (MUST BE FIRST)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                    print(f"Simulation {'PAUSED' if is_paused else 'RESUMED'}. Time: {simulation_time:.2f}s")
        
        # 2. RUN LOGIC ONLY IF NOT PAUSED AND SIMULATION IS ACTIVE
        if not is_paused and simulation_active:
            
            # --- CRITICAL FIX: RESET TARGET CLAIM FLAGS ---
            for drone in drones:
                if drone.is_hostile():
                    drone.is_claimed = False
            # ---------------------------------------------

            # --- CHECK END CONDITION ---
            if not any(d.is_hostile() for d in drones):
                simulation_active = False
                print("All hostiles neutralized. Simulation finished.")
                
            
            if simulation_active:
                # 3. ALGORITHM INTEGRATION 
                new_velocities = {}
                for drone in drones:
                    if drone.is_hostile():
                        new_velocities[drone.id] = drone.velocity
                    elif not drone.is_neutralized:
                        new_velocities[drone.id] = get_move_vector(drone, drones)
                    
                # Apply the new velocities
                for drone in drones:
                    if drone.id in new_velocities:
                        drone.velocity = new_velocities[drone.id]

                # 4. STATE UPDATE 
                drones = handle_physics_update(drones)
                simulation_time += DELTA_TIME
        
        # 5. VISUALIZATION (Runs always to show final state)
        draw_simulation(drones, is_paused=is_paused, time=simulation_time) 

        # 6. Control Speed
        clock.tick(FPS) 
        
    pygame.quit()

if __name__ == "__main__":
    main_simulation_loop()