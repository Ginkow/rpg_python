import random
import os
import ennemy
import save
from datetime import datetime

# Positions fixes pour le boss et les objets
BOSS_POSITION = (5, 5)
TREASURE_POSITION = (2, 3)
GOBELIN_POSITION = (4, 2)
ORC_POSITION = (3, 4)

def generate_save_name(base_name="game_save", directory='save/', extension='.json'):
    """Génère un nom de fichier de sauvegarde basé sur la date et l'heure actuelles, en évitant les doublons."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    save_name = f"{base_name}_{timestamp}{extension}"
    
    # Vérifie si le fichier existe déjà et ajuste le nom si nécessaire
    i = 1
    while os.path.exists(os.path.join(directory, save_name)):
        save_name = f"{base_name}_{timestamp}_{i}{extension}"
        i += 1
    
    return os.path.join(directory, save_name)  # Retourne le chemin complet


def clear_terminal():
    # Vider le terminal en fonction du système d'exploitation
    os.system('cls' if os.name == 'nt' else 'clear')

def start_loaded_game(loaded_player, enemies, current_position, treasures_found, defeated_enemies):
    """Démarre une partie avec les données chargées."""
    print(f"Démarrage de la partie avec {loaded_player.name} à la position {current_position}.")

    # Mettre à jour la position du joueur
    loaded_player.position = current_position  # Définir la position du joueur à celle chargée

    total_treasures = 1

    # Logique pour gérer le déroulement de la partie
    while loaded_player.is_alive() and enemies:  # Boucle principale du jeu
        clear_terminal()  # Vider le terminal au début de chaque boucle
        print(f"Vous êtes à la position {loaded_player.position}. Trésors trouvés : {treasures_found}, Vies restantes : {loaded_player.health}")

        # Afficher l'inventaire du joueur
        loaded_player.show_inventory()

        # Décrire l'emplacement
        describe_location()

        # Entrer une commande de déplacement (zqsd ou go east, etc.)
        move = input("Entrez votre mouvement (zqsd ou go east, go west, go north, go south): ")

        # Mise à jour de la position avec les bons paramètres
        new_position = update_position(move, loaded_player.position, loaded_player, enemies, treasures_found, defeated_enemies)
        if new_position != loaded_player.position:  # Si la position a changé
            loaded_player.position = new_position

        # Vérification des événements
        for enemy in enemies:
            if loaded_player.position == enemy.position and enemy.is_alive():
                print(f"Un {enemy.name} vous attaque !")
                
                # Le joueur peut utiliser une potion ou une arme avant le combat
                action = input("Voulez-vous utiliser un objet avant de combattre ? (oui/non) : ")
                if action.lower() == "oui":
                    item_name = input("Entrez le nom de l'objet à utiliser : ")
                    loaded_player.use_item(item_name)

                # Combat entre le joueur et l'ennemi
                if not combat(loaded_player, enemy):
                    print("Vous êtes mort. Fin de la partie.")
                    return

        if loaded_player.position == TREASURE_POSITION:
            print("Vous avez trouvé un trésor !")
            treasures_found += 1

        elif loaded_player.position == BOSS_POSITION:
            print("Vous avez trouvé le boss ! Préparez-vous à combattre.")
            if combat(loaded_player, ennemy.Enemy("Dragon", 50, 15, 10, BOSS_POSITION)):
                print("Vous avez vaincu le boss et gagné le jeu !")
                break
            else:
                print("Vous avez perdu contre le boss. Fin de la partie.")
                break

        # Vérifier si le joueur a trouvé tous les trésors
        if treasures_found == total_treasures:
            print("Félicitations ! Vous avez trouvé tous les trésors !")
            break

        # Vérifier les vies restantes
        if loaded_player.health <= 0:
            print("Game over ! Vous n'avez plus de vies.")
            break


def describe_location():
    descriptions = [
        "Vous êtes dans une forêt sombre.",
        "Vous arrivez près d'une rivière bruyante.",
        "Vous êtes dans une clairière ensoleillée.",
        "Vous entrez dans une grotte humide et sombre."
    ]
    print(random.choice(descriptions))

def update_position(move, current_position, player, enemies, treasures_found, defeated_enemies):
    x, y = current_position
    
    # Si le joueur veut quitter la partie
    if move == "exit":
        confirm_exit = input("Voulez-vous quitter la partie ? (oui/non): ")
        if confirm_exit.lower() == "oui":
            save_game = input("Voulez-vous sauvegarder la partie avant de quitter ? (oui/non): ")
            if save_game.lower() == "oui":
                save.save_game(player, enemies, current_position, treasures_found, defeated_enemies)
                print("Partie sauvegardée. Au revoir!")
            else:
                print("Vous quittez sans sauvegarder. Au revoir!")
            exit()  # Quitter le programme

    # Déplacement normal
    if move in ["z", "go north"]:
        if y < 10:  # Limite supérieure pour y
            return (x, y + 1)
    elif move in ["s", "go south"]:
        if y > 0:  # Limite inférieure pour y
            return (x, y - 1)
    elif move in ["q", "go west"]:
        if x > 0:  # Limite inférieure pour x
            return (x - 1, y)
    elif move in ["d", "go east"]:
        if x < 10:  # Limite supérieure pour x
            return (x + 1, y)
    else:
        print("Mouvement invalide.")
    
    return current_position

def combat(player, enemy):
    while enemy.is_alive() and player.health > 0:
        print(f"{enemy.name} attaque !")
        damage_to_player = enemy.attack_player(player)
        print(f"{enemy.name} inflige {damage_to_player} points de dégâts. {player.name} a {player.health} points de vie restants.")
        
        if player.health <= 0:
            print(f"{player.name} a été vaincu par {enemy.name}.")
            return False
        
        print(f"{player.name} contre-attaque !")
        damage_to_enemy = player.attack_target(enemy)
        print(f"{player.name} inflige {damage_to_enemy} points de dégâts. {enemy.name} a {enemy.health} points de vie restants.")
        
        if not enemy.is_alive():
            print(f"{enemy.name} est vaincu !")
            player.experience += 10  # Récompense d'expérience
            
            # Génération de loot
            loot = enemy.generate_loot()
            for item in loot:
                print(f"{enemy.name} laisse tomber {item.name} ({item.rarity}).")
                player.pickup_item(item)
            
            return True

    return player.health > 0