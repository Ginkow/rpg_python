class Item:
    def __init__(self, name, effect, value, rarity):
        self.name = name
        self.effect = effect
        self.value = value
        self.rarity = rarity

    def use(self, items):
        pass

class HealthPotion(Item):
    def __init__(self, name, value, rarity):
        super().__init__(name, "Restaure des points de vie", value, rarity)  # Ajouter rarity ici
        self.rarity = rarity

    def use(self, items):
        items.health += self.value
        if items.health > items.max_health:
            items.health = items.max_health
        print(f"{items.name} a utilisé {self.name} ({self.rarity}) et récupéré {self.value} points de vie. Vie actuelle: {items.health}/{items.max_health}")

# Liste des potions de vie
pv_min = HealthPotion("Potion de vie min", 25, "Commune")
pv_mid = HealthPotion("Potion de vie moyenne", 50, "Épique")
pv_max = HealthPotion("Potion de vie max", 100, "Légendaire")

class DamageBoostPotion(Item):
    def __init__(self, name, damage_increase, turns, rarity):
        super().__init__(name, "Augmente les dégâts", damage_increase, rarity)  # Ajouter rarity ici
        self.turns = turns
        self.rarity = rarity

    def use(self, items):
        items.damage_boost = self.value
        items.boost_turns = self.turns
        print(f"{items.name} a utilisé {self.name} ({self.rarity}) et a gagné {self.value} points de dégâts supplémentaires pour {self.turns} tour(s).")

# Liste des potions de boost de dégâts
deg_min = DamageBoostPotion("Potion de boost de dégâts min", 15, 3, "Commune")
deg_mid = DamageBoostPotion("Potion de boost de dégâts moyenne", 50, 2, "Épique")
deg_max = DamageBoostPotion("Potion de boost de dégâts max", 75, 1, "Légendaire")

class Weapon(Item):
    def __init__(self, name, damage, rarity, extra_effect=None):
        super().__init__(name, "Inflige des dégâts", damage, rarity)  # Ajouter rarity ici
        self.extra_effect = extra_effect

    def use(self, items, target):
        target.health -= self.value
        effect_message = f" et inflige {self.value} points de dégâts"
        
        if self.extra_effect:
            items.health += self.extra_effect
            effect_message += f". {items.name} a également récupéré {self.extra_effect} points de vie"

        print(f"{items.name} a utilisé {self.name}{effect_message}. {target.name} a {target.health} points de vie restants.")

# Liste des armes
gun = Weapon("Pistolet", 40, "Épique")
harpoon = Weapon("Harpon", 25, "Commune")
arc = Weapon("Arc", 15, "Commune",extra_effect=25)  # Récupère 25 HP lors de l'utilisation