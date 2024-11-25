import random as rand

def caesar():    
    def rotate_numbers(numbers, shift):
        length = len(numbers)
        if shift > length:
            shift = shift % length
        return numbers[shift:] + numbers[:shift]

    # Encryption
    def caesarEncryptNumbers(plainNumbers, numbers, shift):
        shifted_numbers = rotate_numbers(numbers, shift)
        map_table = {numbers[i]: shifted_numbers[i] for i in range(len(numbers))}
        return [map_table[num] for num in plainNumbers]

    # Decryption
    def caesarDecryptNumbers(cipherNumbers, numbers, shift):
        shifted_numbers = rotate_numbers(numbers, shift)
        reverse_map_table = {shifted_numbers[i]: numbers[i] for i in range(len(numbers))}
        return [reverse_map_table[num] for num in cipherNumbers]

    # Example usage
    plainNumbers = [12, 45, 78, 23, 56]
    shift = 3  # Example shift value
    NUMBERS = list(range(0, 10**(len(str(max(plainNumbers))))))  # Define the range of numbers
    print("***CAESAR CIPHER***")
    print("The shift is: ",shift)
    # Encrypt the numbers
    cipherNumbers = caesarEncryptNumbers(plainNumbers, NUMBERS, shift)
    print("Encrypted Numbers:", cipherNumbers)

    # Decrypt the numbers
    decryptedNumbers = caesarDecryptNumbers(cipherNumbers, NUMBERS, shift)
    print("Decrypted Numbers:", decryptedNumbers)

def mono():
    # Function to generate a permutation of a list of numbers
    def permute_numbers(numbers):
        cipherNumbers = numbers[:]
        rand.shuffle(cipherNumbers)
        return cipherNumbers

    # Mono-substitution encryption for numbers
    def monoSubNumbers(plainNumbers, numbers):
        key = permute_numbers(numbers)
        map = {numbers[i]: key[i] for i in range(len(numbers))}
        print("The key is:", key)
        return [map[num] for num in plainNumbers],key

    # Mono-substitution decryption for numbers
    def monoUnSubNumbers(cipherNumbers, numbers, key):
        reverse_map = {key[i]: numbers[i] for i in range(len(numbers))}
        return [reverse_map[num] for num in cipherNumbers]

    # Example usage
    plainNumbers = [12, 45, 78, 23, 56]
    NUMBERS = list(range(0, 10**(len(str(max(plainNumbers))))))  # Define the range of numbers
    print("***MONOSUBSTITUTION CIPHER***")
    # Encrypt the numbers
    cipherNumbers,key = monoSubNumbers(plainNumbers, NUMBERS)
    print("Encrypted Numbers:", cipherNumbers)

    # Decrypt the numbers
    decryptedNumbers = monoUnSubNumbers(cipherNumbers, NUMBERS, key)
    print("Decrypted Numbers:", decryptedNumbers)

