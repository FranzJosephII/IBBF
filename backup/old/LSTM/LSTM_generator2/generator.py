import random
import string
import re

regex = re.compile(".*a.*")
#regex1 = re.compile("efg")
#regex2 = re.compile("abc")

def getRandomString():
    """
    Generates random string for further processing
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def calcvector(string):
    """
    Calculates a one-gram representation of a given string
    """
    vector = []
    for c in string:
        b = [int(x) for x in bin(ord(c) - 97)[2:]]
        b.reverse()
        while(len(b) < 5):
            b.append(0)
        b.reverse()
        vector += [b]
    return vector

def calcstring(vector_s):
    #print(vector_s)
    string = ""
    for v in vector_s:
        vector_f = v[0]
        #print(vector_f)
        vector = []
        bits = len(vector_f)
        chars = int(bits / 5)
        for i in range(bits):
            if vector_f[i] > 0.5:
                vector.append(1)
            else:
                vector.append(0)
        for i in range(chars):
            b = []
            for j in range(5):
                b.append(vector[i*5 + j])
            b = int("".join(str(i) for i in b), 2)
            string += chr(b+97)
            #print(string)
    return string


def getRandomInput():
    """
    Generates random input for Generator within a GAN
    """
    vector = []
    for i in range(5):
        vector.append(random.uniform(0.01, 0.99))
    return vector

def getPositiveSample():
    """
    Generates a random positive sample for Discriminator within a GAN
    """
    while(42):
        #string = getRandomString()
        string = getnewInput(3)
        #if regex1.match(string) or regex2.match(string):
        if regex.match(string):
             return calcvector(string)


def getNegativeSample():
    """
    Generates a random negative sample for Discriminator within a GAN
    """
    while(42):
        #string = getRandomString()
        string = getnewInput(3)
        #if not regex1.match(string) and not regex2.match(string):
        if not regex.match(string):
            return calcvector(string)

def getSample():
    """
    Generates a random sample with a flag if it is positive or negative
    """
    string = getRandomString()
    if regex.match(string):
        return calcvector(string), True
    else:
        return calcvector(string), False

def getFuzzerInput():
    """
    Generates a random input for generating a fuzzing sample
    """
    return [random.uniform(0.45, 0.55)]

def testSample(sample):
    if regex.match(sample): return True
    else: return False

def getnewInput(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))