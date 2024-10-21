import random
import os  # Importer le module os pour vider le terminal
import player
import ennemy
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
        ennemy.Enemy("Gobelin", 50, 50, 10, 10, GOBELIN_POSITION, 15),
        ennemy.Enemy("Orc", 75, 75, 15, 25, ORC_POSITION, 30)
    ]
    boss = ennemy.Enemy("Dragon", 2500, 2500, 30, 100, BOSS_POSITION, 430)
    
    print(f"Bienvenue, {joueur.name}!")
    print(f"Vous avez {joueur.health} HP et votre objectif est de trouver tous les trésors tout en évitant les obstacles, les monstres, et le boss final.")
    
    treasures_found = 0
    current_position = (0, 0)
    total_treasures = 1
    defeated_enemies = []
        
    inventory_displayed = False  # État de l'affichage de l'inventaire

    while joueur.health > 0:
        clear_terminal()
        print(f"Position actuelle: {current_position}, Trésors trouvés: {treasures_found}, Vies restantes: {joueur.health}, Boucliers restants: {joueur.defense}")
        
        # Afficher l'inventaire si demandé
        if inventory_displayed:
            joueur.show_inventory()

        # Décrire l'emplacement
        describe_location()

        # Entrer une commande de déplacement (zqsd ou go east, etc.)
        move = input("Entrez votre mouvement (zqsd, go east, etc.) ou appuyez sur 'i' pour afficher/masquer l'inventaire, 'exit' pour quitter: ")

        # Vérification si le joueur veut afficher/masquer l'inventaire
        if move.lower() == 'i':
            inventory_displayed = not inventory_displayed  # Alterne l'état de l'inventaire
            continue  # Retourne au début de la boucle pour éviter d'exécuter le reste du code

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
    # Boucle tant que les deux sont vivants
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
            player.experience += 10
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