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
        # Calcul des dégâts infligés par l'ennemi
        damage = self.attack
        if damage < 1:  # Assurer que les dégâts minimum sont de 1
            damage = 1

        # Si le joueur a du bouclier, les dégâts vont d'abord réduire le bouclier
        if player.defense > 0:
            if damage >= player.defense:
                # Si les dégâts dépassent ou égalent la défense, tout le bouclier est détruit
                damage -= player.defense
                player.defense = 0  # Bouclier épuisé
                player.health -= damage  # Dégâts restants affectent la santé
            else:
                # Si les dégâts sont inférieurs à la défense, seule la défense est réduite
                player.defense -= damage
        else:
            # Si le joueur n'a pas de bouclier, les dégâts affectent directement la santé
            player.health -= damage

        return damage




    def generate_loot(self):
        # Objets par rareté
        commune = [inventory.pv_min, inventory.deg_min, inventory.harpoon, inventory.arc]
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

        return [loot]  # Retourner l'objet sous forme de liste pour rester compatible avec le reste du code

