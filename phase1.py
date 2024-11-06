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


