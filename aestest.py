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


#FOR PHASE 5 INTEGRATION INTO PHASE 4

#follwoing are functions to generate a private and public key pair
def extendedGCD(a,b):
    coef_2=(1,0)
    coef_1=(0,1)
    while b!=0:
        quotient=a//b
        (a,b)=(b,a%b)
        (coef_2,coef_1)=(coef_1,(coef_2[0]-quotient*coef_1[0],coef_2[1]-quotient*coef_1[1]))
    return a,coef_2[0],coef_2[1]

def inverseMod(a,m):
    gcd,inv,_=extendedGCD(a,m)
    if gcd != 1:
        raise Exception("Error, "+str(a)+" does not admit an inverse mod "+str(m))
    return inv%m
#keeping p and q fixed as calculating them is beyond scope
p = 5468586886433619073894411726580764173498770708709664207666335008910954157394117737047010310832685387467404417421582009414228902134582657991102753570623459
q = 6442675118318342480288941508523630505099561268793349471454944513843099853236531787541189244253590278169247240616311079998017162034233121434399387485428527
#to generate e to calculate the keys
import math
import random


def generateUserKeyPair(p, q, client):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Generate e
    for _ in range(1000):
        e = random.randint(3, 65537)
        if math.gcd(e, phi_n) == 1:
            break
    else:
        raise Exception("Failed to generate a suitable e after multiple attempts.")

    # Generate d the private key
    d = inverseMod(e, phi_n)

    # Create key pairs
    public_key = (n, e)
    private_key = d

    # Save the private key to a local file
    with open(f"{client}_private_key.txt", "w") as private_file:
        private_file.write(f"Private Key (n, d): {private_key}\n")

    return public_key

def generateUserKeyPair_forUsers(p, q,client1,client2):
    #Generate public-private key pairs for two users and store their private keys in local files.
    
    player1PublicKey = generateUserKeyPair(p, q, client1)
    player2PublicKey = generateUserKeyPair(p, q, client2)

    print("Public keys generated:")
    print(f"User1 Public Key: {player1PublicKey}")
    print(f"User2 Public Key: {player2PublicKey}")

    print("\nPrivate keys stored in local files: 'user1_private_key.txt' and 'user2_private_key.txt'.")
    return player1PublicKey,player2PublicKey

def encryptWithPublicKey(a,e,m):
    #where a is the mssage,e the exponent and m is n
    res=1
    base=a
    bits=bin(e)[2:]
    #here the slicing is because when we convert to ninary it starts with b' whihc is till 2 index
    lst=[]
    for i in bits:
        lst.append(i)
    lst.reverse()
    for i in range(len(lst)):
        if i ==len(lst)-1:
            res=res*base%m
            break
        if lst[i]=='0':
            base=base**2%m
            #this means it is even
        if lst[i]=='1':
            res=res*base%m
            base=base**2%m
            #this means it is odd
    return res

def decryptWithPrivateKey(msg_received,d,n):
    #where d is the private key
    res=1
    base=msg_received
    bits=bin(d)[2:]
    lst=[]
    for i in bits:
        lst.append(i)
    lst.reverse()
    for i in range(len(lst)):
        if i ==len(lst)-1:
            res=res*base%n
            break
        if lst[i]=='0':
            base=base**2%n
        if lst[i]=='1':
            res=res*base%n
            base=base**2%n
    return res

