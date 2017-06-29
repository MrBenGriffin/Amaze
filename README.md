# Amaze
Simple fun learning project.

```By Ben & Tay & Cheddies```
## Requires:
Python 3  
tkinter How to install( http://www.tkdocs.com/tutorial/install.html )  
typing (pip3 install typing)

```python
Miner.dig() # Now works pretty well for a random walk.
```

## Launching:
python3 ./front.py for the GUI
python3 ./InitialMenu.py for text. (TODO: sizing options)

## So far:
Currently I'm not planning on adding unit tests.  Maybe one day.

## Todo:
So, out of basic simple reasons, I chose tkinter as a gfx fe. 
There's stuff to love in tkinter for a project of this scale.

![Maze](maze.png)

We need a mover class - with two subclasses:
√ Digger/Miner    - who constructs the maze (and leaves runes lying around)
* Adventurer      - who travels through the maze interactively.
* Robot           - who travels through the maze. automatically.

## Novelty fun: 
√ Animated miner
extra - add 'power runes':  
A rune can be used just once to open a rune-door.  
One can carry only one rune at a time.   
Running over a rune picks it up, (and drops off any currently held)  
Rune-doors: Are they opened once opened, or do they allow a single transit? 
Multiple players (sharing a keyboard of course).
Stairs that go both up and down.
Rooms.
Monsters.
Treasure.
Nethack.... ;-D

 
 
 
