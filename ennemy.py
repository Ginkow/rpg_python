import random
import inventory

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Enemy class
class Enemy:
    def __init__(self, name, health, max_health, attack, defense, position, level):
        # Initialize enemy attributes
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.position = position
        self.alive = True
        self.level = level

    def is_alive(self):
        """Check if the enemy is still alive."""
        return self.health > 0 and self.alive

    def attack_player(self, player):
        """Attack the player, reducing shield first if applicable, then health."""
        # Calculate the damage dealt by the enemy
        damage = self.attack
        if damage < 1: 
            damage = 1

        # Reduce player’s shield first, then health if shield is depleted
        if player.defense > 0:
            if damage >= player.defense:
                damage -= player.defense
                player.defense = 0 
                player.health -= damage
            else:
                player.defense -= damage
        else:
            player.health -= damage

        return damage

    def generate_loot(self):
        """Generate loot based on rarity with different probabilities."""
        # Define items by rarity
        common = [inventory.pv_min, inventory.deg_min, inventory.harpon, inventory.arc]
        epic = [inventory.pv_mid, inventory.deg_mid, inventory.gun]
        legendary = [inventory.pv_max, inventory.deg_max]

        rarity_roll = random.random()

        # 60% chance for a common item
        if rarity_roll <= 0.6:
            loot = random.choice(common)
        # 30% chance for an epic item
        elif rarity_roll <= 0.9:
            loot = random.choice(epic)
        # 10% chance for a legendary item
        else:
            loot = random.choice(legendary)

        return [loot]
    
    def defeat(self):
        """Mark the enemy as defeated and remove its position."""
        self.alive = False
        self.position = None

def generate_unique_position(existing_positions):
    """Generate a unique position on the grid, avoiding occupied and forbidden positions."""
    forbidden_positions = [(0, 0), (5, 5)]
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # Ensure the new position is not in forbidden positions or already occupied
        if position not in existing_positions and position not in forbidden_positions:
            return position

positions = set()
enemies = []

# Create three Goblins with unique positions
for i in range(1, 4): 
    GOBELIN_POSITION = generate_unique_position(positions)
    positions.add(GOBELIN_POSITION)
    gobelin_name = f"Gobelin {i}"
    enemies.append(Enemy(gobelin_name, 50, 50, 10, 10, GOBELIN_POSITION, 15))

# Create two Orcs with unique positions
for i in range(1, 3):
    ORC_POSITION = generate_unique_position(positions)
    positions.add(ORC_POSITION)
    orc_name = f"Orc {i}"
    enemies.append(Enemy(orc_name, 75, 75, 15, 25, ORC_POSITION, 30))

# Create two Elves with unique positions
for i in range(1, 3):
    ELFE_POSITION = generate_unique_position(positions)
    positions.add(ELFE_POSITION)
    elfe_name = f"Elfe {i}"
    enemies.append(Enemy(elfe_name, 100, 100, 20, 15, ELFE_POSITION, 25))
