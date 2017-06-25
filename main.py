from Maze.maze import Maze

# So this constructs a 'solid' maze that's yet to be tunnelled.
# and show() currently just shows the state of each room separately..
maze = Maze(8, 6)

#  Test that we can make doors.
#             X  Y
maze.ns_walls[0][1].make_door()
maze.ew_walls[1][0].make_door()
maze.ns_walls[2][1].make_door()

#  Bad maze! But at least we can knock walls out.

#  Display the maze.
print(maze)

