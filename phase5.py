def myGCDIter(a,b):
    while b!=0:
        (a,b)=(b,a%b)
    return a

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

def sqm(a, e, m):
    res = 1
    base = a
    bits = bin(e)[2:]
    bitList=[]
    for i in bits:
        bitList.append(i)
    bitList.reverse()
    for i in range(len(bitList)):
        if i == len(bitList)-1:
            res = res*base%m
            break
        if bitList[i] == '0':
            base = base**2%m
        if bitList[i] == '1':
            res = res*base%m
            base = base**2%m
        
    print(res)
sqm(7,26,13)

p=879444230374861669641134196218346212695898251128878861274462696397360027254709043134636220593750949647657696083593011526569499231402671759015715247847100292170454549945387184247594207004818786761105412070559714186375611091845523065678013356121887671715435435635665666601977029635298290603841109876543
q=884156355539734090651342024511099831516304715462262346470827576945203575116701551738041914223749202101027640044384914081312728700908681008628987214128029359450401447589262841875627065956937931557006312756303050952146176840242929855061267653489429686714147273857523203781398260195342718507985441234567

n=p*q
phiN = (p-1)*(q-1)
def goodExponent(phiN):
    res = 2
    while(extendedGCD(phiN,res)[0]!=1):
        res+=1
    return res
e = goodExponent(phiN)
extendedGCD(phiN,e)

d = inverseMod(e,phiN)

print("Public key:",(e,n))