import random
import inventory

# Dimensions de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Classe Enemy
class Enemy:
    def __init__(self, name, health, max_health, attack, defense, position, level):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.position = position
        self.alive = True
        self.level = level

    def is_alive(self):
        return self.health > 0  and self.alive

    def attack_player(self, player):
        # Calcul des dégâts infligés par l'ennemi
        damage = self.attack
        if damage < 1:  # Assurer que les dégâts minimum sont de 1
            damage = 1

        # Si le joueur a du bouclier, les dégâts vont d'abord réduire le bouclier
        if player.defense > 0:
            if damage >= player.defense:
                damage -= player.defense
                player.defense = 0  # Bouclier épuisé
                player.health -= damage  # Dégâts restants affectent la santé
            else:
                player.defense -= damage
        else:
            player.health -= damage  # Dégâts affectent directement la santé

        return damage

    def generate_loot(self):
        # Objets par rareté
        commune = [inventory.pv_min, inventory.deg_min, inventory.harpon, inventory.arc]
        epic = [inventory.pv_mid, inventory.deg_mid, inventory.gun]
        legendary = [inventory.pv_max, inventory.deg_max]

        rarity_roll = random.random()

        # 60% de chance pour un objet commun
        if rarity_roll <= 0.6:
            loot = random.choice(commune)
        # 30% de chance pour un objet épique
        elif rarity_roll <= 0.9:
            loot = random.choice(epic)
        # 10% de chance pour un objet légendaire
        else:
            loot = random.choice(legendary)

        return [loot]
    
    def defeat(self):
        """Marque l'ennemi comme vaincu et enlève sa position."""
        self.alive = False
        self.position = None

# Fonction pour générer une position unique dans la grille
def generate_unique_position(existing_positions):
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in existing_positions:
            return position

# Génération des ennemis avec des positions uniques
positions = set()  # Ensemble pour éviter les chevauchements de position
enemies = []

# Créer trois Gobelins avec des positions uniques
for _ in range(3):
    GOBELIN_POSITION = generate_unique_position(positions)
    positions.add(GOBELIN_POSITION)
    enemies.append(Enemy("Gobelin", 50, 50, 10, 10, GOBELIN_POSITION, 15))

# Créer trois Orcs avec des positions uniques
for _ in range(2):
    ORC_POSITION = generate_unique_position(positions)
    positions.add(ORC_POSITION)
    enemies.append(Enemy("Orc", 75, 75, 15, 25, ORC_POSITION, 30))

# Créer trois Elfes avec des positions uniques
for _ in range(2):
    ELFE_POSITION = generate_unique_position(positions)
    positions.add(ELFE_POSITION)
    enemies.append(Enemy("Elfe", 100, 100, 20, 15, ELFE_POSITION, 25))