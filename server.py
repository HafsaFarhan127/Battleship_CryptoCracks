import random

def createGrid(size):
    grid = []
    for _ in range(size):
        row = [0 for _ in range(size)]
        grid.append(row)
    return grid

def printGrid(grid):
    for row in grid:
        print(' '.join(row))
    print()

def canPlaceShip(grid, row, col, direction, shipSize):
    # Check if the ship can be placed without going out of bounds or overlapping another ship
    if direction == 'H':
        if col + shipSize > len(grid):
            return False
        for i in range(shipSize):
            if grid[row][col + i] != 0:
                return False
    elif direction == 'V':
        if row + shipSize > len(grid):
            return False
        for i in range(shipSize):
            if grid[row + i][col] != 0:
                return False
    return True


def placeShip(grid, shipSize, shipSymbol):
    placed = False
    while not placed:
        direction = random.choice(['H', 'V'])
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid) - 1)
        if canPlaceShip(grid, row, col, direction, shipSize):
            if direction == 'H':
                for i in range(shipSize):
                    grid[row][col + i] = shipSymbol
            elif direction == 'V':
                for i in range(shipSize):
                    grid[row + i][col] = shipSymbol
            placed = True

def grid2ByteArray(grid):
    transmissionMatrix=[]
    for row in grid:
        for column in row:
            transmissionMatrix.append(column)
    bytearrayTransmission = bytearray(transmissionMatrix)
    return bytearrayTransmission

def byteArray2oneD(byteArray):
    transmissionMatrix = []
    for i in range(len(byteArray)):
        transmissionMatrix.append(byteArray[i])
    return byteArray

def oneD2byteArray(list1):
    return bytearray(list1)

gridSize = 10
global grid1,grid2
grid1 = createGrid(gridSize)
grid2 = createGrid(gridSize)

ships = [
    (5, 5),  # Ship of size 5
    (4, 4),  # Ship of size 4
    (3, 3),  # Ship of size 3
    (2, 2),  # Ship of size 2
    (1, 1)   # Ship of size 1
]

for shipSize, shipSymbol in ships:
    placeShip(grid1, shipSize, shipSymbol)

for shipSize, shipSymbol in ships:
    placeShip(grid2, shipSize, shipSymbol)

#two grids as one will be sent to each player and we need to store a local copy in the server for each
print(f'this is {grid1}')
print(f'this is {grid2}')


from socket import *
serverPort = 12001
# Create TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# Bind it
serverSocket.bind(('127.0.0.1', serverPort))
# Server begins listening for incoming TCP requests
serverSocket.listen(2) # Up to 2 clients in the queue
print('The server is ready to receive')

#Accept connections for Player 1 and Player 2
print("Waiting for Player 1...")
client1_socket, client1_address = serverSocket.accept()
print(f"Player 1 connected: {client1_address}")
client1_socket.sendall(grid2ByteArray(grid1))

print("Waiting for Player 2...")
client2_socket, client2_address = serverSocket.accept()
print(f"Player 2 connected: {client2_address}")
client2_socket.sendall(grid2ByteArray(grid2))

player1 = client1_socket  # Start with Player 1
player2 = client2_socket

# Notify players who starts
player1.sendall(oneD2byteArray([1]))
player2.sendall(oneD2byteArray([0]))

sunk=False

# Game Loop
while sunk==False:
    # try:
        # Notify the current player it's their turn
        player1.sendall(oneD2byteArray([1]))
        player2.sendall(oneD2byteArray([0]))
        #receive the attack coordinate from player1
        movePlayer1 = player1.recv(1024)

        if not movePlayer1:
            print("A player disconnected.")
            break
        
        #sending the attack to player2
        player2.sendall(movePlayer1)
        hitCheckByte = player2.recv(1024)
        hitCheck = byteArray2oneD(hitCheckByte)
        print(hitCheck)
        if hitCheck[1]==1:
            sunk=True

        #sending the attack response to player1
        player1.sendall(hitCheckByte)

        #Switch turns
        print(player1)
        print(player2)
        player1, player2 = player2, player1
        print(player1)
        print(player2)
        
    # except Exception as e:
    #     print("Error"+str(e))
    #     break
    
client1_socket.close()
client2_socket.close()
serverSocket.close()
print("Server shut down.")
