from Cryptodome.Cipher import DES, DES3, AES, Blowfish
from Cryptodome.Random import get_random_bytes
import struct

def pad_data(data, block_size):
    """Pads data to be a multiple of the block size."""
    pad_len = block_size - len(data) % block_size
    padding = bytes([pad_len] * pad_len)
    return data + padding

def unpad_data(data):
    """Removes padding from data."""
    pad_len = data[-1]
    return data[:-pad_len]

def list_to_bytes(data_list):
    """Converts a list of integers to a byte array."""
    byte_data = b''
    for num in data_list:
        num_bytes = struct.pack('>I', num)
        byte_data += num_bytes
    return byte_data

def bytes_to_list(byte_data):
    """Converts byte array back to a list of integers."""
    return [struct.unpack('>I', byte_data[i:i+4])[0] for i in range(0, len(byte_data), 4)]

# Encryption and decryption for DES
def des_encrypt(data, key, mode="ECB"):
    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    padded_data = pad_data(data, 8)
    ciphertext = cipher.encrypt(padded_data)

    if mode == "CBC":
        return iv + ciphertext
    return ciphertext

def des_decrypt(ciphertext, key, mode="ECB"):
    if mode == "CBC":
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    elif mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    decrypted_data = cipher.decrypt(ciphertext)
    return unpad_data(decrypted_data)

# Encryption and decryption for 3DES
def triple_des_encrypt(data, key, mode="ECB"):
    if mode == "ECB":
        cipher = DES3.new(key, DES3.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    padded_data = pad_data(data, 8)
    ciphertext = cipher.encrypt(padded_data)

    if mode == "CBC":
        return iv + ciphertext
    return ciphertext

def triple_des_decrypt(ciphertext, key, mode="ECB"):
    if mode == "CBC":
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    elif mode == "ECB":
        cipher = DES3.new(key, DES3.MODE_ECB)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    decrypted_data = cipher.decrypt(ciphertext)
    return unpad_data(decrypted_data)

# Encryption and decryption for AES
def aes_encrypt(data, key, mode="ECB"):
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    padded_data = pad_data(data, 16)
    ciphertext = cipher.encrypt(padded_data)

    if mode == "CBC":
        return iv + ciphertext
    return ciphertext

def aes_decrypt(ciphertext, key, mode="ECB"):
    if mode == "CBC":
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    elif mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    decrypted_data = cipher.decrypt(ciphertext)
    return unpad_data(decrypted_data)

# Encryption and decryption for Blowfish
def blowfish_encrypt(data, key, mode="ECB"):
    if mode == "ECB":
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=iv)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    padded_data = pad_data(data, Blowfish.block_size)
    ciphertext = cipher.encrypt(padded_data)

    if mode == "CBC":
        return iv + ciphertext
    return ciphertext

def blowfish_decrypt(ciphertext, key, mode="ECB"):
    if mode == "CBC":
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=iv)
    elif mode == "ECB":
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    else:
        raise ValueError("Unsupported mode. Choose 'ECB' or 'CBC'.")

    decrypted_data = cipher.decrypt(ciphertext)
    return unpad_data(decrypted_data)

# Example usage
data = [4,3]  # List of integers
byte_data = list_to_bytes(data)

# DES
key_des = get_random_bytes(8)
ciphertext_des = des_encrypt(byte_data, key_des, mode="CBC")
decrypted_des = des_decrypt(ciphertext_des, key_des, mode="CBC")
print("DES Encrypted:", ciphertext_des)
print("Original:", data, "| Decrypted DES:", bytes_to_list(decrypted_des))

# 3DES
key_3des = get_random_bytes(24)
ciphertext_3des = triple_des_encrypt(byte_data, key_3des, mode="CBC")
decrypted_3des = triple_des_decrypt(ciphertext_3des, key_3des, mode="CBC")
print("3DES Encrypted:", ciphertext_3des)
print("Original:", data, "| Decrypted 3DES:", bytes_to_list(decrypted_3des))

# AES
key_aes = get_random_bytes(32)
ciphertext_aes = aes_encrypt(byte_data, key_aes, mode="CBC")
decrypted_aes = aes_decrypt(ciphertext_aes, key_aes, mode="CBC")
print("AES Encrypted:", ciphertext_aes)
print("Original:", data, "| Decrypted AES:", bytes_to_list(decrypted_aes))

# Blowfish
key_blowfish = get_random_bytes(16)
ciphertext_blowfish = blowfish_encrypt(byte_data, key_blowfish, mode="CBC")
decrypted_blowfish = blowfish_decrypt(ciphertext_blowfish, key_blowfish, mode="CBC")
print("Blowfish Encrypted:", ciphertext_blowfish)
print("Original:", data, "| Decrypted Blowfish:", bytes_to_list(decrypted_blowfish))

def rc4_key_schedule(key):
    """Initialize the key-scheduling algorithm (KSA) for RC4."""
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_pseudo_random_generation_algorithm(S, data_length):
    """Generate a keystream using the pseudo-random generation algorithm (PRGA) for RC4."""
    i = j = 0
    keystream = []
    for _ in range(data_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)
    return keystream

def rc4_encrypt(data_list, key):
    """Encrypts or decrypts a list of integers using RC4."""
    # Convert key to byte array and set up key schedule
    key_bytes = bytes(key, 'utf-8')
    S = rc4_key_schedule(key_bytes)

    # Convert list of integers to byte array
    byte_data = b''.join(num.to_bytes(4, byteorder='big') for num in data_list)

    # Generate keystream and apply RC4 encryption
    keystream = rc4_pseudo_random_generation_algorithm(S, len(byte_data))
    encrypted_data = bytes([b ^ k for b, k in zip(byte_data, keystream)])

    return encrypted_data

def rc4_decrypt(encrypted_data, key):
    """Decrypts a byte array back to a list of integers using RC4."""
    # RC4 decryption is identical to encryption, as it is a stream cipher
    decrypted_data = rc4_encrypt(bytes_to_list(encrypted_data), key)
    return bytes_to_list(decrypted_data)

def bytes_to_list(byte_data):
    """Converts byte array back to a list of integers without struct."""
    return [int.from_bytes(byte_data[i:i+4], 'big') for i in range(0, len(byte_data), 4)]

# Example usage
data_list = [10, 20, 30, 40]  # Example list of integers
key = "mysecretkey"  # Key for RC4 as a string

# Encrypt
ciphertext = rc4_encrypt(data_list, key)
print("Ciphertext:", ciphertext)

# Decrypt
decrypted_data = rc4_decrypt(ciphertext, key)
print("Original:", data_list, "| Decrypted:", decrypted_data)

import random

def createGrid(size):
    grid = []
    for _ in range(size):
        row = ['.' for _ in range(size)]
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
            if grid[row][col + i] != '.':
                return False
    elif direction == 'V':
        if row + shipSize > len(grid):
            return False
        for i in range(shipSize):
            if grid[row + i][col] != '.':
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

def main():
    gridSize = 10
    global grid
    grid = createGrid(gridSize)
    ships = [
        (5, 'A'),  # Ship of size 5
        (4, 'B'),  # Ship of size 4
        (3, 'C'),  # Ship of size 3
        (3, 'D'),  # Ship of size 3
        (2, 'E')   # Ship of size 2
    ]

    for shipSize, shipSymbol in ships:
        placeShip(grid, shipSize, shipSymbol)

    printGrid(grid)
    printGrid(grid[1][2])




if __name__ == "__main__":
    main()