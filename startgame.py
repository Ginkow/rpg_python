import random
import os  # Importer le module os pour vider le terminal
import player
import ennemy
import inventory
import save
import startgameload
from datetime import datetime
from launch import game
import tresors
import time

# Positions fixes pour le boss et les objets
BOSS_POSITION = (5, 5)


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_save_name(base_name="game_save", directory='save/', extension='.json'):
    """Génère un nom de fichier de sauvegarde basé sur la date et l'heure actuelles, en utilisant .json."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_name = f"{directory}{base_name}_{timestamp}{extension}"
    return save_name

def save_game_state(player, enemies, position, treasures_found, defeated_enemies):
    save_name = generate_save_name()
    save.save_game(player, enemies, position, treasures_found, defeated_enemies, save_name)
    print(f"Game saved as {save_name}")

def start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies):
    """Démarre une partie avec les données chargées."""
    print(f"Démarrage de la partie avec {player.name} à la position {current_position}.")
    
    # Logique pour gérer le déroulement de la partie
    while player.is_alive() and enemies:
        print(f"Vous êtes à la position {current_position}.")
        startgameload.start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies)

def start_game():
    treasure = tresors.TREASURE_POSITION
    clear_terminal()
    print("Bienvenue dans le jeu !")
    
    name = input("Entrez votre nom pour commencer le jeu: ")
    # Initialisation du joueur
    joueur = player.Player(name, 1, 100, 100, 20, 100, [], "épée", 0, 20)
    boss = ennemy.Enemy("Dragon", 1000, 1000, 30, 250, BOSS_POSITION, 430)
    
    print(f"Bienvenue, {joueur.name}!")
    print(f"Vous avez {joueur.health} HP et votre objectif est de trouver tous les trésors tout en évitant les obstacles, les monstres, et le boss final.")

        
    total_treasures = 1
    treasures_found = 0
    current_position = (0, 0)
    defeated_enemies = []
    
    # Liste pour suivre les trésors collectés
    treasures_collected = []

    inventory_displayed = False  # État de l'affichage de l'inventaire

    while joueur.health > 0:
        clear_terminal()
        
        if joueur.level_up_message:
            print(joueur.level_up_message)
            joueur.level_up_message = ""
            
        print(f"Position actuelle: {current_position}, Trésors trouvés: {treasures_found}, Vies restantes: {joueur.health}, Boucliers restants: {joueur.defense}, Level: {joueur.level}")
        
        active_enemies = [enemy for enemy in ennemy.enemies if enemy.name not in defeated_enemies]
        # #Afficher position ennemies
        for enemy in active_enemies:
            print(f"Position de {enemy.name} : {enemy.position}")
            
        if tresors.TREASURE_POSITION is not None:
            print(f"Position du coffre: {tresors.TREASURE_POSITION}")
        
        # Afficher l'inventaire si demandé
        if inventory_displayed:
            joueur.show_inventory()

        # Décrire l'emplacement
        describe_location()

        # Entrer une commande de déplacement (zqsd ou go east, etc.)
        move = input("Entrez votre mouvement (zqsd, go east, etc.) ou appuyez sur 'i' pour afficher/masquer l'inventaire, 'exit' pour quitter: \n")

        # Vérification si le joueur veut afficher/masquer l'inventaire
        if move.lower() == 'i':
            inventory_displayed = not inventory_displayed  # Alterne l'état de l'inventaire
            continue  # Retourne au début de la boucle pour éviter d'exécuter le reste du code

        # Mise à jour de la position avec les bons paramètres
        new_position = update_position(move, current_position, joueur, ennemy.enemies, treasures_found, defeated_enemies)
        if new_position != current_position:
            current_position = new_position

        # Vérification des événements
        for enemy in ennemy.enemies:
            if current_position == enemy.position and enemy.is_alive() and enemy.name not in defeated_enemies:
                print(f"Un {enemy.name} vous attaque !")
                
                # Le joueur peut utiliser une potion ou une arme avant le combat
                action = input("Voulez-vous utiliser un objet avant de combattre ? (oui/non) : ")
                if action.lower() == "oui":
                    # Combat entre le joueur et l'ennemi
                    combat(joueur, enemy, defeated_enemies)

                if joueur.health <= 0:
                    print("Vous êtes mort. Fin de la partie.")
                    time.sleep(2)
                    clear_terminal()
                    return

        if current_position == treasure:
            # Vérifie si le trésor a déjà été récupéré
            if "treasure_1" not in treasures_collected:
                print("Vous avez trouvé un trésor !\n")
                treasures_found += 1

                # Générer et donner deux objets aléatoires au joueur
                loot = inventory.generate_random_loot()
                item_names = [item.name for item in loot]  # Crée une liste avec les noms des objets

                # Afficher les objets récupérés
                print(f"Vous avez récupéré {item_names[0]} et {item_names[1]}.\n")
                for item in loot:
                    joueur.pickup_item(item)

                # Marque ce trésor comme récupéré
                treasures_collected.append("treasure_1")
                tresors.mark_treasure_collected() 

                # Attendre que le joueur appuie sur une touche avant de continuer
                input("\nAppuyez sur Entrée pour continuer...")

            else:
                print("Vous avez déjà récupéré ce trésor.\n")
                input("\nAppuyez sur Entrée pour continuer...")
            
            # Continuer le jeu après avoir trouvé le trésor
            continue  # Reprend la boucle du jeu, sans finir
        
        if treasures_found == total_treasures:
            print("Félicitations ! Vous avez trouvé tous les trésors !")
            treasure = None
            continue  # Reprend la boucle du jeu, sans finir

        elif current_position == BOSS_POSITION:
            print("Vous avez trouvé le boss ! Préparez-vous à combattre.")
            if combat(joueur, boss, defeated_enemies):
                print("Vous avez vaincu le boss et gagné le jeu !\n")
                time.sleep(2)
                clear_terminal()
                game()
                break
            else:
                print("Vous avez perdu contre le boss. Fin de la partie.\n")
                time.sleep(2)
                clear_terminal()
                game()
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

def combat(player, enemy, defeated_enemies):
    while enemy.is_alive() and player.health > 0:
        print(f"\n*** Combat contre {enemy.name} (Niveau {enemy.level}) ***")
        print(f"{player.name}: {player.health}/{player.max_health} HP, {player.defense} de bouclier.")
        print(f"{enemy.name}: {enemy.health}/{enemy.max_health} HP, {enemy.defense} de bouclier.\n")

        # Tour du joueur
        print("\nC'est votre tour !")
        action = input("Que voulez-vous faire ? (1: Attaquer, 2: Utiliser un objet):\n ")

        if action == "1":
            # Le joueur choisit d'attaquer
            print(f"{player.name} attaque {enemy.name} !")
            player.attack_target(enemy)
        elif action == "2":
            # Le joueur choisit d'utiliser un objet
            if not player.inventory:  # Vérifie si l'inventaire est vide
                print("Inventaire vide, attaque normale effectuée.\n")
                print(f"{player.name} attaque {enemy.name} par défaut.")
                player.attack_target(enemy)
            else:
                player.show_inventory()
                item_name = input("Quel objet voulez-vous utiliser ? : ")
                player.use_item(item_name, target=enemy)

        # Si l'ennemi est mort après l'attaque ou l'utilisation de l'objet, le combat s'arrête ici
        if not enemy.is_alive():
            print(f"{enemy.name} est vaincu !")
            defeated_enemies.append(enemy.name)
            enemy.defeat()  # Marque l'ennemi comme vaincu
            exp_gained = enemy.level  # Suppose que le niveau de l'ennemi détermine les points d'expérience
            player.gain_experience(exp_gained)  # Utilise la méthode gain_experience pour gérer le level-up
            print(f"Vous avez récupéré {exp_gained} points d'expérience pour avoir vaincu {enemy.name} !\n")

            loot = enemy.generate_loot()
            for item in loot:
                print(f"{enemy.name} laisse tomber {item.name} ({item.rarity}).")
                player.pickup_item(item)
            input("Appuyez sur Entrée pour continuer...")
            return True  # Le joueur a gagné

        # Tour de l'ennemi
        print(f"\nC'est au tour de {enemy.name} d'attaquer !")
        enemy.attack_player(player)  # L'ennemi attaque le joueur

        # Vérifier si le joueur est toujours en vie
        if player.health <= 0:
            print(f"{player.name} a été vaincu par {enemy.name}.")
            return False 

    return player.health > 0
