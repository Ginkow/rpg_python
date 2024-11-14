import random

# Define grid size
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Forbidden positions where the treasure cannot be placed
FORBIDDEN_POSITIONS = [(0, 0), (5, 5)]

# Generate a random position for the treasure, avoiding forbidden positions
def generate_treasure_position():
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in FORBIDDEN_POSITIONS:
            return position

# Initial generation of the treasure position
TREASURE_POSITION = generate_treasure_position()

def mark_treasure_collected():
    """Marks the treasure as collected by removing it from the map."""
    global TREASURE_POSITION
    TREASURE_POSITION = None 
