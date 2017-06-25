from Maze.maze import Maze
from InitialMenu import menu


def maze():
    # So this constructs a 'solid' maze that's yet to be tunnelled.
    # and show() currently just shows the state of each room separately..
    the_maze = Maze(8, 6)

    #  Test that we can make doors.
    #             X  Y
    the_maze.ns_walls[0][1].make_door()
    the_maze.ew_walls[1][0].make_door()
    the_maze.ns_walls[2][1].make_door()

    #  Bad maze! But at least we can knock walls out.

    #  Display the maze.
    print(the_maze)

    #  What? No interaction?! Well, let's generate the maze first!!


if __name__ == "__main__":
    menu(maze)


