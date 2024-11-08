import random

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
        super().__init__(name, "Restaure des points de vie", value, rarity)
        self.rarity = rarity

    def use(self, items):
        items.health += self.value
        if items.health > items.max_health:
            items.health = items.max_health
        print(f"{items.name} a utilisé {self.name} ({self.rarity}) et récupéré {self.value} points de vie. Vie actuelle: {items.health}/{items.max_health}")

# Liste des potions de vie
pv_min = HealthPotion("Potion 25", 25, "Commune")
pv_mid = HealthPotion("Potion 50", 50, "Épique")
pv_max = HealthPotion("Potion 100", 100, "Légendaire")

class DamageBoostPotion(Item):
    def __init__(self, name, damage_increase, turns, rarity):
        super().__init__(name, "Augmente les dégâts", damage_increase, rarity)
        self.turns = turns
        self.rarity = rarity

    def use(self, items):
        items.damage_boost = self.value
        items.boost_turns = self.turns
        print(f"{items.name} a utilisé {self.name} ({self.rarity}) et a gagné {self.value} points de dégâts supplémentaires pour {self.turns} tour(s).")

# Liste des potions de boost de dégâts
deg_min = DamageBoostPotion("Boost 15", 15, 3, "Commune")
deg_mid = DamageBoostPotion("Boost 30", 30, 2, "Épique")
deg_max = DamageBoostPotion("Boost 50", 50, 1, "Légendaire")

class Weapon(Item):
    def __init__(self, name, damage, rarity, extra_effect=None):
        super().__init__(name, "Inflige des dégâts", damage, rarity)
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
harpon = Weapon("Harpon", 25, "Commune")
arc = Weapon("Arc", 15, "Commune",extra_effect=25)

# Dictionnaire pour retrouver les objets par nom
item_classes = {
    "Potion 25": pv_min,
    "Potion 50": pv_mid,
    "Potion 100": pv_max,
    "Boost 15": deg_min,
    "Boost 30": deg_mid,
    "Boost 50": deg_max,
    "Pistolet": gun,
    "Harpon": harpon,
    "Arc": arc
}

def get_item_by_name(name):
    return item_classes.get(name)

def generate_random_loot():
    """Génère deux objets aléatoires à partir d'une liste prédéfinie."""
    loot_items = [pv_min, pv_mid, pv_max, deg_min, deg_mid, deg_max, gun, harpon, arc]  # Liste d'objets possibles
    return random.sample(loot_items, 2)  # Retourne 2 objets aléatoires
