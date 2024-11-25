#pip install pycryptodome
from Cryptodome.Cipher import AES
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



key = get_random_bytes(16)  # AES requires a 16-byte key for 128-bit encryption
print(bytes([0,1]))
ciphertext = aes_encrypt(bytes([0,1]), None, mode="CBC")
print("Ciphertext:", ciphertext)