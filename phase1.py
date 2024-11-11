#ashjar's part of affine and monosubstituition ciphers
# %%
import random as rand
ALPHABET="abcdefghijklmnopqrstuvwxyz ."
def permute(characters):
    cipherText=''
    length=len(characters)
    for i in range(length):
        randnum=rand.randint(0,len(characters)-1)
        cipherText+=characters[randnum]
        characters=characters.replace(characters[randnum],'')
    return cipherText
permute(ALPHABET)

# %%
def monoSub(plainText,characters):
    char=permute(characters)
    trans=str.maketrans(characters,char)
    print("The key is: ",char)
    return plainText.translate(trans)
print(monoSub("hello",ALPHABET))

# %%
def monoUnSub(cipherText, characters, key):
    trans=str.maketrans(key,characters)
    return cipherText.translate(trans)
print(monoUnSub("icxxr",ALPHABET,"eoymclhivazxfqrbpwdu n.gktjs"))

# %%
def myGCDRec(a,b):
    if(b == 0):
        return abs(a)
    else:
        return myGCDRec(b, a%b )
print(myGCDRec(25,5))

# %%
def extendedGCD(a,b):
    s1=1
    t1=0
    s2=0
    t2=1

    while(a%b!=0):
        r=a%b
        s3=s1-(s2*(a//b))
        t3=t1-(t2*(a//b))
        a=b
        b=r
        s1,t1=s2,t2
        s2,t2=s3,t3
    return s3,t3
print(extendedGCD(27,7))

# %%
def inverseMod(a,m):
    if(myGCDRec(a,m)!=1):
        print("Inverse doesnt exist")
    else:
        num=extendedGCD(a,m)
        return num[1]
inverseMod(28,5)

# %%
def affineCipherEncrypt(plainText,k,a):
  cipherText = ""
  for i in plainText:
    letterIndex = ALPHABET.index(i)
    cipherText+=ALPHABET[(letterIndex*k+a)%len(ALPHABET)]
  return cipherText
affineCipherEncrypt("sleep",5,2)


# %%
def affineCipherDecrypt(cipherText,k,a):
  plainText = ""
  inverseK = inverseMod(len(ALPHABET),k)
  if(inverseK<0):
    inverseK+=len(ALPHABET)
  for i in cipherText:
    letterIndex = ALPHABET.index(i)
    plainText+= ALPHABET[(inverseK*(letterIndex-a))%len(ALPHABET)]
  return plainText
affineCipherDecrypt("ibwwv",5,2)


#####hafsa -caesar & hill cipher
#for testing,i used input prompts so you can check extensively.

# CAESAR CIPHER Encryption
def rotate(char,shift):
    if(shift>len(char)):
        shift=shift%len(char)
        #this line is for shift bigger than length of char,it takes the remainder and then does the same function
    return(char[shift:]+char[0:shift])

def caesarEncrypt(plaintext, characters, shift):
    shifted_chars=rotate(characters,shift)
    mytable=str.maketrans(characters, shifted_chars)
    #maketrans(x,y) where x is the og and the y are the values that it is replaced by
    return(plaintext.translate(mytable))

plaintext=input("Enter your plaintext:")
shift=int(input("Enter the shift/key:"))
ciphertxt=caesarEncrypt(plaintext,ALPHABET,shift)
print("cipher is: ",ciphertxt)

# CAESAR CIPHER Decryption

def caesarDecrypt(ciphertext, characters, shift):
    shifted_chars = rotate(characters, -shift)
    mytable = str.maketrans(characters, shifted_chars)
    return ciphertext.translate(mytable)

ciphertext=input("Enter your ciphertext:")
shift=int(input("Enter the shift/key:"))
plaintext=caesarDecrypt(ciphertext,ALPHABET,shift)
print("plaintext is: ",plaintext)

#HILL CIPHER Encryption
def det(a):
    ElemA=1
    ElemB=1
    if len(a) != 2 or len(a[0]) != 2 or len(a[1]) != 2:
        return False
    for row in range(len(a)): 
        for col in range(len(a[row])): 
            if row==col:
                ElemA*=a[row][col] 
            else:
                ElemB*=a[row][col] 

                
    det=ElemA-ElemB
    return det

def Hill_extendedGCD(a, b):
    if b == 0:
        return a, 1, 0
    
    gcd, s1, t1 = extendedGCD(b, a % b)

    s = t1
    t = s1 - (a // b) * t1

    return gcd, s, t

def hillCipherEncrypt(pt, k, alphabet):
    determinant = det(k)
    if determinant == False:
        return "The input must be a 2x2 matrix"

    gcd, _, _ = Hill_extendedGCD(determinant, len(alphabet))
    #here its _ as the other variables returned from this function will not be used 
    if gcd != 1:
        return "The key matrix does not admit an inverse."

    if len(pt) % 2 != 0:
        pt += alphabet[0]

    pt_numbers = [alphabet.index(char) for char in pt]

    encrypted_numbers = []
    for i in range(0, len(pt_numbers), 2):
        x1 = pt_numbers[i]
        x2 = pt_numbers[i + 1]
        
        y1 = (k[0][0] * x1 + k[0][1] * x2) % len(alphabet)
        y2 = (k[1][0] * x1 + k[1][1] * x2) % len(alphabet)
        encrypted_numbers.extend([y1, y2])

    encrypted_text = ''.join([alphabet[num] for num in encrypted_numbers])
    return encrypted_text

k = [[1, 2], [4, 3]]
plaintext =input("Enter your plaintext:")
ciphertext = hillCipherEncrypt(plaintext, k, ALPHABET)
print(ciphertext)

##HILL CIPHER Decryption

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
    
def hillCipherDecrypt(ct, k, alphabet):
    determinant = det(k)
    if determinant == False:
        return "The input must be a 2x2 matrix"

    m = len(alphabet)
    inverse_k = Hill_inverseMatrixMod(k, m)
    if inverse_k == "The matrix does not admit an inverse.":
        return inverse_k

    ct_numbers = [alphabet.index(char) for char in ct]

    decrypted_numbers = []
    for i in range(0, len(ct_numbers), 2):
        y1 = ct_numbers[i]
        y2 = ct_numbers[i + 1]
        
        x1 = (inverse_k[0][0] * y1 + inverse_k[0][1] * y2) % m
        x2 = (inverse_k[1][0] * y1 + inverse_k[1][1] * y2) % m
        decrypted_numbers.extend([x1, x2])

    decrypted_text = ''.join([alphabet[num] for num in decrypted_numbers])
    
    if decrypted_text[-1] == alphabet[0]:
        decrypted_text = decrypted_text[:-1]
    return decrypted_text

k = [[1, 2], [4, 3]]
ciphertext =input("Enter your ciphertext:")
plaintext = hillCipherDecrypt(ciphertext, k, ALPHABET)
print(plaintext)

#####Fazil - Playfair & Columnar

#Playfair
def generate_playfair_matrix(keyword):
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
    
    return playfair_matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None

def playfair_encrypt(plaintext, keyword):
    matrix = generate_playfair_matrix(keyword)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    encrypted_text = ""
    
    i = 0
    while i < len(plaintext):
        if i + 1 == len(plaintext) or plaintext[i] == plaintext[i + 1]:
            pair = plaintext[i] + "X"
            i += 1
        else:
            pair = plaintext[i] + plaintext[i + 1]
            i += 2

        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])

        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]

    return encrypted_text

def playfair_decrypt(ciphertext, keyword):
    matrix = generate_playfair_matrix(keyword)
    decrypted_text = ""
    
    i = 0
    while i < len(ciphertext):
        pair = ciphertext[i] + ciphertext[i + 1]
        i += 2

        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])

        if row1 == row2:
            decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += matrix[row1][col2] + matrix[row2][col1]

    return decrypted_text

