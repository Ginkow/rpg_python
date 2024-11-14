from inventory import Weapon

# Player class representing the main character
class Player:
    def __init__(self, name, level, health, max_health, attack, defense, inventory, weapon, experience, experience_to_next_level, position=(0, 0)):
        # Initialize player attributes
        self.name = name
        self.level = level
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.inventory = inventory
        self.weapon = weapon
        self.experience = experience
        self.experience_to_next_level = experience_to_next_level
        self.damage_boost = 0
        self.boost_turns = 0
        self.position = position
        self.level_up_message = ""
    
    def is_alive(self):
        """Check if the player is still alive."""
        return self.health > 0
    
    def gain_experience(self, amount):
        """Gain experience and level up if the threshold is reached."""
        self.experience += amount
        print(f"{self.name} gains {amount} experience points.")

        # Loop to handle multiple level-ups in case of high experience gain
        while self.experience >= self.experience_to_next_level:
            # Advance to the next level
            self.experience -= self.experience_to_next_level
            self.level += 1

            # Increase health and attack based on the new level
            self.max_health += 10 * self.level 
            self.attack += 2 * self.level 

            # Restore health and shield to maximum
            self.health = self.max_health
            self.defense = 100

            # Increase experience needed for the next level
            self.experience_to_next_level += 10

            # Level-up message
            self.level_up_message = f"Congratulations! You are now level {self.level}!"
            print(f"Max health increased to {self.max_health}, attack increased to {self.attack}.")
            print(f"Health and shield restored to: {self.health} HP and {self.defense} shield.\n")

    def attack_target(self, target):
        # Calculate damage considering any temporary boost
        total_attack = self.attack + self.damage_boost
        damage = total_attack

        # Damage first affects the target's shield if present
        if target.defense > 0:
            if damage >= target.defense:
                # If damage exceeds shield, deplete shield and apply remainder to health
                damage_to_health = damage - target.defense
                print(f"{self.name} destroys {target.name}'s shield ({target.defense} defense points).")
                target.defense = 0
                target.health -= damage_to_health
                print(f"{self.name} deals {damage_to_health} damage to {target.name}. {target.name} has {target.health} HP left.\n")
            else:
                # If damage is less than shield, only reduce shield
                target.defense -= damage
                print(f"{self.name} reduces {target.name}'s shield by {damage}. {target.defense} shield remains.\n")
        else:
            # If no shield, damage directly reduces health
            target.health -= damage
            print(f"{self.name} attacks {target.name} and deals {damage} damage. {target.name} has {target.health} HP left.\n")

        # Reduce the remaining turns of damage boost
        if self.boost_turns > 0:
            self.boost_turns -= 1
            if self.boost_turns == 0:
                self.damage_boost = 0
                print(f"{self.name}'s damage boost has expired.")

    def pickup_item(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        print(f"{self.name} picked up {item.name}!")

    def use_item(self, item_index, target=None):
        """Use an item from the inventory based on its index."""
        # Convert the provided index to an integer and validate it
        try:
            item_index = int(item_index) - 1
        except ValueError:
            print("Invalid entry. Please enter a number corresponding to an item.")
            return

        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if isinstance(item, Weapon):
                # If target not specified, check if the player is in combat with an enemy
                if target is None:
                    if hasattr(self, 'current_enemy') and self.current_enemy is not None and self.current_enemy.is_alive():
                        target = self.current_enemy
                    else:
                        print(f"You need to choose a target to use {item.name}.")
                        return
                
                # Use the weapon on the target
                item.use(self, target)
            else:
                item.use(self)

            # Remove the used item from inventory
            self.inventory.remove(item)
            print(f"{self.name} used {item.name}, and it has been removed from the inventory.\n")
        else:
            print(f"Invalid item number. Choose a number between 1 and {len(self.inventory)}.")

    def show_inventory(self):
        """Display all items in the player's inventory with numbering."""
        if not self.inventory:
            print(f"{self.name}'s inventory is empty.")
        else:
            print(f"{self.name}'s inventory:")
            for idx, item in enumerate(self.inventory, 1):
                print(f"{idx}. {item.name}")

    def use_skill(self, target):
        """Special skill dealing 70 damage points."""
        skill_damage = 70
        print(f"{self.name} uses a special skill!")
        target.health -= skill_damage
        print(f"{target.name} receives {skill_damage} damage!")
        return skill_damage
