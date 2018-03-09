import random
import string
import re

regex = re.compile("abc")

def getRandomString():
    """
    Generates random string for further processing
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def calc2gram(string):
    """
    Calculates a one-gram representation of a given string
    """
    gram = []
    for i in range(26+26*26): gram.append(0)
    for c in string:
        gram[ord(c)-97] += 1
    for i in range(len(string)-1):
        pos = (ord(string[i])-96)*26 + (ord(string[i+1])-97)
        gram[pos] += 1
    return gram

def getRandomInput():
    """
    Generates random input for Generator within a GAN
    """
    vector = []
    for i in range(64):
        vector.append(random.uniform(0.01, 0.99))
    return vector

def getPositiveSample():
    """
    Generates a random positive sample for Discriminator within a GAN
    """
    """vector = []
    vector.append(random.uniform(0.8, 0.99))
    for i in range(25):
        vector.append(random.uniform(0.01, 0.99))
    return vector"""
    while(42):
        string = getRandomString()
        if regex.match(string):
             return calc2gram(string)


def getNegativeSample():
    """
    Generates a random negative sample for Discriminator within a GAN
    """
    """vector = []
    vector.append(random.uniform(0.01, 0.2))
    for i in range(25):
        vector.append(random.uniform(0.01, 0.99))
    return vector"""
    while(42):
        string = getRandomString()
        if not regex.match(string):
             return calc2gram(string)


def getFuzzerInput():
    """
    Generates a random input for generating a fuzzing sample
    """
    return [random.uniform(0.45, 0.55)]

def gramToString(vector):
    "Generates a string representation out of a two-gram"
    string = ""
    twograms = []
    for i in range(26, 702):
        if vector[i] > 0.5:
            twograms.append(chr(int(i/26+96)) + chr((i%26)+97))
    return twograms
