import random
import os  # Importer le module os pour vider le terminal
import player
import ennemy
import inventory
import save
import startgameload
from datetime import datetime

# Positions fixes pour le boss et les objets
BOSS_POSITION = (5, 5)
TREASURE_POSITION = (2, 3)
GOBELIN_POSITION = (4, 2)
ORC_POSITION = (3, 4)


def clear_terminal():
    # Vider le terminal en fonction du système d'exploitation
    os.system('cls' if os.name == 'nt' else 'clear')
    
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
    
def start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies):
    """Démarre une partie avec les données chargées."""
    print(f"Démarrage de la partie avec {player.name} à la position {current_position}.")
    
    # Logique pour gérer le déroulement de la partie
    while player.is_alive() and enemies:
        print(f"Vous êtes à la position {current_position}.")
        startgameload.start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies)

def start_game():
    clear_terminal()
    print("Bienvenue dans le jeu !")
    
    name = input("Entrez votre nom pour commencer le jeu: ")
    # Initialisation du joueur
    joueur = player.Player(name, 10, 100, 100, 20, 100, [], "épée", 100, 200)

    # Initialisation des ennemis
    enemies = [
        ennemy.Enemy("Gobelin", 50, 10, 10, GOBELIN_POSITION),
        ennemy.Enemy("Orc", 75, 15, 25, ORC_POSITION)
    ]
    boss = ennemy.Enemy("Dragon", 100, 30, 100, BOSS_POSITION)
    
    print(f"Bienvenue, {joueur.name}!")
    print(f"Vous avez {joueur.health} HP et votre objectif est de trouver tous les trésors tout en évitant les obstacles, les monstres, et le boss final.")
    
    treasures_found = 0
    current_position = (0, 0)
    total_treasures = 1
    defeated_enemies = []

    # Ajout d'objets dans le monde du jeu
    health_potion = inventory.HealthPotion("Potion de vie moyenne", 50, "Épique")
    damage_boost = inventory.DamageBoostPotion("Potion de boost de dégâts max", 75, 1, "Légendaire")
    arc_weapon = inventory.Weapon("Arc", 15, "Légendaire", extra_effect=25)

    # Ramasser des objets au cours de l'aventure
    joueur.pickup_item(health_potion)
    joueur.pickup_item(damage_boost)
    joueur.pickup_item(arc_weapon)
    
    while joueur.health > 0:
        clear_terminal()
        print(f"Position actuelle: {current_position}, Trésors trouvés: {treasures_found}, Vies restantes: {joueur.health}, Boucliers restants: {joueur.defense}")
        
        # Afficher l'inventaire du joueur
        joueur.show_inventory()
        
        # Décrire l'emplacement
        describe_location()

        # Entrer une commande de déplacement (zqsd ou go east, etc.)
        move = input("Entrez votre mouvement (zqsd ou go east, go west, go north, go south) et pour quitter/sauvegarder (exit): ")

        # Mise à jour de la position avec les bons paramètres
        new_position = update_position(move, current_position, joueur, enemies, treasures_found, defeated_enemies)
        if new_position != current_position:
            current_position = new_position

        # Vérification des événements
        for enemy in enemies:
            if current_position == enemy.position and enemy.is_alive():
                print(f"Un {enemy.name} vous attaque !")
                
                # Le joueur peut utiliser une potion ou une arme avant le combat
                action = input("Voulez-vous utiliser un objet avant de combattre ? (oui/non) : ")
                if action.lower() == "oui":
                    item_name = input("Entrez le nom de l'objet à utiliser : ")
                    joueur.use_item(item_name)

                # Combat entre le joueur et l'ennemi
                combat(joueur, enemy)
                if joueur.health <= 0:
                    print("Vous êtes mort. Fin de la partie.")
                    return

        if current_position == TREASURE_POSITION:
            print("Vous avez trouvé un trésor !")
            treasures_found += 1

        elif current_position == BOSS_POSITION:
            print("Vous avez trouvé le boss ! Préparez-vous à combattre.")
            if combat(joueur, boss):
                print("Vous avez vaincu le boss et gagné le jeu !\n")
                break
            else:
                print("Vous avez perdu contre le boss. Fin de la partie.\n")
                break

        # Vérifier si le joueur a trouvé tous les trésors
        if treasures_found == total_treasures:
            print("Félicitations ! Vous avez trouvé tous les trésors !\n")
            break

        # Vérifier les vies restantes
        if joueur.health <= 0:
            print("Game over ! Vous n'avez plus de vies.\n")
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
                save_name = generate_save_name()
                save.save_game(player, enemies, current_position, treasures_found, defeated_enemies, save_name)
                print("Partie sauvegardée. Au revoir!")
            else:
                print("Vous quittez sans sauvegarder. Au revoir!")
            exit()  # Quitter le programme

    # Déplacement normal
    if move in ["z", "go north"]:
        if y < 10: 
            return (x, y + 1)
    elif move in ["s", "go south"]:
        if y > 0:
            return (x, y - 1)
    elif move in ["q", "go west"]:
        if x > 0:
            return (x - 1, y)
    elif move in ["d", "go east"]:
        if x < 10: 
            return (x + 1, y)
    else:
        print("Mouvement invalide.")
    
    return current_position

def combat(player, enemy):
    while enemy.is_alive() and player.health > 0:
        print(f"{enemy.name} attaque !")
        damage_to_player = enemy.attack_player(player)
        print(f"{enemy.name} inflige {damage_to_player} points de dégâts. {player.name} a {player.health} points de vie restants et {player.defense} de shield.\n")
        
        if player.health <= 0:
            print(f"{player.name} a été vaincu par {enemy.name}.")
            return False
        
        print(f"{player.name} contre-attaque !")
        player.attack_target(enemy)
        
        if not enemy.is_alive():
            print(f"{enemy.name} est vaincu !")
            # Récompense d'expérience
            player.experience += 10
            
            # Génération de loot
            loot = enemy.generate_loot()
            for item in loot:
                print(f"{enemy.name} laisse tomber {item.name} ({item.rarity}).")
                player.pickup_item(item)
            
             # Attendre que le joueur appuie sur "Entrée" avant de continuer
            input("Appuyez sur Entrée pour continuer...")
            return True

    return player.health > 0