#Test - Playfair Encryption
print("PLAYFAIR TEST")
cipher=playfair_encrypt("lord Granvilles letter","palmerstone")
print(cipher)

plaintext = playfair_decrypt(cipher,"palmerstone")
print(plaintext)

#####Fazil - Columnar Transposition
import math

def reOrderKey(t):
    asciiConv=[]
    for i in t:
        asciiConv.append(ord(i))
    ordered = sorted(asciiConv)
    
    l=[]
    for i in asciiConv:
        l.append(ordered.index(i))
    
    return l

def columnarTransposition(m,k):
    keyOrder = reOrderKey(k)
    keyLength = len(k)
    fillLetters = ['u','v','w','x','y','z']
    i=0
    m=m.split(" ")
    
    k=""
    for i in m:
        k+=i
    m=k
    
    remainder = len(m) % keyLength
    if remainder != 0:
        padding_needed = keyLength - remainder
        padding_index = 0
        while padding_needed > 0:
            m += fillLetters[padding_index % len(fillLetters)]
            padding_index += 1
            padding_needed -= 1
    
  
    l=[]
    for i in range(len(keyOrder)):
        l.append(m[i::keyLength])
        
    
    dictionary={}
    index=0
    for i in keyOrder:
        dictionary[i] = l[index]
        index+=1
    
    c=""
    for key in (sorted(dictionary)):
        c+=dictionary[key]

    return c

def decryptColumnarTransposition(c,k):
    rows = len(c)/len(k)
    cipherBlock=[]
    block=""
    i=0
    
    m=""
    for i in range(int(rows)):
        for j in reOrderKey(k):
            m+=c[i+int(j*rows)]    
    
    return m

#Test - Columnar
print("Columnar Transposition Test")
cipher=columnarTransposition("attackpostponeduntiltwoam","ciphers")
print(cipher)
plaintext=decryptColumnarTransposition(cipher,"ciphers")
print(plaintext)
