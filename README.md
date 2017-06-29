# Amaze
Simple fun learning project.

```By Ben & Tay & Cheddies```
## Requires:
Python 3  
tkinter (apt-get install python-tk on ubuntu - but may well be packaged with python)  
typing (pip3 install typing)



## Launching:
python3 ./front.py for the GUI

## So far:
Currently I'm not planning on adding unit tests.  Maybe one day.

## Todo:
So, out of basic simple reasons, I chose tkinter as a gfx fe.

![Maze](maze.png)

We need a mover class - with two subclasses:
* Digger/Miner    - who constructs the maze (and leaves runes lying around)
* Adventurer      - who travels through the maze interactively.
* Robot           - who travels through the maze. automatically.

## Novelty fun: 
Total extra - add 'power runes':  
A rune can be used just once to open a rune-door.  
One can carry only one rune at a time.   
Running over a rune picks it up, (and drops off any currently held)  
Rune-doors: Are they opened once opened, or do they allow a single transit?  
 
 
 
