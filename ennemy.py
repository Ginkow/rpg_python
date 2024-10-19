import random
import inventory

class Enemy:
    def __init__(self, name, health, attack, defense, position):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.position = position
        self.alive = True

    def is_alive(self):
        return self.health > 0

    def attack_player(self, player):
        damage = self.attack - player.defense
        if damage < 0:
            damage = 0
        player.health -= damage
        return damage

    def generate_loot(self):
        # Objets par rareté
        commune = [inventory.pv_min, inventory.deg_min, inventory.harpoon, inventory.arc]
        epic = [inventory.pv_mid, inventory.deg_mid, inventory.gun]
        legendary = [inventory.pv_max, inventory.deg_max]

        possible_loot = []

        # Le monstre peut laisser entre 1 et 3 objets
        loot_count = random.randint(1, 3)
        
        for _ in range(loot_count):
            rarity_roll = random.random()
            
            # 60% de chance pour un objet commun
            if rarity_roll <= 0.6:
                possible_loot.append(random.choice(commune))
            # 30% de chance pour un objet épique
            elif rarity_roll <= 0.9:
                possible_loot.append(random.choice(epic))
            # 10% de chance pour un objet légendaire
            else:
                possible_loot.append(random.choice(legendary))

        return possible_loot
