import random
import string

def getRandomString():
    """
    Generates random string for further processing
    """
    letters = string.ascii_lowercase
    return [random.choice(letters) for i in range(10)]

def calc1gram(string):
    """
    Calculates a one-gram representation of a given string
    """
    gram = []
    for i in range(26): gram.append(0)
    for c in string:
        gram[ord(c)-97] += 1
    return(gram)

def getRandomInput():
    """
    Generates random input for Generator within a GAN
    """
    vector = []
    for i in range(10):
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
        vector = calc1gram(getRandomString())
        if vector[0] != 0 and vector[13] != 0:
             return vector


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
        vector = calc1gram(getRandomString())
        if vector[0] == 0 or vector[13]:
             return vector


def getFuzzerInput():
    """
    Generates a random input for generating a fuzzing sample
    """
    return [random.uniform(0.45, 0.55)]