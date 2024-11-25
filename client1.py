import socket

def byteArrayToGrid(byteArray, size):
    grid = []
    for i in range(0, len(byteArray), size):
        grid.append(list(byteArray[i:i + size]))
    return grid

def byteArrayToList(byteArray):
    return [int(byte) for byte in byteArray]

def listToByteArray(data):
    return bytearray(data)

def displayGrid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

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

# Server connection
host = '127.0.0.1'
port = 12001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server")

# Initialize grids
gridSize = 10
myGrid = byteArrayToGrid(client_socket.recv(1024), gridSize)
guessGrid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]



print("Your Grid:")
displayGrid(myGrid)

while True:
    try:
        # Wait for turn signal
        server_message = byteArrayToList(client_socket.recv(1024))
        if 2 in server_message:  # Game over
            print("Game over! You lose.")
            break
        if 1 in server_message:  # Player's turn
            while True:
                try:
                    # Prompt user for coordinates
                    x, y = map(int, input("Enter coordinates to attack (x, y): ").split(","))
                    
                    # Check if the input is within valid range (assuming a 10x10 grid)
                    if 0 <= x < 10 and 0 <= y < 10:
                        break  # Valid input; exit the loop
                    else:
                        print("Coordinates out of bounds. Please enter values between 0 and 9.")
                except ValueError:
                    # Handle non-integer or invalid input
                    print("Invalid input format. Please enter two integers separated by a comma.")
            client_socket.sendall(listToByteArray([x, y]))
            result = byteArrayToList(client_socket.recv(1024))
            if result[1] == 1:
                print("You sunk the ship! You win!")
                break
            print(result)
            if result[0]==1:
                print()
                print("HIT!")
                print()
                displayGuessMadeMatrix("hit",guessGrid,x,y)
            else:
                print()
                print("MISS!")
                print()
                displayGuessMadeMatrix("miss",guessGrid,x,y)
            
        elif 0 in server_message:  # Opponent's turn
            print("Waiting for opponent's move...")
            move = byteArrayToList(client_socket.recv(1024))
            x, y = move
            if myGrid[x][y] !=0 and myGrid[x][y]!="X":
                print("You got HIT!")
            else:
                print("Opponent Missed!")          
            result = "HIT" if myGrid[x][y] != 0 else "MISS"
            myGrid[x][y] = 0
            sink = 1 if sum(sum(row) for row in myGrid) == 0 else 0
            client_socket.sendall(listToByteArray([1 if result == "HIT" else 0, sink]))
            if sink == 1:
                print("All ships sunk! You lose.")
                break
    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
print("Disconnected from the server.")
