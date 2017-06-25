from Maze.maze import Maze
from Maze.wall import Com
from InitialMenu import menu


def maze():
    # So this constructs a 'solid' maze that's yet to be tunnelled.
    # and show() currently just shows the state of each room separately..
    the_maze = Maze(8, 6)

    #  Add some doors, put a rune down..
    the_maze.make_door(0, 0, Com.S)  # I want Out!! No...
    the_maze.make_door(0, 0, Com.N)
    the_maze.make_door(0, 0, Com.E)
    the_maze.make_door(1, 0, Com.E)
    the_maze.make_door(1, 0, Com.N)
    the_maze.make_door(1, 1, Com.E)
    the_maze.make_door(1, 1, Com.N, 'a')  # Rune door. Needs the rune 'A'.
    the_maze.change_rune(0, 1, 'a')  # Put a rune onto the floor of room 0, 0

    #  Bad maze! But at least we can knock walls out.
    exits = the_maze.exits(1, 1)  # {<Com.N: 'N'>: [a], <Com.S: 'S'>: [ ], <Com.E: 'E'>: [ ]}
    print(exits)

    #  Display the maze.
    print(the_maze)

    #  What? No interaction?! Well, let's generate the maze first!!


if __name__ == "__main__":
    menu(maze)  #

