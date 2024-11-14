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
            print(column)
            transmissionMatrix.append(column)
    bytearrayTransmission = bytearray(transmissionMatrix)
    return bytearrayTransmission

gridSize = 10
global grid1,grid2
grid1 = createGrid(gridSize)
grid2 = createGrid(gridSize)

ships = [
    (5, 1),  # Ship of size 5
    (4, 2),  # Ship of size 4
    (3, 3),  # Ship of size 3
    (3, 4),  # Ship of size 3
    (2, 5)   # Ship of size 2
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
serverSocket.listen(10) # Up to 10 clients in the queue
print('The server is ready to receive')
# Wait for connection requests (loop forever)
while True:
    # The server waits on accept() for incoming requests
    # A new socket created on return for every client

    #can we distinguish between each client?liek have different coonections for each client?
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send(grid2ByteArray(grid1))

    #Getting message from the client
    # Read bytes from socket (but not the address as in UDP)
    message = connectionSocket.recv(1024)
    print(message)

    
    # Close connection to this client (but not welcoming socket)
    connectionSocket.close()