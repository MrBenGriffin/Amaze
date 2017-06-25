def menu(maze, *args):
    while True:
        print("* AMAZING MAZE *")
        print("* 1. Start     *")
        print("* 2. Quit      *")
        choice = int(input("Do you want to enter the maze?"))
        if choice == 1:
            maze(*args)
        elif choice == 2:
            print("You MUST enter the Maze. To exit next time, use the hidden option 3.")
            maze(*args)
        elif choice == 3:
            print("Fare thee well, O Maze traveller.")
            break
        else:
            print("That is an invalid option")
