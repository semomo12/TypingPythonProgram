
"""Program for practicing typing on a keyboard."""

import functions

def main():
    """main function"""
    stop = False
    while not stop:
        functions.clean_console()
        print("""Typing test
1. Training - Easy
2. Training - Medium
3. Training - Hard
4. see high score
q) Quit.

Choose from the menu.""")

        choice = input("--> ")

        if choice == "q":
            functions.clean_console()
            print("Bye, and welcome back anytime!")
            stop = True

        elif choice == "1":
            functions.clean_console()
            try:
                functions.test_function("easy.txt")
            except FileNotFoundError:
                print("The file does not found.")
        elif choice == "2":
            functions.clean_console()
            try:
                functions.test_function("medium.txt")
            except FileNotFoundError:
                print("The file does not found.")
        elif choice == "3":
            functions.clean_console()
            try:
                functions.test_function("hard.txt")
            except FileNotFoundError:
                print("The file does not found.")
        elif choice == "4":
            functions.clean_console()
            try:
                print(functions.show_score_file("score.txt"))
            except FileNotFoundError:
                print("The file does not found.")
        else:
            print("That is not a valid choice. You can only choose from the menu.")

        if not stop:
            input("\nPress enter to continue...")

if __name__ == "__main__":
    main()
