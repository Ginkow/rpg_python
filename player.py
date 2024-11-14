from inventory import Weapon

class Player:
    def __init__(self, name, level, health, max_health, attack, defense, inventory, weapon, experience, experience_to_next_level, position=(0, 0)):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = max_health
        self.attack = 20
        self.defense = defense
        self.inventory = inventory
        self.weapon = weapon
        self.experience = experience
        self.experience_to_next_level = experience_to_next_level
        self.damage_boost = 0
        self.boost_turns = 0
        self.position = position
    
    def is_alive(self):
        """Vérifie si le joueur est encore en vie."""
        return self.health > 0


    def attack_target(self, target):
        # Calculer les dégâts en prenant en compte le boost temporaire
        total_attack = self.attack + self.damage_boost
        damage = total_attack

        # Si l'ennemi a du bouclier, les dégâts affectent d'abord le bouclier
        if target.defense > 0:
            if damage >= target.defense:
                # Si les dégâts sont supérieurs ou égaux au bouclier, tout le bouclier est détruit
                damage_to_health = damage - target.defense  # Calculer les dégâts restants après le bouclier
                print(f"{self.name} détruit le bouclier de {target.name} ({target.defense} points de défense).")
                target.defense = 0  # Bouclier épuisé
                target.health -= damage_to_health  # Dégâts restants affectent la santé
                print(f"{self.name} inflige {damage_to_health} points de dégâts à {target.name}. {target.name} a {target.health} points de vie restants.\n")
            else:
                # Si les dégâts sont inférieurs au bouclier, seule la défense est réduite
                target.defense -= damage
                print(f"{self.name} réduit le bouclier de {target.name} de {damage} points. Il reste {target.defense} points de bouclier.\n")
        else:
            # Si l'ennemi n'a plus de bouclier, les dégâts affectent directement la santé
            target.health -= damage
            print(f"{self.name} attaque {target.name} et inflige {damage} points de dégâts. {target.name} a {target.health} points de vie restants.\n")

        # Diminuer le nombre de tours de boost de dégâts
        if self.boost_turns > 0:
            self.boost_turns -= 1
            if self.boost_turns == 0:
                self.damage_boost = 0
                print(f"Le boost de dégâts de {self.name} a expiré.")

    def pickup_item(self, item):
        """Ajoute un objet à l'inventaire du joueur."""
        self.inventory.append(item)
        print(f"{self.name} a ramassé un(e) {item.name} !")

    def use_item(self, item_index, target=None):
        """Utilise un objet de l'inventaire en fonction de son index."""
        # Convertir l'index donné en entier et vérifier sa validité
        try:
            item_index = int(item_index) - 1  # L'utilisateur entre un numéro à partir de 1, donc on ajuste l'index
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro correspondant à un objet.")
            return

        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if isinstance(item, Weapon):
                # Si aucune cible n'est donnée, on vérifie si le joueur est en combat avec un ennemi
                if target is None:
                    if hasattr(self, 'current_enemy') and self.current_enemy is not None and self.current_enemy.is_alive():
                        target = self.current_enemy 
                    else:
                        print(f"Vous devez choisir une cible pour utiliser {item.name}.")
                        return
                
                # Utilisation de l'arme contre la cible (l'ennemi actuel)
                item.use(self, target)  # On passe le joueur et la cible
            else:
                item.use(self)

            # Supprimer l'item de l'inventaire après utilisation
            self.inventory.remove(item)
            print(f"{self.name} a utilisé {item.name}, et l'item a été retiré de l'inventaire.\n")
        else:
            print(f"Numéro d'objet invalide. Choisissez un numéro entre 1 et {len(self.inventory)}.")
            

    def show_inventory(self):
        """Affiche tous les objets dans l'inventaire du joueur avec des numéros."""
        if not self.inventory:
            print(f"L'inventaire de {self.name} est vide.")
        else:
            print(f"Inventaire de {self.name}:")
            for idx, item in enumerate(self.inventory, 1):
                print(f"{idx}. {item.name}")


    def use_skill(self, target):
        """Compétence spéciale infligeant 70 points de dégâts."""
        skill_damage = 70
        print(f"{self.name} utilise une compétence spéciale !")
        target.health -= skill_damage
        print(f"{target.name} reçoit {skill_damage} points de dégâts !")
        return skill_damage
