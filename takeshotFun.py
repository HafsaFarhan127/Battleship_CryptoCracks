def takeShot(x,y):
  shot = grid[x][y]
  if shot!=0:
    print("hit")
    if shot == 1:
      grid[x][y]=0
      return 1
    elif shot == 2:
      grid[x][y]=0
      return 2
    elif shot == 3:
      grid[x][y]=0
      return 3
    elif shot == 4:
      grid[x][y]=0
      return 4
    elif shot == 5:
      grid[x][y]=0
      return 5
  else:
    return "miss"
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
shipCount = 0
x = int(input("Enter x coordinate: "))
y = int(input("Enter y coordinate: "))
while(shipCount!=5):
  result = takeShot(x,y)
  if result == 1:
    count1+=1
    if(count1 == 5):
      shipCount+=1
      print("ship 1 has been sunk")
  if result == 2:
    count2+=1
    if(count2 == 4):
      shipCount+=1
      print("ship 2 has been sunk")
  if result == 3:
    count3+=1
    if(count3 == 3):
      shipCount+=1
      print("ship 3 has been sunk")
  if result == 4:
    count4+=1
    if(count4 == 3):
      shipCount+=1
      print("ship 4 has been sunk")
  if result == 5:
    count5+=1
    if(count5 == 2):
      shipCount+=1
      print("ship 5 has been sunk")
  else:
    print(result)
  x = int(input("Enter x coordinate: "))
  y = int(input("Enter y coordinate: "))
