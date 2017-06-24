Brief

A solvable, and interesting 2D maze written in Python 3.

Solvable = we must guarantee that there is at least one path from the entrance to the exit.
Interesting = there must be several non-trivial choices as to which path to take.

Each room (or cell) will be square and have from 1 to 4 exits, or be a wall...
We can represent this with an array.

The size of the maze can be configured, but we can start with eg. 50x50 cells.
Start-point and end-point can be from one corner to the opposite corner.

We need to be able to draw it. (Any ideas are good here, T).

Notes.
So, each room will have a doorway (or not) to it's neighbour, and on both sides, that state is the same.
-- Let's NOT have one-way doors, for the time being at least! So, all doorways are both exits/entrances.

So, a 4 by 4 set of cells can be represented ascii-wise as follows:
````
+-+-+-+-+
|   |   |
+-+ + +-+
|     | |
+-+ +-+ +
|       |
+ + +-+ +
| |   | |
+-+-+-+-+
````
Let's make the maze traversable - ie, no cell is inaccessible.

Although we want to be able to walk through the maze, for drawing it, it's easier to think of walls that need drawing.
Not only that, but (except for the outer wall) each wall is shared by two cells. 

Rather than thinking of a doorway as a mere absence of wall, we can keep it as a drawable. So then each wall is
either 'solid' or 'doorway'.

So we have some sort of 'wall' object that is drawable..
And then we have some sort of 'cell' object that refers to four walls.





Bla bla bla .. later on.
We will want to write a ‘maze solver’ later - so we will need to be able to provide a maze traversal functions, including eg.
cell.getExits()
move(direction)