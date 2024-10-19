import json

def save_game(player, enemies, position, treasures_found, defeated_enemies):
    game_data = {
        'player': {
            'name': player.name,
            'health': player.health,
            'inventory': [item.name for item in player.inventory],
            'position': position,
            'experience': player.experience
        },
        'enemies': [
            {'name': enemy.name, 'health': enemy.health, 'position': enemy.position}
            for enemy in enemies if enemy.is_alive()
        ],
        'treasures_found': treasures_found
    }

    with open('save/saved_game.json', 'w') as save_file:
        json.dump(game_data, save_file, indent=4)
    print("Partie sauvegardée avec succès.")
