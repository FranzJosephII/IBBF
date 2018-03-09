_MAXLENGTH = 0

def calcvector(string):
    vector = []
    for c in string:
        b = [int(x) for x in bin(ord(c) - 96)[2:]]
        b.reverse()
        while(len(b) < 5):
            b.append(0)
        b.reverse()
        vector += b
    if len(vector) < _MAXLENGTH:
        for i in range(_MAXLENGTH-len(vector)):
            vector.append(0)
    return vector

def calcstring(vector_f):
    vector = []
    for i in range(_MAXLENGTH):
        if vector_f[i] > 0.5:
            vector.append(1)
        else:
            vector.append(0)
    string = ""
    for i in range(int(_MAXLENGTH/5)):
        b = []
        for j in range(5):
            b.append(vector[i*5 + j])
        b = int("".join(str(i) for i in b), 2)
        if b:
            string += chr(b+96)
        else: string += ""

    return string
