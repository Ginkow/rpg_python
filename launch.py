import os
import startgame
import about
import save

def list_saves(directory='save/', extension='.json'):
    """Liste tous les fichiers de sauvegarde dans le répertoire spécifié."""
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def game():
    while True:  # Boucle pour revenir au menu après chaque action
        print("Menu:")
        print("1. Create New Game")
        print("2. Load Saved Game")
        print("3. About")
        print("4. Exit \n")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Create New Game")
            startgame.start_game()  # Démarrer une nouvelle partie
        elif choice == "2":
            print("Load Saved Game")
            saves = list_saves()  # Liste des sauvegardes
            if not saves:
                print("Aucune sauvegarde trouvée.")
                continue
            
            print("Available saves:")
            for i, save_file in enumerate(saves, 1):
                print(f"{i}. {save_file}")

            save_choice = input("Choose a save to load (1-{}): ".format(len(saves)))
            try:
                save_index = int(save_choice) - 1
                if 0 <= save_index < len(saves):
                    player, enemies, current_position, treasures_found, defeated_enemies = save.load_game(saves[save_index])
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
        elif choice == "3":
            print("About")
            about.about()  # Afficher des informations sur le jeu (doit être implémenté)
        elif choice == "4":
            print("Exit")
            break  # Quitter le jeu
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    game()  # Lancer le menu principal
