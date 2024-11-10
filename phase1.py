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