def affine():    
    # GCD Function
    def myGCDRec(a, b): 
        if b == 0:
            return abs(a)
        else:
            return myGCDRec(b, a % b)

    # Extended GCD Function
    def extendedGCD(a, b):
        s1, t1, s2, t2 = 1, 0, 0, 1
        while a % b != 0:
            r = a % b
            s3 = s1 - (s2 * (a // b))
            t3 = t1 - (t2 * (a // b))
            a, b = b, r
            s1, t1, s2, t2 = s2, t2, s3, t3
        return s3, t3

    # Modular Inverse Function
    def inverseMod(a, m):
        if myGCDRec(a, m) != 1:
            raise ValueError("Inverse does not exist")
        else:
            num = extendedGCD(a, m)
            return num[0]%m

    # Affine Cipher Encryption for Numbers
    def affineCipherEncryptNumbers(plainNumbers, k, a, modulus):
        cipherNumbers = []
        for num in plainNumbers:
            cipherNumbers.append((num * k + a) % modulus)
        return cipherNumbers

    # Affine Cipher Decryption for Numbers
    def affineCipherDecryptNumbers(cipherNumbers, k, a, modulus):
        inverseK = inverseMod(k, modulus)
        if inverseK < 0:
            inverseK += modulus  # Ensure positive modular inverse
        plainNumbers = []
        for num in cipherNumbers:
            decrypted_num = (inverseK * (num - a)) % modulus
            plainNumbers.append(decrypted_num)
        return plainNumbers
    print("***AFFINE CIPHER***")
    # Example usage
    plainNumbers = [12, 45, 78, 23, 56]  # Input numbers
    modulus = (max(plainNumbers)+1) # Define range dynamically
    # Choose m and a
    m = 5  # Key value
    a = 2  # Offset value
    print("The Key is: (",m,",",a,")")
    # Encrypt the numbers
    cipherNumbers = affineCipherEncryptNumbers(plainNumbers, m, a, modulus)
    print("Encrypted Numbers:", cipherNumbers)

    # Decrypt the numbers
    decryptedNumbers = affineCipherDecryptNumbers(cipherNumbers, m, a, modulus)
    print("Decrypted Numbers:", decryptedNumbers)

def hill():
    # Determinant of a 2x2 matrix
    def det(a):
        if len(a) != 2 or len(a[0]) != 2 or len(a[1]) != 2:
            return False
        determinant = (a[0][0] * a[1][1]) - (a[0][1] * a[1][0])
        return determinant

    # Extended GCD for modular inverses
    def Hill_extendedGCD(a, b):
        if b == 0:
            return a, 1, 0
        gcd, s1, t1 = Hill_extendedGCD(b, a % b)
        s = t1
        t = s1 - (a // b) * t1
        return gcd, s, t

    # Inverse of a 2x2 matrix modulo m
    def Hill_inverseMatrixMod(a, m):
        if len(a) != 2 or len(a[0]) != 2 or len(a[1]) != 2:
            return "The key must be a 2x2 matrix"
        
        determinant = det(a)
        gcd, det_inverse, _ = Hill_extendedGCD(determinant, m)
        if gcd != 1:
            return "The matrix does not admit an inverse."
        det_inverse = det_inverse % m
        
        adjoint = [[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]]
        inverse = [[(det_inverse * adjoint[i][j]) % m for j in range(2)] for i in range(2)]
        return inverse

    # Hill Cipher Encryption for Numbers
    def hillCipherEncryptNumbers(numbers, k, modulus):
        determinant = det(k)
        if determinant == False:
            return "The input must be a 2x2 matrix"

        gcd, _, _ = Hill_extendedGCD(determinant, modulus)
        if gcd != 1:
            return "The key matrix does not admit an inverse."

        if len(numbers) % 2 != 0:
            numbers.append(0)  # Padding with 0 for odd-length numbers

        encrypted_numbers = []
        for i in range(0, len(numbers), 2):
            x1 = numbers[i]
            x2 = numbers[i + 1]

            y1 = (k[0][0] * x1 + k[0][1] * x2) % modulus
            y2 = (k[1][0] * x1 + k[1][1] * x2) % modulus
            encrypted_numbers.extend([y1, y2])

        return encrypted_numbers

    # Hill Cipher Decryption for Numbers
    def hillCipherDecryptNumbers(numbers, k, modulus):
        determinant = det(k)
        if determinant == False:
            return "The input must be a 2x2 matrix"

        inverse_k = Hill_inverseMatrixMod(k, modulus)
        if isinstance(inverse_k, str):  # If the inverse is invalid
            return inverse_k

        decrypted_numbers = []
        for i in range(0, len(numbers), 2):
            y1 = numbers[i]
            y2 = numbers[i + 1]

            x1 = (inverse_k[0][0] * y1 + inverse_k[0][1] * y2) % modulus
            x2 = (inverse_k[1][0] * y1 + inverse_k[1][1] * y2) % modulus
            decrypted_numbers.extend([x1, x2])

        if decrypted_numbers[-1] == 0:
            decrypted_numbers = decrypted_numbers[:-1]
        return decrypted_numbers

    # Example Usage
    numbers = [12, 45, 78, 23, 56]  # Plain numbers
    k = [[1, 2], [4, 3]]  # Key matrix
    
    modulus = (max(numbers)+1)  # Modulus for encryption/decryption
    print("***HILL CIPHER***")
    print("The Key Matrix is:")
    [print(k[i],"\n") for i in range(len(k))]
    # Encrypt
    encrypted_numbers = hillCipherEncryptNumbers(numbers, k, modulus)
    print("Encrypted Numbers:", encrypted_numbers)

    # Decrypt
    decrypted_numbers = hillCipherDecryptNumbers(encrypted_numbers, k, modulus)
    print("Decrypted Numbers:", decrypted_numbers)
    
def playfair():
    def number_to_char(num):
        """Convert a number (0-25) to a character (A-Z)."""
        return chr(num % 26 + 65)

    def char_to_number(char):
        """Convert a character (A-Z) to a number (0-25)."""
        return ord(char) - 65

    def generate_playfair_matrix(keyword):
        """Generate a 5x5 Playfair matrix from the keyword."""
        keyword = keyword.upper().replace("J", "I")
        seen = set()
        matrix = []

        for char in keyword:
            if char not in seen and char.isalpha():
                seen.add(char)
                matrix.append(char)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in seen:
                matrix.append(char)

        playfair_matrix = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(matrix[i * 5 + j])
            playfair_matrix.append(row)
        # print("Playfair Matrix: \n",playfair_matrix)
        return playfair_matrix

    def find_position(matrix, char):
        """Find the position of a character in the Playfair matrix."""
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j
        return None

    def playfair_encrypt_numbers(numbers, keyword):
        """Encrypt a list of numbers using the Playfair cipher."""
        matrix = generate_playfair_matrix(keyword)
        offsets=[]
        # Map numbers to characters
        chars=""
        for num in numbers:
            char = number_to_char(num)
            offsets.append(num-char_to_number(char))
            chars+= ''.join(char)
        
        # Ensure even number of characters for pairing
        if len(chars) % 2 != 0:
            chars += number_to_char(23)  # Add a filler character ('X' -> 23)

        encrypted_chars = ""
        i = 0
        while i < len(chars):
            pair = chars[i] + chars[i + 1]
            i += 2

            row1, col1 = find_position(matrix, pair[0])
            row2, col2 = find_position(matrix, pair[1])

            if row1 == row2:  # Same row
                encrypted_chars += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_chars += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle swap
                encrypted_chars += matrix[row1][col2] + matrix[row2][col1]

        # Convert encrypted characters back to numbers
        encrypted_numbers = [char_to_number(c) for c in encrypted_chars]
        return encrypted_numbers,offsets

    def playfair_decrypt_numbers(encrypted_numbers, keyword,offsets):
        """Decrypt a list of numbers using the Playfair cipher."""
        matrix = generate_playfair_matrix(keyword)

        # Map numbers to characters
        chars = ''.join(number_to_char(num) for num in encrypted_numbers)

        decrypted_chars = ""
        i = 0
        while i < len(chars):
            pair = chars[i] + chars[i + 1]
            i += 2

            row1, col1 = find_position(matrix, pair[0])
            row2, col2 = find_position(matrix, pair[1])

            if row1 == row2:  # Same row
                decrypted_chars += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                decrypted_chars += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle swap
                decrypted_chars += matrix[row1][col2] + matrix[row2][col1]

        # Convert decrypted characters back to numbers
        decrypted_numbers = [((char_to_number(c)//26)*26+char_to_number(c)) for c in decrypted_chars]
        
        # Remove filler if it was added
        if len(decrypted_numbers) > len(encrypted_numbers) / 2:
            decrypted_numbers.pop()
        for i,d in enumerate(decrypted_numbers):
            decrypted_numbers[i]=d+offsets[i]

        return decrypted_numbers

    # Test the corrected functions
    numbers = [12, 45, 78, 23, 56]  # Input numbers
    keyword = "palmerstone"
    print("***PLAYFAIR CIPHER***")
    print("The key is: ",keyword)
    # Encrypt
    encrypted_numbers,offsets = playfair_encrypt_numbers(numbers, keyword)
    print("Encrypted Numbers:", encrypted_numbers)

    # Decrypt
    decrypted_numbers = playfair_decrypt_numbers(encrypted_numbers, keyword,offsets)
    print("Decrypted Numbers:", decrypted_numbers)

def column():
    def reOrderKey(t):
        asciiConv = [ord(i) for i in t]
        ordered = sorted(asciiConv)
        return [ordered.index(i) for i in asciiConv]

    def columnarTranspositionNumbers(numbers, k):
        keyOrder = reOrderKey(k)
        keyLength = len(k)
        padding_value = -1  # Use -1 as the padding value for numbers
        remainder = len(numbers) % keyLength
        
        # Add padding if necessary
        if remainder != 0:
            padding_needed = keyLength - remainder
            numbers += [padding_value] * padding_needed

        # Split numbers into columns based on the key length
        l = [numbers[i::keyLength] for i in range(keyLength)]

        # Create a dictionary with the order of columns
        dictionary = {}
        for index, key in enumerate(keyOrder):
            dictionary[key] = l[index]

        # Build the cipher by reading columns in sorted order of the key
        c = []
        for key in sorted(dictionary):
            c.extend(dictionary[key])

        return c

    def decryptColumnarTranspositionNumbers(c, k):
        keyOrder = reOrderKey(k)
        keyLength = len(k)
        rows = len(c) // keyLength

        # Reverse the ordering of columns
        dictionary = {}
        for i, key in enumerate(sorted(keyOrder)):
            dictionary[key] = c[i * rows:(i + 1) * rows]

        # Reconstruct the plaintext from the columns
        plaintext = []
        for i in range(rows):
            for key in keyOrder:
                plaintext.append(dictionary[key][i])

        # Remove padding values
        plaintext = [num for num in plaintext if num != -1]
        return plaintext

    # Test - Columnar Transposition for Numbers
    print("***COLUMNAR TRANSPOSITION CIPHER***")
    numbers = [12, 45, 78, 23, 56]
    key = "cipher"
    print("The key is: ",key)
    # Encrypt the numbers
    cipher = columnarTranspositionNumbers(numbers, key)
    print("Encrypted Numbers:", cipher)

    # Decrypt the numbers
    plaintext = decryptColumnarTranspositionNumbers(cipher, key)
    print("Decrypted Numbers:", plaintext)

def vigenere():
    def create_vigenere_table():
        """Create a Vigenère table for numbers 0-25."""
        table = []
        for i in range(26):
            row = [(j + i) % 26 for j in range(26)]
            table.append(row)
        return table

    def encrypt_vigenere_numbers_with_table(numbers, key):
        """Encrypt a list of numbers using the Vigenère cipher and the generated table."""
        table = create_vigenere_table()
        encrypted = []
        key_values = [ALPH.index(k.upper()) for k in key]  # Convert key to numeric values
        key_length = len(key_values)
        offsets = []  # To store offsets for recovering original values during decryption

        for i, num in enumerate(numbers):
            num_mod = num % 26  # Convert the number to 0-25 range
            key_val = key_values[i%key_length]  # Cycle through key values
            encrypted_val = table[num_mod][key_val]  # Get the intersection value from the table
            encrypted.append(encrypted_val)
            offsets.append(num - num_mod)  # Store the offset used

        return encrypted, offsets

    def decrypt_vigenere_numbers_with_table(encrypted, key, offsets):
        """Decrypt a list of numbers using the Vigenère cipher and the generated table."""
        table = create_vigenere_table()
        decrypted = []
        key_values = [ALPH.index(k.upper()) for k in key]  # Convert key to numeric values
        key_length = len(key_values)

        for i, enc_val in enumerate(encrypted):
            key_val = key_values[i%key_length]  # Cycle through key values
            # Find the row corresponding to the key_val and locate enc_val's position
            row = table[key_val]
            num_mod = row.index(enc_val)  # Reverse lookup in the table
            original_val = num_mod + offsets[i]  # Add back the offset to get the original value
            decrypted.append(original_val)

        return decrypted

    # Test the implementation
    ALPH=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numbers = [12, 45, 78, 23, 56]  # List of numbers to encrypt
    key = "ciph"  # Encryption key
    print("***VIGENERE CIPHER***")
    print("The key is: ",key)
    # Encrypt the numbers
    encrypted, offsets = encrypt_vigenere_numbers_with_table(numbers, key)
    print(f"Encrypted Numbers: {encrypted}")

    # Decrypt the numbers
    decrypted = decrypt_vigenere_numbers_with_table(encrypted, key, offsets)
    print(f"Decrypted Numbers: {decrypted}")

def auto():
    def create_autokey_table():
        """Create an Autokey table for numbers 0-25."""
        table = []
        for i in range(26):
            row = [(j + i) % 26 for j in range(26)]
            table.append(row)
        return table

    def encrypt_autokey_numbers_with_table(numbers, key):
        """Encrypt a list of numbers using the Autokey cipher and the generated table."""
        table = create_autokey_table()
        encrypted = []
        offsets = []

        # Start the key sequence with the initial key
        key_values = [ALPH.index(k.upper()) for k in key]

        for i, num in enumerate(numbers):
            num_mod = num % 26  # Convert the number to 0-25 range

            if i < len(key_values):
                key_val = key_values[i]  # Use the key initially
            else:
                key_val = numbers[i - len(key_values)] % 26  # Use previous plaintext values as key

            encrypted_val = table[num_mod][key_val]
            encrypted.append(encrypted_val)
            offsets.append(num - num_mod)  # Store the offset used

        return encrypted, offsets

    def decrypt_autokey_numbers_with_table(encrypted, key, offsets):
        """Decrypt a list of numbers using the Autokey cipher and the generated table."""
        table = create_autokey_table()
        decrypted = []

        # Start the key sequence with the initial key
        key_values = [ALPH.index(k.upper()) for k in key]

        for i, enc_val in enumerate(encrypted):
            if i < len(key_values):
                key_val = key_values[i]  # Use the key initially
            else:
                key_val = decrypted[i - len(key_values)] % 26  # Use previously decrypted values as key

            # Find the row corresponding to the key_val and locate enc_val's position
            row = table[key_val]
            num_mod = row.index(enc_val)  # Reverse lookup in the table
            original_val = num_mod + offsets[i]  # Add back the offset to get the original value
            decrypted.append(original_val)

        return decrypted

    # Test the implementation
    ALPH = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = [12, 45, 78, 23, 56]  # List of numbers to encrypt
    key = "ciph"  # Encryption key
    print("***AUTOKEY CIPHER***")
    print("The key is: ",key)
    # Encrypt the numbers
    encrypted, offsets = encrypt_autokey_numbers_with_table(numbers, key)
    print(f"Encrypted Numbers: {encrypted}")

    # Decrypt the numbers
    decrypted = decrypt_autokey_numbers_with_table(encrypted, key, offsets)
    print(f"Decrypted Numbers: {decrypted}")

def homo():
    # Define the homophonic substitution mappings
    homophonic_map = {
        0: [11, 12, 13],
        1: [21, 22],
        2: [31, 32, 33],
        3: [41, 42],
        4: [51, 52, 53, 54],
        5: [61, 62],
        6: [71, 72],
        7: [81, 82, 83],
        8: [91, 92, 93],
        9: [14],
        10: [24],
        11: [34],
        12: [44],
        13: [94, 95],
        14: [25, 26],
        15: [35],
        16: [45],
        17: [55, 56],
        18: [65, 66],
        19: [75, 76, 77],
        20: [85, 86],
        21: [96],
        22: [16],
        23: [36],
        24: [46],
        25: [17]
    }

    # Reverse the homophonic map to help with decryption
    reverse_homophonic_map = {}
    for key, values in homophonic_map.items():
        for value in values:
            reverse_homophonic_map[value] = key

    def encrypt_homophonic(numbers):
        """Encrypt the plaintext using the homophonic cipher."""
        enc = []
        offsets = []
        for num in numbers:
            num_mod = num % 26  # Convert the number to 0-25 range
            # Randomly choose one of the possible encodings
            enc.append(rand.choice(homophonic_map[num_mod]))
            offsets.append(num - num_mod)  # Store the offset used
        return enc,offsets

    def decrypt_homophonic(enc,offsets):
        """Decrypt the ciphertext using the homophonic cipher."""
        dec = []
        # Split the ciphertext by spaces to get each code
        for i,code in enumerate(enc):
            num = code # Add back the offset to get the original value
            original= reverse_homophonic_map[num]
            dec.append(original+offsets[i])
        return dec
                                    
    numbers = [12,45,78,23,56]
    enc,offsets = encrypt_homophonic(numbers)
    dec = decrypt_homophonic(enc,offsets)
    print("***HOMOPHONIC CIPHER***")
    print("Encrypted Numbers: ", enc)
    print("Decrypted Numbers: ", dec)
    
def rail():
    def encrypt_rail_fence(num, num_rails):
        # Create a matrix to store the rail pattern
        rail_matrix = [['\n' for _ in range(len(num))] for _ in range(num_rails)]

        # Fill the rail matrix with characters in a zigzag pattern
        direction_down = False
        row, col = 0, 0
        
        for char in num:
            # Put the character in the correct row
            rail_matrix[row][col] = char 
            col += 1
            
            # Change direction when reaching the top or bottom rail
            if row == 0 or row == num_rails - 1:
                direction_down = not direction_down
                
            # Move to the next row in the current direction
            row += 1 if direction_down else -1
        
        # Read the characters row-by-row to form the encrypted text
        enc = []
        for i in range(num_rails):
            for j in range(len(num)):
                if rail_matrix[i][j] != '\n':
                    enc.append(rail_matrix[i][j])
        
        return enc

    def decrypt_rail_fence(enc, num_rails):
        # Create a matrix to mark the zigzag pattern
        rail_matrix = [['\n' for _ in range(len(enc))] for _ in range(num_rails)]
        
        # Mark the positions to place characters in the zigzag pattern
        direction_down = None
        row, col = 0, 0
        
        for i in range(len(enc)):
            # Mark the position with '*'
            rail_matrix[row][col] = '*'
            col += 1
            
            # Change direction when reaching the top or bottom rail
            if row == 0:
                direction_down = True
            elif row == num_rails - 1:
                direction_down = False
                
            # Move to the next row in the current direction
            row += 1 if direction_down else -1
        
        # Place the characters in the marked positions
        index = 0
        for i in range(num_rails):
            for j in range(len(enc)):
                if rail_matrix[i][j] == '*' and index < len(enc):
                    rail_matrix[i][j] = enc[index]
                    index += 1
        
        # Read the matrix in a zigzag pattern to decrypt the text
        decrypted_text = []
        row, col = 0, 0
        for i in range(len(enc)):
            # Append the character to the decrypted text
            decrypted_text.append(rail_matrix[row][col])
            col += 1
            
            # Change direction when reaching the top or bottom rail
            if row == 0:
                direction_down = True
            elif row == num_rails - 1:
                direction_down = False
                
            # Move to the next row in the current direction
            row += 1 if direction_down else -1
        
        return decrypted_text
    # Test the Rail Fence Cipher
    numbers = [12,45,78,23,56]
    num_rails = 3
    enc = encrypt_rail_fence(numbers, num_rails) 
    dec = decrypt_rail_fence(enc, num_rails)
    print("***RAILFENCE CIPHER***")
    print("The number of rails is: ",num_rails)
    print("Encrypted Numbers:", enc)
    print("Decrypted Numbers:", dec)

def main():
    cipher_map = {
        1: caesar,
        2: mono,
        3: affine,
        4: hill,
        5: playfair,
        6: column,
        7: vigenere,
        8: auto,
        9: homo,
        10: rail
    }
    
    while True:
        print("\nChoose a cipher:")
        print("1. Caesar Cipher")
        print("2. Monoalphabetic Cipher")
        print("3. Affine Cipher")
        print("4. Hill Cipher")
        print("5. Playfair Cipher")
        print("6. Columnar Transposition Cipher")
        print("7. Vigenère Cipher")
        print("8. Autokey Cipher")
        print("9. Homophonic Cipher")
        print("10. Rail Fence Cipher")
        print("Type 'exit' to quit.")
        
        choice = input("Enter your choice: ").strip().lower()
        if choice == "exit":
            print("Exiting the program. Goodbye!")
            break
        elif choice.isdigit() and int(choice) in cipher_map:
            cipher_map[int(choice)]()
        else:
            print("Invalid choice. Please choose a number between 1 and 10, or type 'exit'.")

main()
# caesar()
# mono()
# affine()
# hill() #Have to recheck
# playfair()
# column()
# vigenere()
# auto()
# homo()
# rail()