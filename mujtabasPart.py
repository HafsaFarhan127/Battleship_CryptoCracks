import random

# Define the homophonic substitution mappings
homophonic_map = {
    'A': ['11', '12', '13'],
    'B': ['21', '22'],
    'C': ['31', '32', '33'],
    'D': ['41', '42'],
    'E': ['51', '52', '53', '54'],
    'F': ['61', '62'],
    'G': ['71', '72'],
    'H': ['81', '82', '83'],
    'I': ['91', '92', '93'],
    'J': ['14'],
    'K': ['24'],
    'L': ['34'],
    'M': ['44'],
    'N': ['94', '95'],
    'O': ['25', '26'],
    'P': ['35'],
    'Q': ['45'],
    'R': ['55', '56'],
    'S': ['65', '66'],
    'T': ['75', '76', '77'],
    'U': ['85', '86'],
    'V': ['96'],
    'W': ['16'],
    'X': ['36'],
    'Y': ['46'],
    'Z': ['17']
}

# Reverse the homophonic map to help with decryption
reverse_homophonic_map = {}
for key, values in homophonic_map.items():
    for value in values:
        reverse_homophonic_map[value] = key

def encrypt_homophonic(plaintext):
    """Encrypt the plaintext using the homophonic cipher."""
    ciphertext = []
    for char in plaintext.upper():
        if char in homophonic_map:
            # Randomly choose one of the possible encodings
            ciphertext.append(random.choice(homophonic_map[char]))
        else:
            # Keep non-alphabetic characters as is
            ciphertext.append(char)
    return ' '.join(ciphertext)

def decrypt_homophonic(ciphertext):
    """Decrypt the ciphertext using the homophonic cipher."""
    decrypted_text = []
    # Split the ciphertext by spaces to get each code
    codes = ciphertext.split()
    for code in codes:
        if code in reverse_homophonic_map:
            decrypted_text.append(reverse_homophonic_map[code])
        else:
            # Keep characters that are not part of the cipher as is
            decrypted_text.append(code)
    return ''.join(decrypted_text)