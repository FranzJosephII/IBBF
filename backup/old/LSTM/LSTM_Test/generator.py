import random
import string
import re
import numpy as np

regex = re.compile("^c.*a$")

def getRandomString():
    """
    Generates random string for further processing
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(random.randint(10, 100)))

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
        vector += b
    return np.array(vector)

def calcstring(vector_f):
    vector = []
    for i in range(len(vector_f)):
        if vector_f[i] > 0.5:
            vector.append(1)
        else:
            vector.append(0)
    string = ""
    for i in range(int(len(vector)/5)):
        b = []
        for j in range(5):
            b.append(vector[i*5 + j])
        b = int("".join(str(i) for i in b), 2)
        string += chr(b+97)
    return string

def gen_batch(batch_size, num_steps):
    raw_x, raw_y = calc_data()
    #print(len(raw_x))
    #print(len(raw_y))
    #print(raw_x)
    #print(raw_y)
    data_length = len(raw_x)

    # partition raw data into batches and stack them vertically in a data matrix
    batch_partition_length = data_length // batch_size
    data_x = np.zeros([batch_size, batch_partition_length])
    data_y = np.zeros([batch_size, batch_partition_length])
    for i in range(batch_size):
        data_x[i] = raw_x[batch_partition_length * i:batch_partition_length * (i + 1)]
        data_y[i] = raw_y[batch_partition_length * i:batch_partition_length * (i + 1)]
    # further divide batch partitions into num_steps for truncated backprop
    epoch_size = batch_partition_length // num_steps

    for i in range(epoch_size):
        x = data_x[:, i * num_steps:(i + 1) * num_steps]
        y = data_y[:, i * num_steps:(i + 1) * num_steps]
        #print(x)
        #print(y)
        #print("#########################################################")
        yield (x, y)

def gen_epochs(n, num_steps, batch_size):
    for i in range(n):
        yield gen_batch(batch_size, num_steps)


def calc_data():
    X = getRandomString()
    Y = ""
    for i in range(len(X)):
        if X[i-2] == 'a':
            Y += 'a'
        else:
            Y += X[i]
    return calcvector(X), calcvector(Y)
    """
def calc_data():

    letters = string.ascii_lowercase
    big_X = []
    big_Y = ""
    for i in range(random.randint(1, 5)):
        choice = random.randint(0, 1)
        #choice = 1
        test_regex = re.compile(".*a.{1}a.*")
        X = []
        Y = ""
        while(42):
            X = []
            Y = ''.join(random.choice(letters) for i in range(10))
            if test_regex.match(Y) and choice:
                #X.append(1)
                #X.append(1)
                #print("found")
                for i in range(len(Y)*5): X.append(1)
                break
            elif not test_regex.match(Y) and not choice:
                #X.append(0)
                #X.append(0)
                for i in range(len(Y)*5): X.append(0)
                break
        big_X += X
        big_Y += Y
    #print(big_Y)
    return big_X, calcvector(big_Y)
    """
    """
    test_regex = re.compile(".*a.{1}a.*")
    letters = string.ascii_lowercase
    X = []
    Y = ""
    for i in range(random.randint(1, 5)):
        str = ''.join(random.choice(letters) for i in range(10))
        Y += str
        if test_regex.match(str):
            for i in range(50): X.append(1)
        else:
            for i in range(50): X.append(0)
    #print(Y)
    return X, calcvector(Y)
    """
    """
    choice = random.randint(0, 1)
    if choice:
        X = []
        for i in range(50): X.append(0)
        Y = "aaaaaaaaaa"
    else:
        X = []
        for i in range(50): X.append(1)
        Y = "zzzzzzzzzz"
    return X, calcvector(Y)
    """



#print(calc_data()[0])


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
        string = getRandomString()
        if regex.match(string):
             return calcvector(string)


def getNegativeSample():
    """
    Generates a random negative sample for Discriminator within a GAN
    """
    while(42):
        string = getRandomString()
        if not regex.match(string):
             return calcvector(string)


def getFuzzerInput():
    """
    Generates a random input for generating a fuzzing sample
    """
    return [random.uniform(0.45, 0.55)]