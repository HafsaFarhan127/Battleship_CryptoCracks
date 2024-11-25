import random
from socket import *
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import struct

# Helper functions for encryption
def pad_data(data, block_size):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len] * pad_len)

def unpad_data(data):
    pad_len = data[-1]
    return data[:-pad_len]

def aes_encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return iv + cipher.encrypt(pad_data(data, 16))

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad_data(cipher.decrypt(ciphertext))

# Ship configuration
ships = [(5, 5), (4, 4), (3, 3), (3, 3), (2, 2)]

# Server setup
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(2)
print('The server is ready to receive')

# Encryption configuration
encryption = input("Do you want the communication in Encryption Mode?")
while encryption.lower() !="yes" and encryption.lower() != "no":
    print("Enter yes/no")
    encryption = input("Do you want the communication in Encryption Mode?")

if encryption=="yes":
    encryption_mode = True
else:
    encryption_mode = False
encryption_flag = bytearray([1 if encryption_mode else 0])

aes_key = get_random_bytes(16) if encryption_mode else None

def send_encrypted(socket, data):
    if encryption_mode:
        encrypted_data = aes_encrypt(data, aes_key)
        # Send the length of the encrypted data followed by the data itself
        socket.sendall(struct.pack("!I", len(encrypted_data)) + encrypted_data)
    else:
        socket.sendall(data)

def receive_encrypted(socket):
    # Read the length of the incoming data
    data_length = struct.unpack("!I", socket.recv(4))[0]
    data = socket.recv(data_length)
    if encryption_mode:
        return aes_decrypt(data, aes_key)
    return data

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
player1_socket.sendall(encryption_flag)
if encryption_mode:    
    print("Sending AES key to Player 1...")
    player1_socket.sendall(aes_key)  # Send the AES key to Player 1

print("Grid before encryption (Player 1):", grid1)
send_encrypted(player1_socket, gridToByteArray(grid1))

print("Waiting for Player 2...")
player2_socket, _ = serverSocket.accept()
player2_socket.sendall(encryption_flag)
if encryption_mode:    
    print("Sending AES key to Player 2...")
    player2_socket.sendall(aes_key)  # Send the AES key to Player 2

print("Grid before encryption (Player 2):", grid2)
send_encrypted(player2_socket, gridToByteArray(grid2))

# Initialize game variables
attacker, defender = player1_socket, player2_socket
attacker_grid, defender_grid = grid1, grid2
game_over = False

# Game loop
while not game_over:
    try:
        # Notify players of turn
        send_encrypted(attacker, bytearray([1]))
        send_encrypted(defender, bytearray([0]))

        # Receive attack coordinates from attacker
        move = byteArrayToList(receive_encrypted(attacker))
        x, y = move

        # Process attack
        hit = 1 if defender_grid[x][y] != 0 else 0
        defender_grid[x][y] = 0 if hit else defender_grid[x][y]
        sink = 1 if sum(sum(row) for row in defender_grid) == 0 else 0

        # Send attack result to attacker
        send_encrypted(attacker, bytearray([hit, sink]))

        # Check if game is over
        if sink == 1:
            send_encrypted(attacker, bytearray([2]))
            send_encrypted(defender, bytearray([2]))
            game_over = True
            break

        # Forward attack coordinates to defender
        move = [x, y]  # Ensure move is always a list of two integers
        print(f"Sending move to defender: {move}")
        send_encrypted(defender, bytearray(move))

        # Defender processes the attack and responds
        response = byteArrayToList(receive_encrypted(defender))
        # send_encrypted(attacker, bytearray(response))

        # Switch roles
        attacker, defender = defender, attacker
        attacker_grid, defender_grid = defender_grid, attacker_grid

    except Exception as e:
        print(f"Error: {e}")
        break

player1_socket.close()
player2_socket.close()
serverSocket.close()
