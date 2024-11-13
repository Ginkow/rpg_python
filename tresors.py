import random

# Définition de la taille de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Positions interdites pour le trésor
FORBIDDEN_POSITIONS = [(0, 0), (5, 5)]

# Génération d'une position aléatoire pour le trésor en évitant les positions interdites
def generate_treasure_position():
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in FORBIDDEN_POSITIONS:
            return position

# Génération de la position du trésor
TREASURE_POSITION = generate_treasure_position()

def mark_treasure_collected():
    """Marque le trésor comme collecté en le retirant de la carte."""
    global TREASURE_POSITION
    TREASURE_POSITION = None
