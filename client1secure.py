import socket
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

def byteArrayToGrid(byteArray, size):
    return [list(byteArray[i:i + size]) for i in range(0, len(byteArray), size)]

def byteArrayToList(byteArray):
    return [int(byte) for byte in byteArray]

def listToByteArray(data):
    return bytearray(data)

def displayGrid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def displayGuessMadeMatrix(SERVER_take_shotMsg, grid, oldGuess_X, oldGuess_Y):
    if SERVER_take_shotMsg == 'hit':
        grid[oldGuess_X][oldGuess_Y] = 'x'
    elif SERVER_take_shotMsg == 'miss':
        grid[oldGuess_X][oldGuess_Y] = 'm'

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

encryption_flag = client_socket.recv(1)
encryption_mode = encryption_flag[0] == 1  


# Receive the AES key from the server
aes_key = client_socket.recv(16) if encryption_mode else None

def send_encrypted(data):
    if encryption_mode:
        encrypted_data = aes_encrypt(data, aes_key)
        client_socket.sendall(struct.pack("!I", len(encrypted_data)) + encrypted_data)
    else:
        client_socket.sendall(data)

def receive_encrypted(buffer_size=1024):
    if encryption_mode:
        data_length = struct.unpack("!I", client_socket.recv(4))[0]
        data = client_socket.recv(data_length)
        return aes_decrypt(data, aes_key)
    return client_socket.recv(buffer_size)

# Receive initial grid
decrypted_data = receive_encrypted()
myGrid = byteArrayToGrid(decrypted_data, 10)
guessGrid = [[0 for _ in range(10)] for _ in range(10)]

print("Your Grid:")
displayGrid(myGrid)

while True:
    try:
        server_message = byteArrayToList(receive_encrypted())
        if 2 in server_message:
            print("Game over! You lose.")
            break
        if 1 in server_message:
            while True:
                try:
                    x, y = map(int, input("Enter coordinates to attack (x, y): ").split(","))
                    if 0 <= x < 10 and 0 <= y < 10:
                        break
                    else:
                        print("Coordinates out of bounds. Enter values between 0 and 9.")
                except ValueError:
                    print("Invalid input format. Enter two integers separated by a comma.")
            send_encrypted(bytearray([x, y]))
            result = byteArrayToList(receive_encrypted())
            if result[1] == 1:
                print("You sunk the ship! You win!")
                break
            print(result)
            if result[0] == 1:
                print()
                print("HIT!")
                print()                
                displayGuessMadeMatrix("hit", guessGrid, x, y)
            else:
                print()
                print("MISS!")
                print()                
                displayGuessMadeMatrix("miss", guessGrid, x, y)
        elif 0 in server_message:
            print("Waiting for opponent's move...")
            move = byteArrayToList(receive_encrypted())
            x, y = move
            result = "HIT" if myGrid[x][y] != 0 else "MISS"
            myGrid[x][y] = 0
            sink = 1 if sum(sum(row) for row in myGrid) == 0 else 0
            send_encrypted(bytearray([1 if result == "HIT" else 0, sink]))
            if sink == 1:
                print("All ships sunk! You lose.")
                break
    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
