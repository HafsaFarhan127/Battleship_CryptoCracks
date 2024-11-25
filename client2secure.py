import socket

from Cryptodome.Cipher import AES

def pad_data(data, block_size):
    pad_len = block_size - len(data) % block_size
    padding = bytes([pad_len] * pad_len)
    return data + padding

def unpad_data(data):
    pad_len = data[-1]
    return data[:-pad_len]

def aes_encrypt(data, key, mode="ECB"):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad_data(data, 16))

def aes_decrypt(ciphertext, key, mode="ECB"):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad_data(cipher.decrypt(ciphertext))

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12001))

# Determine encryption mode
encryption_indicator = client_socket.recv(1024)
encryption_mode = encryption_indicator == b"ENCRYPTED"
aes_key = client_socket.recv(1024) if encryption_mode else None

def send_data(data):
    if encryption_mode:
        client_socket.sendall(aes_encrypt(data, aes_key, mode="CBC"))
    else:
        client_socket.sendall(data)

def receive_data(buffer_size=1024):
    data = client_socket.recv(buffer_size)
    if encryption_mode:
        return aes_decrypt(data, aes_key, mode="CBC")
    return data

# Receive initial grid
grid = receive_data()
print("Game start!")

while True:
    try:
        turn_signal = receive_data()
        if turn_signal == b"END":
            print("Game over!")
            break

        if turn_signal == b"1":
            x, y = map(int, input("Enter coordinates (x, y): ").split(","))
            send_data(bytearray([x, y]))
            result = receive_data()
            print("Result:", result)
        else:
            print("Waiting for opponent's move...")
            move = receive_data()
            print("Opponent attacked:", move)

    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
