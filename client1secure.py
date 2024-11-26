import socket
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import struct

# Helper functions for AES encryption
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

import random
import math
# RSA Key Generation and Operations
def extendedGCD(a, b):
    coef_2, coef_1 = (1, 0), (0, 1)
    while b != 0:
        quotient = a // b
        a, b = b, a % b
        coef_2, coef_1 = coef_1, (coef_2[0] - quotient * coef_1[0], coef_2[1] - quotient * coef_1[1])
    return a, coef_2[0], coef_2[1]

def inverseMod(a, m):
    gcd, inv, _ = extendedGCD(a, m)
    if gcd != 1:
        raise Exception(f"Error, {a} does not admit an inverse mod {m}")
    return inv % m

def generateKeyPair(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    for _ in range(1000):
        e = random.randint(3, 65537)
        if math.gcd(e, phi_n) == 1:
            break
    else:
        raise Exception("Failed to generate a suitable e.")
    d = inverseMod(e, phi_n)
    return (n, e), (n, d)

def encryptWithPublicKey(msg, e, n):
    return pow(msg, e, n)

def decryptWithPrivateKey(ciphertext, d, n):
    return pow(ciphertext, d, n)

# Fixed p and q for simplicity
p = 5468586886433619073894411726580764173498770708709664207666335008910954157394117737047010310832685387467404417421582009414228902134582657991102753570623459
q = 6442675118318342480288941508523630505099561268793349471454944513843099853236531787541189244253590278169247240616311079998017162034233121434399387485428527

# Generate RSA key pair
public_key, private_key = generateKeyPair(p, q)
print("Generated Public Key:", public_key)

# Save private key locally
with open("private_key1.txt", "w") as f:
    f.write(str({private_key}))


# Server connection
host = '127.0.0.1'
port = 12001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

encryption_flag = client_socket.recv(1)
encryption_mode = encryption_flag[0] == 1  

if encryption_mode:
    # Send public key to the server
    client_socket.sendall(f"{public_key[0]} {public_key[1]}".encode())  # Send n and e as space-separated values
    # Receive the AES key from the server
    encrypted_aes_key = int(client_socket.recv(1024).decode())
    aes_key = decryptWithPrivateKey(encrypted_aes_key, private_key[1], private_key[0])
    aes_key = aes_key.to_bytes(16, "big")  # Convert to bytes
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
            
            if result[0] == 1:
                print("HIT!")
                print("Opponent's Grid")                
                displayGuessMadeMatrix("hit", guessGrid, x, y)
            else:
                print("MISS!")
                print("Opponent's Grid")                
                displayGuessMadeMatrix("miss", guessGrid, x, y)
                print("Your Grid:")
                displayGrid(myGrid)
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
