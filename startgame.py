import random
import os 
import player
import ennemy
import inventory
import save
import startgameload
from datetime import datetime
from launch import game
import tresors
import time

BOSS_POSITION = (5, 5)

# Function to clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Generate a unique save file name based on the current date and time
def generate_save_name(base_name="game_save", directory='save/', extension='.json'):
    """Generates a save file name based on the current date and time, using .json extension."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_name = f"{directory}{base_name}_{timestamp}{extension}"
    return save_name

# Save the game state including the player's data, enemies, position, treasures, and defeated enemies
def save_game_state(player, enemies, position, treasures_found, defeated_enemies):
    save_name = generate_save_name()
    save.save_game(player, enemies, position, treasures_found, defeated_enemies, save_name)
    print(f"Game saved as {save_name}")

# Start a loaded game with the saved player data and game state
def start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies):
    """Starts a game with loaded data."""
    print(f"Starting the game with {player.name} at position {current_position}.")
    
    # Main loop to handle gameplay
    while player.is_alive() and enemies:
        print(f"You are at position {current_position}.")
        startgameload.start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies)

# Start a new game
def start_game():
    treasure = tresors.TREASURE_POSITION
    clear_terminal()
    print("Welcome to the game!")
    
    name = input("Enter your name to start the game: ")
    joueur = player.Player(name, 1, 100, 100, 20, 100, [], "sword", 0, 20)
    boss = ennemy.Enemy("Dragon", 1000, 1000, 30, 250, BOSS_POSITION, 430)
    
    print(f"Welcome, {joueur.name}!")
    print(f"You have {joueur.health} HP and your goal is to find all treasures while avoiding obstacles, monsters, and the final boss.")

    total_treasures = 1
    treasures_found = 0
    current_position = (0, 0)
    defeated_enemies = []
    treasures_collected = []

    inventory_displayed = False

    # Main game loop
    while joueur.health > 0:
        clear_terminal()
        
        # Display level-up message if applicable
        if joueur.level_up_message:
            print(joueur.level_up_message)
            joueur.level_up_message = ""
            
        # Display player status and game information
        print(f"Current Position: {current_position}, Treasures Found: {treasures_found}, Remaining Health: {joueur.health}, Remaining Shields: {joueur.defense}, Level: {joueur.level}")
        
        # # Display the positions of active enemies
        # active_enemies = [enemy for enemy in ennemy.enemies if enemy.name not in defeated_enemies]
        # for enemy in active_enemies:
        #     print(f"{enemy.name} Position: {enemy.position}")
            
        # # Display the treasure position if it exists
        # if tresors.TREASURE_POSITION is not None:
        #     print(f"Treasure Position: {tresors.TREASURE_POSITION}")
        
        # Show inventory if the player has toggled it
        if inventory_displayed:
            joueur.show_inventory()

        # Describe the player's current location
        describe_location()

        move = input("Enter your move (zqsd, go east, etc.) or press 'i' to toggle inventory, 'exit' to quit: \n")

        # Toggle inventory display if 'i' is pressed
        if move.lower() == 'i':
            inventory_displayed = not inventory_displayed
            continue 

        # Update position based on player's move
        new_position = update_position(move, current_position, joueur, ennemy.enemies, treasures_found, defeated_enemies)
        if new_position != current_position:
            current_position = new_position

        # Check for events such as enemy encounters or finding treasures
        for enemy in ennemy.enemies:
            if current_position == enemy.position and enemy.is_alive() and enemy.name not in defeated_enemies:
                print(f"A {enemy.name} attacks you!")
                
                # Ask the player if they want to use an item before combat
                action = input("Do you want to use an item before fighting? (yes/no): ")
                if action.lower() == "yes":
                    combat(joueur, enemy, defeated_enemies)

                if joueur.health <= 0:
                    print("You have died. Game over.")
                    time.sleep(2)
                    clear_terminal()
                    return

        # Handle treasure collection
        if current_position == treasure:
            if "treasure_1" not in treasures_collected:
                print("You found a treasure!\n")
                treasures_found += 1

                # Generate random loot and add to inventory
                loot = inventory.generate_random_loot()
                item_names = [item.name for item in loot]
                print(f"You collected {item_names[0]} and {item_names[1]}.\n")
                for item in loot:
                    joueur.pickup_item(item)

                treasures_collected.append("treasure_1")
                tresors.mark_treasure_collected() 
                input("\nPress Enter to continue...")

            else:
                print("You have already collected this treasure.\n")
                input("\nPress Enter to continue...")
            
            continue
        
        # Check if all treasures are found
        if treasures_found == total_treasures:
            print("Congratulations! You found all treasures!")
            treasure = None
            continue

        # Handle final boss encounter
        elif current_position == BOSS_POSITION:
            print("You found the boss! Prepare for battle.")
            if combat(joueur, boss, defeated_enemies):
                print("You defeated the boss and won the game!\n")
                time.sleep(2)
                clear_terminal()
                game()
                break
            else:
                print("You lost against the boss. Game over.\n")
                time.sleep(2)
                clear_terminal()
                game()
                break

        if joueur.health <= 0:
            print("Game over! You have no health left.\n")
            break


# Function to describe the player's current location
def describe_location():
    descriptions = [
        "You are in a dark forest.",
        "You arrive near a noisy river.",
        "You are in a sunny clearing.",
        "You enter a damp, dark cave."
    ]
    print(random.choice(descriptions))

# Update the player's position based on input
def update_position(move, current_position, player, enemies, treasures_found, defeated_enemies):
    x, y = current_position
    
    # Handle player exit
    if move == "exit":
        confirm_exit = input("Do you want to quit the game? (yes/no): ")
        if confirm_exit.lower() == "yes":
            save_game = input("Do you want to save before quitting? (yes/no): ")
            if save_game.lower() == "yes":
                save_name = generate_save_name()
                save.save_game(player, enemies, current_position, treasures_found, defeated_enemies, save_name)
                print("Game saved. Goodbye!")
            else:
                print("Exiting without saving. Goodbye!")
            exit()

    # Normal movement handling
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
        print("Invalid move.")
    
    return current_position

# Combat function for handling player and enemy actions
def combat(player, enemy, defeated_enemies):
    while enemy.is_alive() and player.health > 0:
        print(f"\n*** Battle with {enemy.name} (Level {enemy.level}) ***")
        print(f"{player.name}: {player.health}/{player.max_health} HP, {player.defense} shield.")
        print(f"{enemy.name}: {enemy.health}/{enemy.max_health} HP, {enemy.defense} shield.\n")

        # Player's turn
        print("\nYour turn!")
        action = input("What do you want to do? (1: Attack, 2: Use an item):\n ")

        if action == "1":
            print(f"{player.name} attacks {enemy.name}!")
            player.attack_target(enemy)
        elif action == "2":
            # Use item from inventory if available
            if not player.inventory:
                print("Inventory empty, performing a normal attack.\n")
                player.attack_target(enemy)
            else:
                player.show_inventory()
                item_name = input("Which item do you want to use? : ")
                player.use_item(item_name, target=enemy)

        if not enemy.is_alive():
            print(f"{enemy.name} has been defeated!")
            defeated_enemies.append(enemy.name)
            enemy.defeat()
            exp_gained = enemy.level
            player.gain_experience(exp_gained)
            print(f"You gained {exp_gained} experience points for defeating {enemy.name}!\n")

            loot = enemy.generate_loot()
            for item in loot:
                print(f"{enemy.name} drops {item.name} ({item.rarity}).")
                player.pickup_item(item)
            input("Press Enter to continue...")
            return True

        # Enemy's turn to attack
        print(f"\n{enemy.name}'s turn to attack!")
        enemy.attack_player(player)

        # Check if player is still alive
        if player.health <= 0:
            print(f"{player.name} was defeated by {enemy.name}.")
            return False 

    return player.health > 0
