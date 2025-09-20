# visualization.py (Member D - CORRECTED FINAL VERSION)

import pygame
import time
# Ensure constants and drone class are available for drawing
from constants import R_SENSE, R_THREAT, R_INTERCEPT 
from drone import Drone, DroneType

# Define Display Constants (Must be defined globally)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FIELD_SCALE = 4 
RADIUS = 5 

# Colors (Ensure these are defined globally)
COLOR_BACKGROUND = (10, 10, 40)
COLOR_FRIENDLY = (0, 255, 0)
COLOR_HOSTILE = (255, 0, 0)
COLOR_SENSE = (50, 50, 150)
COLOR_THREAT = (150, 50, 50)
COLOR_TARGET_LINE = (255, 255, 255)

screen = None
FONT = None

# -----------------------------------------------------------------
# INITIALIZATION FUNCTIONS
# -----------------------------------------------------------------
def setup_display():
    """Initializes Pygame subsystems and font."""
    global FONT
    pygame.init() 
    
    try:
        FONT = pygame.font.Font(None, 36)
    except pygame.error:
        FONT = None
    return 

def set_screen_mode():
    """Sets the screen mode AFTER a brief delay in the master loop."""
    global screen
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Coordinated Swarm Engagement MVP")
    
    # CRITICAL: Force the display to update the window immediately
    pygame.display.update() 
    return screen

# -----------------------------------------------------------------
# DRAWING HELPER FUNCTIONS (Place draw_drone and draw_text here)
# -----------------------------------------------------------------

def sim_to_screen(sim_pos):
    """Converts simulation coordinates (x, y) to screen pixels (px, py)."""
    px = int(sim_pos[0] * FIELD_SCALE + SCREEN_WIDTH / 2)
    py = int(-sim_pos[1] * FIELD_SCALE + SCREEN_HEIGHT / 2)
    return (px, py)

def draw_text(text, position, color=(255, 255, 255)):
    """Helper function to draw text on the screen."""
    global screen
    if FONT:
        text_surface = FONT.render(text, True, color)
        screen.blit(text_surface, position)

def draw_drone(drone: Drone, all_drones: list):
    """Draws a single drone, its sensor range, and its target line."""
    global screen
    
    # --- NEW BLINKING LOGIC ---
    if drone.is_neutralized:
        # Blink effect: only draw the drone half the time
        if int(drone.blink_timer * 10) % 2 == 0: 
            return # Skip drawing this frame to make it flash
        color = (255, 255, 255) # Draw white flash
    elif drone.is_hostile():
        color = COLOR_HOSTILE
    else:
        color = COLOR_FRIENDLY
        
    screen_pos = sim_to_screen(drone.pos)

    # 1. Draw Threat/Sensor Ranges (Simplified, only for live drones)
    if not drone.is_neutralized:
        # Draw Sensor Range
        if not drone.is_hostile():
             pygame.draw.circle(screen, COLOR_SENSE, screen_pos, int(R_SENSE * FIELD_SCALE), 1)
        # Draw Threat Range (often around hostiles)
        # pygame.draw.circle(screen, COLOR_THREAT, screen_pos, int(R_THREAT * FIELD_SCALE), 1)

    # 2. Draw the Drone (Dot)
    pygame.draw.circle(screen, color, screen_pos, RADIUS)
    
    # 3. Draw Target Line
    if drone.target_id != -1 and not drone.is_hostile():
        target_drone = next((d for d in all_drones if d.id == drone.target_id), None)
        if target_drone and not target_drone.is_neutralized:
            target_pos = sim_to_screen(target_drone.pos)
            pygame.draw.line(screen, COLOR_TARGET_LINE, screen_pos, target_pos, 1)


# -----------------------------------------------------------------
# CRITICAL: MAIN DRAWING LOOP FUNCTION
# -----------------------------------------------------------------
def draw_simulation(drones: list, is_paused: bool = False, time: float = 0.0):
    """Clears the screen and draws all elements."""
    global screen

    # ERROR WAS HERE: screen must be initialized by master_loop BEFORE this call.
    if screen is None:
        # Emergency exit/print if screen is somehow still None
        print("FATAL DRAWING ERROR: Screen surface not initialized. Cannot draw.")
        return 

    screen.fill(COLOR_BACKGROUND) 
    
    # 1. Draw all drones
    for drone in drones:
        draw_drone(drone, drones) 
        
    # 2. Draw HUD (Runs always to show status)
    friendly_count = sum(1 for d in drones if not d.is_hostile() and not d.is_neutralized)
    hostile_count = sum(1 for d in drones if d.is_hostile() and not d.is_neutralized)
    
    draw_text(f"Friendlies: {friendly_count}", (10, 10), COLOR_FRIENDLY)
    draw_text(f"Hostiles: {hostile_count}", (10, 40), COLOR_HOSTILE)
    draw_text(f"Time: {time:.2f}s", (10, 70), (200, 200, 200))
    
    if is_paused:
        draw_text("PAUSED (SPACE)", (SCREEN_WIDTH - 300, 10), (255, 255, 0))

    # 3. Final display flip to update the monitor
    pygame.display.flip()