import random
from socket import *

# Helper functions
def createGrid(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def canPlaceShip(grid, row, col, direction, shipSize):
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
    while True:
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
            break

def gridToByteArray(grid):
    return bytearray([cell for row in grid for cell in row])

def byteArrayToList(byteArray):
    return [int(byte) for byte in byteArray]

def listToByteArray(data):
    return bytearray(data)

# Ship configuration
ships = [(5, 5), (4, 4), (3, 3), (3, 3), (2, 2)]

# Server setup
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(2)
print('The server is ready to receive')

# Create grids
gridSize = 10
grid1 = createGrid(gridSize)
grid2 = createGrid(gridSize)

for shipSize, shipSymbol in ships:
    placeShip(grid1, shipSize, shipSymbol)
    placeShip(grid2, shipSize, shipSymbol)

# Accept connections
print("Waiting for Player 1...")
player1_socket, _ = serverSocket.accept()
print("Player 1 connected")
player1_socket.sendall(gridToByteArray(grid1))

print("Waiting for Player 2...")
player2_socket, _ = serverSocket.accept()
print("Player 2 connected")
player2_socket.sendall(gridToByteArray(grid2))

# Initialize game variables
attacker, defender = player1_socket, player2_socket
attacker_grid, defender_grid = grid1, grid2
game_over = False

# Game loop
while not game_over:
    try:
        # Notify players of turn
        print(f"Attacker: {'Player 1' if attacker == player1_socket else 'Player 2'}")
        print(f"Defender: {'Player 1' if defender == player1_socket else 'Player 2'}")
        
        attacker.sendall(listToByteArray([1]))  # Notify attacker it's their turn
        defender.sendall(listToByteArray([0]))  # Notify defender to wait

        # Receive attack coordinates from attacker
        move = byteArrayToList(attacker.recv(1024))
        x, y = move
        print(f"Player {'1' if attacker == player1_socket else '2'} attacks: ({x}, {y})")

        # Process attack
        hit = 1 if defender_grid[x][y] != 0 else 0
        defender_grid[x][y] = 0 if hit else defender_grid[x][y]
        sink = 1 if sum(sum(row) for row in defender_grid) == 0 else 0

        # Send attack result to attacker
        attacker.sendall(listToByteArray([hit, sink]))

        # Check if game is over
        if sink == 1:
            print(f"Player {'1' if attacker == player1_socket else '2'} wins!")
            attacker.sendall(listToByteArray([2]))  # 2 indicates game over to attacker
            defender.sendall(listToByteArray([2]))
            game_over = True
            break

        # Forward attack coordinates to defender
        defender.sendall(listToByteArray(move))

        # Defender processes the attack and responds
        response = byteArrayToList(defender.recv(1024))
        print(f"Player {'1' if defender == player1_socket else '2'} responds with: {response}")


        # Switch roles
        attacker, defender = defender, attacker
        attacker_grid, defender_grid = defender_grid, attacker_grid

    except Exception as e:
        print(f"Error: {e}")
        break

# Close connections
player1_socket.close()
player2_socket.close()
serverSocket.close()
print("Server shut down.")
