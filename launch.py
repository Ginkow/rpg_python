import os
import startgame
import about
import save

# Function to list all save files in the specified directory with a specific file extension
def list_saves(directory='save/', extension='.json'):
    """Lists all save files in the specified directory with the given file extension."""
    return [f for f in os.listdir(directory) if f.endswith(extension)]

# Main game menu function, which loops until the user chooses to exit
def game():
    while True:
        # Display the main menu options
        print("Menu:")
        print("1. Create New Game")
        print("2. Load Saved Game")
        print("3. About")
        print("4. Exit \n")

        # Get user input to select a menu option
        choice = input("Enter your choice: ")
        
        # Handle the user's choice
        if choice == "1":
            print("Create New Game")
            startgame.start_game()
        elif choice == "2":
            print("Load Saved Game")
            saves = list_saves()
            if not saves:
                print("No save files found.")
                continue
            
            # Display all available save files to the user
            print("Available saves:")
            for i, save_file in enumerate(saves, 1):
                print(f"{i}. {save_file}")

            # Get user input for which save file to load
            save_choice = input("Choose a save to load (1-{}): ".format(len(saves)))
            try:
                save_index = int(save_choice) - 1
                # Load the chosen save file if the choice is valid
                if 0 <= save_index < len(saves):
                    player, enemies, current_position, treasures_found, defeated_enemies = save.load_game(f'save/{saves[save_index]}')
                    # Start the loaded game with the saved state
                    startgame.start_loaded_game(player, enemies, current_position, treasures_found, defeated_enemies)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            startgame.clear_terminal()
            about.about()
        elif choice == "4":
            print("Au revoir et à bientôt")
            break 
        else:
            print("Invalid choice!")

# Run the game menu if this file is executed as the main program
if __name__ == "__main__":
    game()
