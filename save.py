import json
from player import Player
from ennemy import Enemy
from inventory import get_item_by_name
from datetime import datetime

def generate_save_name():
    """Génère un nom de fichier de sauvegarde basé sur la date et l'heure actuelles."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"save/game_save_{timestamp}.json"

def save_game(player, enemies, position, treasures_found, defeated_enemies, save_name):
    """Sauvegarde l'état du jeu dans un fichier JSON."""
    game_data = {
        'player': {
            'name': player.name,
            'level': player.level,
            'health': player.health,
            'max_health': player.max_health,
            'attack': player.attack,
            'defense': player.defense,
            'weapon': player.weapon,
            'inventory': [item.name for item in player.inventory],
            'experience': player.experience,
            'experience_to_next_level': player.experience_to_next_level,
            'position': position,
            'alive': player.is_alive()
        },
        'enemies': [
            {
                'name': enemy.name,
                'health': enemy.health,
                'max_health': enemy.max_health,
                'attack': enemy.attack,
                'defense': enemy.defense,
                'position': enemy.position,  # Enregistre la position de l'ennemi
                'level': enemy.level,
                'defeated': not enemy.is_alive()
            }
            for enemy in enemies
        ],
        'treasures_found': treasures_found,
        'defeated_enemies': defeated_enemies
    }

    with open(save_name, 'w') as save_file:
        json.dump(game_data, save_file, indent=4)
    print("Partie sauvegardée avec succès.")

def load_inventory(inventory_data):
    """Charge l'inventaire à partir des données sauvegardées."""
    inventory = []
    for item_name in inventory_data:
        item = get_item_by_name(item_name)
        if item:
            inventory.append(item)
    return inventory

def load_game(filename):
    """Charge l'état du jeu depuis un fichier JSON."""
    try:
        with open(filename, 'r') as save_file:
            game_data = json.load(save_file)

        player_data = game_data['player']
        enemies_data = game_data['enemies']
        position = player_data['position']
        treasures_found = game_data['treasures_found']
        defeated_enemies = game_data['defeated_enemies']

        # Vérifier si le joueur est toujours en vie
        if not player_data['alive']:
            print("Le joueur est mort. Vous ne pouvez pas charger cette partie.")
            return None, [], (0, 0), 0, []

        # Créer une instance du joueur avec toutes les informations nécessaires
        player_instance = Player(
            name=player_data['name'],
            level=player_data['level'],
            health=player_data['health'],
            max_health=player_data['max_health'],
            attack=player_data['attack'],
            defense=player_data['defense'],
            inventory=load_inventory(player_data['inventory']),
            weapon=player_data['weapon'],
            experience=player_data['experience'],
            experience_to_next_level=player_data['experience_to_next_level']
        )

        # Créer des instances des ennemis avec les positions chargées
        enemies = [
            Enemy(
                enemy['name'],
                enemy['health'],
                enemy['max_health'],
                enemy['attack'],
                enemy['defense'],
                enemy['position'],  # Utilise la position chargée au lieu d'une position aléatoire
                enemy['level']
            )
            for enemy in enemies_data
        ]

        print("Partie chargée avec succès.")
        return player_instance, enemies, position, treasures_found, defeated_enemies

    except FileNotFoundError:
        print("Aucun fichier de sauvegarde trouvé.")
        return None, [], (0, 0), 0, []
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier de sauvegarde.")
        return None, [], (0, 0), 0, []