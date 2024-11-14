import random

# Base Item class for all items in the game
class Item:
    def __init__(self, name, effect, value, rarity):
        # Initialize basic item properties
        self.name = name
        self.effect = effect
        self.value = value
        self.rarity = rarity

    def use(self, items):
        # Placeholder method to be overridden in subclasses
        pass

# HealthPotion class that inherits from Item, specific to healing the player
class HealthPotion(Item):
    def __init__(self, name, value, rarity):
        # Initialize health potion with a specific effect
        super().__init__(name, "Restores health points", value, rarity)
        self.rarity = rarity

    def use(self, items):
        """Restores health to the player, up to the max health limit."""
        items.health += self.value
        if items.health > items.max_health:
            items.health = items.max_health
        print(f"{items.name} used {self.name} ({self.rarity}) and recovered {self.value} health points. Current health: {items.health}/{items.max_health}")

# List of health potions with different rarities and healing values
pv_min = HealthPotion("Potion 25", 25, "Common")
pv_mid = HealthPotion("Potion 50", 50, "Epic")
pv_max = HealthPotion("Potion 100", 100, "Legendary")

# DamageBoostPotion class that temporarily boosts the player's damage
class DamageBoostPotion(Item):
    def __init__(self, name, damage_increase, turns, rarity):
        # Initialize damage boost potion with duration and effect value
        super().__init__(name, "Increases damage", damage_increase, rarity)
        self.turns = turns
        self.rarity = rarity

    def use(self, items):
        """Applies a damage boost to the player for a set number of turns."""
        items.damage_boost = self.value
        items.boost_turns = self.turns
        print(f"{items.name} used {self.name} ({self.rarity}) and gained {self.value} extra damage points for {self.turns} turn(s).")

# List of damage boost potions with different rarities and values
deg_min = DamageBoostPotion("Boost 15", 15, 3, "Common")
deg_mid = DamageBoostPotion("Boost 30", 30, 2, "Epic")
deg_max = DamageBoostPotion("Boost 50", 50, 1, "Legendary")

# Weapon class that inherits from Item, with additional properties for damage and effects
class Weapon(Item):
    def __init__(self, name, damage, rarity, extra_effect=None):
        # Initialize weapon with optional extra effect (e.g., healing)
        super().__init__(name, "Deals damage", damage, rarity)
        self.extra_effect = extra_effect

    def use(self, items, target):
        """Inflicts damage on a target and applies any additional effect, such as healing."""
        target.health -= self.value
        effect_message = f" and dealt {self.value} damage"

        # If weapon has an extra effect (like healing the user), apply it
        if self.extra_effect:
            items.health += self.extra_effect
            effect_message += f". {items.name} also recovered {self.extra_effect} health points"

        print(f"{items.name} used {self.name}{effect_message}. {target.name} has {target.health} health remaining.")

# List of weapons with different properties and effects
gun = Weapon("Gun", 40, "Epic")
harpon = Weapon("Harpoon", 25, "Common")
arc = Weapon("Bow", 15, "Common", extra_effect=25) 

# Dictionary to retrieve items by name, making it easier to find specific items
item_classes = {
    "Potion 25": pv_min,
    "Potion 50": pv_mid,
    "Potion 100": pv_max,
    "Boost 15": deg_min,
    "Boost 30": deg_mid,
    "Boost 50": deg_max,
    "Gun": gun,
    "Harpoon": harpon,
    "Bow": arc
}

# Function to retrieve an item instance by its name
def get_item_by_name(name):
    return item_classes.get(name)

# Function to generate random loot, selecting two random items from the predefined list
def generate_random_loot():
    """Generates two random items from a predefined list of possible loot items."""
    loot_items = [pv_min, pv_mid, pv_max, deg_min, deg_mid, deg_max, gun, harpon, arc]
    return random.sample(loot_items, 2)
