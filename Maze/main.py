from Maze import Maze

# So this constructs a 'solid' maze that's yet to be tunnelled.
# and show() currently just shows the state of each room separately..
maze = Maze(6, 6)
#             X  Y
maze.ns_walls[0][1].make_door()
maze.ew_walls[1][0].make_door()
print maze

