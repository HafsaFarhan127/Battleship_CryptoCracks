def displayGuessMadeMatrix(SERVER_take_shotMsg,grid,oldGuess_X,oldGuess_Y):
   #will take old user guess and put value at guess acc to msg received from server
  if SERVER_take_shotMsg=='hit':
      grid[oldGuess_X][oldGuess_Y]='x'
  if SERVER_take_shotMsg=='miss':
      grid[oldGuess_X][oldGuess_Y]='m'
  
  # Print column numbers at the top
  print("   ", end="")  # Add spaces for alignment
  for i in range(10):
      print(i, end="  ")  # Print column headers
  print()  # Move to the next line
    # Print a line below the headers
  print("  " + "-" * 30)
    # Print each row with its row number
  for j in range(10):
      print(j, "|", end=" ")  # Print row number with a separator
      for cell in grid[j]:
          print(cell, end="  ")  # Print each cell with spaces
      print()  # Move to the next line
  return grid
def createGrid(size):
    grid = []
    for _ in range(size):
        row = [0 for _ in range(size)]
        grid.append(row)
    return grid

grid=createGrid(10)
grid[0][0]=1
print(grid)
displayGuessMadeMatrix('hit',grid,0,0)
print(grid)