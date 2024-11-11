import random

# Définition de la taille de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Génération d'une position aléatoire pour le trésor
TREASURE_POSITION = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def mark_treasure_collected():
    """Marque le trésor comme collecté en le retirant de la carte."""
    global TREASURE_POSITION
    TREASURE_POSITION = None
