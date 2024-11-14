import random
import os
import ennemy
import save
from datetime import datetime
import inventory
import player
from launch import game
import tresors
import time

BOSS_POSITION = (5, 5)

# Generate a unique save file name based on the current date and time
def generate_save_name(base_name="game_save", directory='save/', extension='.json'):
    """Generates a unique save file name based on the current date and time, avoiding duplicates."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_name = f"{base_name}_{timestamp}{extension}"
    
    i = 1
    while os.path.exists(os.path.join(directory, save_name)):
        save_name = f"{base_name}_{timestamp}_{i}{extension}"
        i += 1
    
    return os.path.join(directory, save_name)

# Function to clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Start a loaded game with saved player data and game state, excluding defeated enemies
def start_loaded_game(loaded_player, saved_enemies_data, current_position, treasures_found, defeated_enemies):
    """Starts a game with loaded data, excluding already defeated enemies."""
    print(f"Starting the game with {loaded_player.name} at position {current_position}.")

    treasure = tresors.TREASURE_POSITION
    
    # Load remaining enemies, excluding those that have been defeated
    enemies = []
    for enemy in saved_enemies_data:
        if enemy.name in defeated_enemies:
            continue
        enemies.append(enemy)

    # Set the player's current position
    loaded_player.position = current_position

    # Initialize the boss
    boss = ennemy.Enemy("Dragon", 1000, 1000, 30, 250, BOSS_POSITION, 430)
    loaded_player = player.Player(
        loaded_player.name, loaded_player.level, loaded_player.health, 
        loaded_player.max_health, loaded_player.attack, loaded_player.defense, 
        loaded_player.inventory, "sword", loaded_player.experience, 
        loaded_player.experience_to_next_level, current_position
    )
    
    total_treasures = 1
    inventory_displayed = False
    treasures_collected = []

    # Main game loop
    while loaded_player.is_alive() and enemies:
        
        # Display level-up message if applicable
        if loaded_player.level_up_message:
            print(loaded_player.level_up_message)
            loaded_player.level_up_message = ""
            
        clear_terminal()
        print(f"You are at position {loaded_player.position}. Treasures found: {treasures_found}, Remaining health: {loaded_player.health}, Remaining shield: {loaded_player.defense}, Level: {loaded_player.level}")
        
        # # Display positions of active (not defeated) enemies
        # active_enemies = [enemy for enemy in ennemy.enemies if enemy.name not in defeated_enemies]
        # for enemy in active_enemies:
        #     print(f"Position of {enemy.name}: {enemy.position}")
        
        # # Display the position of the treasure if it hasn't been found yet
        # if treasures_found < total_treasures:
        #     print(f"Treasure position: {tresors.TREASURE_POSITION}")
        # else:
        #     tresors.mark_treasure_collected()
        
        # Show inventory if the player has toggled it
        if inventory_displayed:
            loaded_player.show_inventory()

        # Describe the player's current location
        describe_location()

        # Get the player's movement input
        move = input("Enter your move (zqsd, go east, etc.) or press 'i' to toggle inventory, 'exit' to quit: ")
        
        # Toggle inventory display if 'i' is pressed
        if move.lower() == 'i':
            inventory_displayed = not inventory_displayed
            continue

        # Update position based on the player's input
        new_position = update_position(move, loaded_player.position, loaded_player, enemies, treasures_found, defeated_enemies)
        if new_position != loaded_player.position:
            loaded_player.position = new_position
            current_position = new_position

        # Event handling, such as enemy encounters
        for enemy in ennemy.enemies:
            if current_position == enemy.position:
                if enemy.name in defeated_enemies:
                    continue  # Skip defeated enemies
                elif enemy.is_alive():
                    print(f"A {enemy.name} attacks you!")
                                        
                    # Ask if the player wants to use an item before combat
                    action = input("Do you want to use an item before fighting? (Y/N): ")
                    if action.lower() == "y":
                        combat(loaded_player, enemy, defeated_enemies)

                    # End the game if the player dies
                    if loaded_player.health <= 0:
                        print("You have died. Game over.")
                        time.sleep(2)
                        clear_terminal()
                        game()
                        return

        # Check if player found the treasure
        if current_position == treasure:
            if "treasure_1" not in treasures_collected:
                print("You found a treasure!\n")
                treasures_found += 1

                # Generate two random items and add them to the player's inventory
                loot = inventory.generate_random_loot()
                item_names = [item.name for item in loot]
                print(f"You collected {item_names[0]} and {item_names[1]}.\n")
                for item in loot:
                    loaded_player.pickup_item(item)

                treasures_collected.append("treasure_1")
                tresors.mark_treasure_collected()
                input("\nPress Enter to continue...")

            else:
                print("You have already collected this treasure.\n")
                input("\nPress Enter to continue...")
            
            continue
        
        # Check if the player found all treasures
        if treasures_found == total_treasures:
            print("Congratulations! You found all the treasures!")
            treasure = None
            continue

        # Check if player encounters the boss
        elif current_position == BOSS_POSITION:
            print("You have encountered the boss! Do you want to engage in battle?")
            
            # Ask the player if they want to fight the boss
            fight_boss = input("Do you want to fight the boss? (Y/N): ")
            
            if fight_boss.lower() == "y":
                print("Prepare for battle!")
                
                if combat(loaded_player, boss, defeated_enemies):
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
            else:
                print("You chose to avoid the boss. Move carefully!")
                # Continue the game loop without fighting the boss
                continue

        # End game if the player has no health left
        if loaded_player.health <= 0:
            print("Game over! You have no health left.")
            break

# Describe the player's current location with random messages
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
    
    # Handle player exit request
    if move == "exit":
        confirm_exit = input("Do you want to quit the game? (Y/N): ")
        if confirm_exit.lower() == "y":
            save_game = input("Do you want to save the game before quitting? (Y/N): ")
            if save_game.lower() == "y":
                save_name = generate_save_name()
                save.save_game(player, enemies, current_position, treasures_found, defeated_enemies, save_name)
                print("Game saved. Goodbye!")
            else:
                print("Exiting without saving. Goodbye!")
            exit()

    # Handle normal movement based on player's input
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
        while True:  # Repeat until a valid action is taken
            print("\nYour turn!")
            action = input("What do you want to do? (1: Attack, 2: Use an item): ")

            if action == "1":
                print(f"{player.name} attacks {enemy.name}!")
                player.attack_target(enemy)
                break  # Exit the action loop and continue combat
            elif action == "2":
                # Use item from inventory if available
                if not player.inventory:
                    print("Inventory empty, performing a normal attack.\n")
                    player.attack_target(enemy)
                    break  # Exit the action loop and continue combat
                else:
                    player.show_inventory()
                    item_choice = input("Which item do you want to use? (Type 'back' to return to main menu): ")

                    # Allow the player to go back to the main combat menu
                    if item_choice.lower() == "back":
                        print("Returning to main menu.")
                        continue  # Restart the action loop

                    # Attempt to use the chosen item if valid
                    player.use_item(item_choice, target=enemy)
                    break  # Exit the action loop and continue combat
            else:
                print("Invalid choice. Please select 1 or 2.")

        # Check if the enemy was defeated
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

