class Player:
    def __init__(self, name, level, health, max_health, attack, defense, inventory, weapon, experience, experience_to_next_level, position=(0, 0)):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = max_health
        self.attack = 20
        self.defense = defense
        self.inventory = []
        self.weapon = weapon
        self.experience = experience
        self.experience_to_next_level = experience_to_next_level
        self.damage_boost = 0
        self.boost_turns = 0
        self.position = position  # Position du joueur
    
    def is_alive(self):
        """Vérifie si le joueur est encore en vie."""
        return self.health > 0


    def attack_target(self, target):
        # Calculer les dégâts en prenant en compte le boost temporaire
        total_attack = self.attack + self.damage_boost
        damage = total_attack - target.defense
        if damage < 0:
            damage = 0  # Éviter les dégâts négatifs
        target.health -= damage
        print(f"{self.name} attaque {target.name} et inflige {damage} points de dégâts. {target.name} a {target.health} points de vie restants.")

        # Diminuer le nombre de tours de boost de dégâts
        if self.boost_turns > 0:
            self.boost_turns -= 1
            if self.boost_turns == 0:
                self.damage_boost = 0  # Réinitialiser le boost après expiration
                print(f"Le boost de dégâts de {self.name} a expiré.")

    def pickup_item(self, item):
        """Ajoute un objet à l'inventaire du joueur."""
        self.inventory.append(item)
        print(f"{self.name} a ramassé un(e) {item.name} !")

    def use_item(self, item_name):
        """Utilise un objet de l'inventaire en fonction du nom."""
        for item in self.inventory:
            if item.name == item_name:
                item.use(self)  # Utilise l'objet sur le joueur
                self.inventory.remove(item)  # Retire l'objet après utilisation
                return
        print(f"Objet {item_name} non trouvé dans l'inventaire.")

    def show_inventory(self):
        """Affiche tous les objets dans l'inventaire du joueur."""
        if not self.inventory:
            print(f"L'inventaire de {self.name} est vide.")
        else:
            print(f"Inventaire de {self.name}:")
            for item in self.inventory:
                print(f"- {item.name}")

    def use_skill(self, target):
        """Compétence spéciale infligeant 70 points de dégâts."""
        skill_damage = 70
        print(f"{self.name} utilise une compétence spéciale !")
        target.health -= skill_damage
        print(f"{target.name} reçoit {skill_damage} points de dégâts !")
        return skill_damage
