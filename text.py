from Maze.maze import Maze
from Bod.slaver import Slaver


def maze():
    the_maze = Maze(40, 10, 10)
    the_miner = Slaver()
    the_miner.dig(the_maze.cell(0, 0))
    while not the_miner.finished():
        the_miner._run()
    print(the_maze)


def menu():
    while True:
        print("* AMAZING MAZE *")
        print("* 1. Start     *")
        print("* 2. Quit      *")
        choice = int(input("Do you want to enter the maze?"))
        if choice == 1:
            maze()
        elif choice == 2:
            print("You MUST enter the Maze. To exit next time, use the hidden option 3.")
            maze()
        elif choice == 3:
            print("Fare thee well, O Maze traveller.")
            break
        else:
            print("That is an invalid option")

if __name__ == "__main__":
    menu()
