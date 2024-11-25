import socket

def takeShot(grid,SERVER_Guess_x,SERVER_Guess_y):
  shot = grid[SERVER_Guess_x][SERVER_Guess_y]
  if shot!=0:
    print("hit")
    if shot == 1:
      grid[SERVER_Guess_x][SERVER_Guess_y]=0
      return 1
    elif shot == 2:
      grid[SERVER_Guess_x][SERVER_Guess_y]=0
      return 2
    elif shot == 3:
      grid[SERVER_Guess_x][SERVER_Guess_y]=0
      return 3
    elif shot == 4:
      grid[SERVER_Guess_x][SERVER_Guess_y]=0
      return 4
    elif shot == 5:
      grid[SERVER_Guess_x][SERVER_Guess_y]=0
      return 5
  else:
    return "miss"

def byteArray2Grid(arrayByte):
    transmissionMatrix = []
    for i in range(len(arrayByte)):
        transmissionMatrix.append(arrayByte[i])
    grid = []
    for i in range(0, len(transmissionMatrix), 10):
        grid.append(transmissionMatrix[i:i + 10])
    return grid


def oneD2byteArray(list1):
    return bytearray(list1)


def byteArray2oneD(byteArray):
    transmissionMatrix = []
    for i in range(len(byteArray)):
        transmissionMatrix.append(byteArray[i])
    return transmissionMatrix


def displayGuessMadeMatrix(server_msg, grid, x, y):
    if server_msg.lower() == "hit":
        grid[x][y] = 'X'
    elif server_msg.lower() == "miss":
        grid[x][y] = 'O'

    # Display updated grid
    print("   ", end="")
    for i in range(10):
        print(i, end="  ")
    print("\n  " + "-" * 30)
    for i, row in enumerate(grid):
        print(f"{i} | {'  '.join(map(str, row))}")


def createGrid(size):
    return [[0 for _ in range(size)] for _ in range(size)]


# Server connection
host = '127.0.0.1'
port = 12001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"Connected to the game server at {host}:{port}")

# Initialize grids
guessGrid = createGrid(10)  # Grid for tracking guesses
myGrid = byteArray2Grid(client_socket.recv(1024))  # Receive initial grid from server

print("Your Grid:")
for row in myGrid:
    print(' '.join(map(str, row)))
print()
sink=False
# Main game loop
while True:
    # try:
        # Wait for the server's message
        server_message = byteArray2oneD(client_socket.recv(1024))
        # Check if it's the player's turn
        if 1 in server_message:
            print("\nYour turn!")
            attackCoordinates=[]
            x, y = map(int, input("Enter coordinates to attack (format: x,y): ").split(","))
            attackCoordinates.append(x)
            attackCoordinates.append(y)
            client_socket.sendall(oneD2byteArray(attackCoordinates))  # Send attack coordinates to the server

            # Receive the result of the attack
            attack_result = byteArray2oneD(client_socket.recv(1024))
            print(attack_result)
            if attack_result[0] == 1 and attack_result[1] == 1:
               print(f"Result of your attack: HIT!")
               print("You Win!")
               break
            if attack_result[0] == 1 and attack_result[1] == 1:
               attack_result="HIT"
            else:
               attack_result="MISS"
            
            print(f"Result of your attack: {attack_result}")
            print("Opponent's Grid:")
            displayGuessMadeMatrix(attack_result, guessGrid, x, y)

            # Update the guess grid
            guessGrid = displayGuessMadeMatrix(attack_result, guessGrid, x, y)
        elif 0 in server_message:
            print("\nWaiting for the other player's move...")

            # Receive attack coordinates and result from the server
            opponent_attack = byteArray2oneD(client_socket.recv(1024))
            
            for i in range(len(opponent_attack)):
               opponent_attack[i]=int(opponent_attack[i])

            print(f"Opponent attacked at {opponent_attack}")

            x=opponent_attack[0]
            y=opponent_attack[1]

            if myGrid[x][y] != 0:
                result = "HIT"
                takeShot(myGrid,x,y)
                print("Updated Grid:")
                print(myGrid)
                sum=0
                for i in myGrid:
                   sum=sum+sum(i)
                if sum==0:
                   sink=True
                   print("YOU LOSE!")
            else:
                result = "MISS"

            resultArray=[]
            if result=="HIT":
               resultArray.append(1)
            else:
               resultArray.append(0)

            if not sink:
               resultArray.append(0)
            else:
               resultArray.append(1)
            
            print(resultArray)
            client_socket.sendall(oneD2byteArray(resultArray))  # Send attack result to the server

            print("\nYour updated grid:")
            for row in myGrid:
                print(row)

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     break

client_socket.close()
print("Disconnected from the server.")