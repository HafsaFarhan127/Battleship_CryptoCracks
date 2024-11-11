def encrypt_autokey(plaintext, key):
    plaintext = plaintext.lower()  # Convert plaintext to lowercase
    key = key.lower()  # Convert key to lowercase
    ciphertext = []
    key_extended = key + plaintext  # Extend the key with the plaintext
    
    key_index = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():  # Encrypt only letters
            shift = ord(key_extended[key_index]) - ord('a')
            encrypted_char = chr(((ord(plaintext[i]) - ord('a') + shift) % 26) + ord('a'))
            ciphertext.append(encrypted_char)
            key_index += 1
        else:
            ciphertext.append(plaintext[i])  # Append non-alphabet characters as is
    
    return ''.join(ciphertext).upper()  # Return ciphertext in uppercase

def decrypt_autokey(ciphertext, key):
    ciphertext = ciphertext.lower()  # Convert ciphertext to lowercase
    key = key.lower()  # Convert key to lowercase
    plaintext = []
    key_index = 0
    
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():  # Decrypt only letters
            shift = ord(key[key_index]) - ord('a')
            decrypted_char = chr(((ord(ciphertext[i]) - ord('a') - shift) % 26) + ord('a'))
            plaintext.append(decrypted_char)
            key += decrypted_char  # Update key with the decrypted character
            key_index += 1
        else:
            plaintext.append(ciphertext[i])  # Append non-alphabet characters as is
    
    return ''.join(plaintext).lower()  # Return plaintext in lowercase

print("***********This is Autokey Cipher!***********")
key = input("Enter the key: ")
plaintext = input("Enter the string to be encrypted: ")

# Encrypt the plaintext
ciphertext = encrypt_autokey(plaintext, key)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext
decrypted_text = decrypt_autokey(ciphertext, key)
print(f"Decrypted Text: {decrypted_text}")
