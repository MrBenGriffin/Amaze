def menu():
  while True:
    print("*AMAZING MAZE*)
    print("*1. Start    *")
    print("*2. Quit     *")
    choice = int(input("Do you want to enter the maze?"))
    if choice == 1:
      Maze()
    elif choice == 2:
      break
    else:
      print("That is an invalid option")
