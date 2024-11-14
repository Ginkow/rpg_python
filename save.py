import json
from player import Player
from ennemy import Enemy
from inventory import get_item_by_name
from datetime import datetime

# Generate a unique save file name based on the current date and time
def generate_save_name():
    """Generates a save file name based on the current date and time."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    return f"save/game_save_{timestamp}.json"

# Function to save the game state to a JSON file
def save_game(player, enemies, position, treasures_found, defeated_enemies, save_name):
    """Saves the game state to a JSON file."""
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
                'position': enemy.position,
                'level': enemy.level,
                'defeated': not enemy.is_alive() 
            }
            for enemy in enemies
        ],
        'treasures_found': treasures_found,
        'defeated_enemies': defeated_enemies
    }

    # Write game data to a JSON file
    with open(save_name, 'w') as save_file:
        json.dump(game_data, save_file, indent=4)
    print("Game saved successfully.")

# Function to load inventory from saved data
def load_inventory(inventory_data):
    """Loads the inventory from saved data."""
    inventory = []
    for item_name in inventory_data:
        item = get_item_by_name(item_name)
        if item:
            inventory.append(item)
    return inventory

# Function to load the game state from a JSON file
def load_game(filename):
    """Loads the game state from a JSON file."""
    try:
        with open(filename, 'r') as save_file:
            game_data = json.load(save_file)

        player_data = game_data['player']
        enemies_data = game_data['enemies']
        position = player_data['position']
        treasures_found = game_data['treasures_found']
        defeated_enemies = game_data['defeated_enemies']

        # Check if the player is alive before loading the game
        if not player_data['alive']:
            print("The player is dead. You cannot load this game.")
            return None, [], (0, 0), 0, []

        # Create a Player instance with loaded attributes
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

        # Create Enemy instances with loaded positions
        enemies = [
            Enemy(
                enemy['name'],
                enemy['health'],
                enemy['max_health'],
                enemy['attack'],
                enemy['defense'],
                enemy['position'],
                enemy['level']
            )
            for enemy in enemies_data
        ]

        print("Game loaded successfully.")
        return player_instance, enemies, position, treasures_found, defeated_enemies

    except FileNotFoundError:
        print("No save file found.")
        return None, [], (0, 0), 0, []
    except json.JSONDecodeError:
        print("Error reading the save file.")
        return None, [], (0, 0), 0, []
