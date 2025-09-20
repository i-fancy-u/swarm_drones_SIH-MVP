# scenario_data.py (Member F)

# Data format: (ID, POS_X, POS_Y, TYPE_STRING, [VEL_X, VEL_Y])

# Scenario: 3 Friendlies (F) vs 2 Hostiles (H)

INITIAL_DRONE_DATA = [
    # Friendly Swarm Start (near the center-left)
    (1, -100.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (2, -90.0, 10.0, 'FRIENDLY', [0.0, 0.0]),
    (3, -90.0, -10.0, 'FRIENDLY', [0.0, 0.0]),
    
    # Hostile Swarm Start (approaching from the right)
    (4, 150.0, 10.0, 'HOSTILE', [-15.0, 0.0]), # Incoming Threat 1
    (5, 140.0, -10.0, 'HOSTILE', [-15.0, 0.0]), # Incoming Threat 2
]

# scenario_data.py

# SCENARIO A: Immediate Handoff Test (New data for aggressive pursuit test)
SCENARIO_A = [
    (1, -5.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (2, 5.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (3, 10.0, 0.0, 'HOSTILE', [-15.0, 0.0]), # Hostile is moving fast
]

# SCENARIO B: Swarm Encircling / Dual Threat Test (Tests coordination and formation integrity)
SCENARIO_B = [
    (1, 0.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (2, 10.0, 10.0, 'FRIENDLY', [0.0, 0.0]),
    (3, 100.0, 50.0, 'HOSTILE', [-20.0, -5.0]), # Threat 1: High speed diagonal
    (4, 100.0, -50.0, 'HOSTILE', [-10.0, 5.0]), # Threat 2: Slower approach
]

# scenario_data.py

# ... (Previous SCENARIO_A and SCENARIO_B definitions) ...

# SCENARIO C: Overwhelm Test (5 Hostiles vs 3 Friendlies)
SCENARIO_C = [
    # Friendly Swarm (Small, defensive formation)
    (1, -5.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (2, 5.0, 0.0, 'FRIENDLY', [0.0, 0.0]),
    (3, 0.0, 10.0, 'FRIENDLY', [0.0, 0.0]),
    
    # Hostile Swarm (Larger, simple attack formation)
    (4, 150.0, 0.0, 'HOSTILE', [-18.0, 0.0]),  # Primary threat, fastest
    (5, 140.0, 15.0, 'HOSTILE', [-16.0, 0.0]), 
    (6, 140.0, -15.0, 'HOSTILE', [-16.0, 0.0]),
    (7, 130.0, 30.0, 'HOSTILE', [-14.0, 0.0]),
    (8, 130.0, -30.0, 'HOSTILE', [-14.0, 0.0]), # Secondary threat
]


# ------------------------------------------------------------------
# CRITICAL CONTROL LINE: 
INITIAL_DRONE_DATA = SCENARIO_C # <--- Select this line to run the test!
# ------------------------------------------------------------------