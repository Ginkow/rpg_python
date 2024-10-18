import startgame
import about
import save

def game():
    while True:  # Boucle pour revenir au menu après chaque action
        print("Menu:")
        print("1. Create New Game")
        print("2. Load Saved Game")
        print("3. About")
        print("4. Exit \n" )

        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Create New Game")
            startgame.start_game()  # Démarrer une nouvelle partie
        elif choice == "2":
            print("Load Saved Game")
            save.save()  # Charger une partie sauvegardée (doit être implémenté)
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
