# DisplaGuess_y MatriGuess_x and Option to choose encrGuess_yption or no encrGuess_yption mode
# DisplaGuess_y MatriGuess_x - Hafsa

def takeShot(SERVER_Guess_x,SERVER_Guess_y):
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
  
def displayPlayerGrid(grid):
   for row in grid:
        print(' '.join(row))

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
  

def byteArray2Grid(arrayByte):
    transmissionMatrix = []
    for i in range(len(arrayByte)):
        transmissionMatrix.append(arrayByte[i])
    grid = []
    for i in range(0, len(transmissionMatrix), 10):
        innerList = []
        for j in range(10):
            innerList.append(transmissionMatrix[i + j])
        grid.append(innerList)
    return grid

from socket import *
serverName = '127.0.0.1'
serverPort = 12001

# Create TCP socket and connect once
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

try:
    while True:
        # Receive the initial response or grid data
        response = clientSocket.recv(1024)
        grid = byteArray2Grid(response)
        print("Received grid:", grid)
        print(displayGuessMadeMatrix('hit',grid,0,0))




        # Input message to send to the server
        message = input('Input a message (or type "exit" to quit): ')

        # Check if the user wants to eGuess_xit
        if message.lower() == "exit":
            print("Closing connection.")
            break

        # Send the message in bGuess_ytes,here we will send take_shot message & user entered coordinates
        clientSocket.send(message.encode())

        #here send coordinates sent from client1 to client2 and vice versa



        #receive a response after sending a message and receive our grid from the server
        #maGuess_ybe we can use this for receiving the response for the attack coordinates sent
        response = clientSocket.recv(1024)
        #we should receive two things from server,coordinates and take_shot msg
        print("Server response:", response.decode())
        grid=response.decode()



finally:
    clientSocket.close()
    print("Client has exited.")

#this block of code to create the take shot msgs and then send to game server through socket alongwith coordinates guessed.
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
shipCount = 0
message=''

SERVER_Guess_x,SERVER_Guess_y= clientSocket.recv(1024) 
#maybe smthg like    SERVER_Guess_cordinates = clientSocket.recv(1024)  this is a list received as x,y which then is fed into the local take_shot

while(shipCount!=5):
#server guess means we will receive this corrdinates through the server from the other player,our programs take shot will create and send a take_shot msg to the other player,
#this take_shot is to be sent back to the server not used locally in any of our functions.
  result = takeShot(SERVER_Guess_x,SERVER_Guess_y)
  if result == 1:
    count1+=1
    if(count1 == 5):
      shipCount+=1
      message="ship 1 has been sunk"
      #changed from print to message as we want to send this to the game server not just print it.
      #the msg we receive from game server on behalf of other plaGuess_yer is what we will displaGuess_y.
  if result == 2:
    count2+=1
    if(count2 == 4):
      shipCount+=1
      message="ship 2 has been sunk"
  if result == 3:
    count3+=1
    if(count3 == 3):
      shipCount+=1
      message="ship 3 has been sunk"
  if result == 4:
    count4+=1
    if(count4 == 3):
      shipCount+=1
      message="ship 4 has been sunk"
  if result == 5:
    count5+=1
    if(count5 == 2):
      shipCount+=1
      message="ship 5 has been sunk"
  else:
    print(result)
  oldGuess_X=Guess_x
  oldGuess_Y=Guess_y
  Guess_x = int(input("Enter x coordinate: "))
  Guess_y = int(input("Enter y coordinate: "))
  #here entering an infinite loop,confused about how to order sending and receiving to sockets,as after first exchange 
  #theres an error for the function too. Maybe loop should be inside the while function

#GAMEFLOW -the functions here will  generate the take shot msg that will be sent to the server for the other user
  #1.here you enter a coorditante 
  # 2.then receive msg from server whether you hit or miss
  #3.then get displayed your guess matix
  #4.Then you make another guess