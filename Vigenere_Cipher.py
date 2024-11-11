def encrypt_vigenere(plaintext, key):
    plaintext = plaintext.lower()
    key = key.lower()
    ciphertext = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(encrypted_char)
            key_index += 1
        else:
            ciphertext.append(char)
    
    return ''.join(ciphertext).upper()

def decrypt_vigenere(ciphertext, key):
    ciphertext = ciphertext.lower()
    key = key.lower()
    plaintext = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext.append(decrypted_char)
            key_index += 1
        else:
            plaintext.append(char)
    
    return ''.join(plaintext).lower()

print("***********This is Vignere Cipher!***********")
key = input("Enter the key: ")
plaintext = input("Enter the string to be encrypted: ")

# Encrypt the plaintext
ciphertext = encrypt_vigenere(plaintext, key)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext
decrypted_text = decrypt_vigenere(ciphertext, key)
print(f"Decrypted Text: {decrypted_text}")
