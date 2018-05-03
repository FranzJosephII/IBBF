from matplotlib import pyplot as plt

data = []
f = open("testing/logs/7/neural", 'r')
for line in f.readlines():
    line = line.strip()
    line = line.split(';')
    data.append(line)
f.close()

print(data)

for i in range(1, len(data)):
    data[i][0] = int(data[i][0]) - int(data[0][0])
    data[i][1] = float(data[i][1])

data[0][0] = 0
data[0][1] = 0

print(data)

x = []
y = []

i = True
for d in data:
    if i:
        i = False
        continue
    x.append(d[0])
    y.append(d[1])


plt.plot(x, y)
plt.ylabel("Accuracy")
plt.xlabel("Used Samples")
#plt.show()
plt.savefig("testing/logs/7/neural.png")
plt.close()


























"""
import string, random, re

letters = string.ascii_lowercase
result = 0
epochs = 10000000


def match(sample):
    for i in range(int(len(sample) / 2)):
        if sample[i] != sample[-(i + 1)]:
            return False
    return True

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if match(sample):
        sum += 1

p = sum/epochs
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))


def match2(self, sample):
    if len(sample) % 3 != 0:
        return False

    for i in range(len(sample)):
        if len(sample) / 3 > i:
            # print("1: " + sample[i])
            if sample[i] != 'a':
                return False
        elif (len(sample) / 3) * 2 > i:
            # print("2: " + sample[i])
            if sample[i] != 'b':
                return False
        else:
            # print("3: " + sample[i])
            if sample[i] != 'c':
                return False
    return True
"""

"""
sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if match(sample):
        sum += 1

p = sum/epochs
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
"""




"""
reg = "a.*"
regex = re.compile(reg)

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if regex.match(sample):
        sum += 1

p = sum/epochs
print(reg)
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
print("###################################")


reg = "[a-m].*"
regex = re.compile(reg)

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if regex.match(sample):
        sum += 1

p = sum/epochs
print(reg)
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
print("###################################")

reg = ".*a.*"
regex = re.compile(reg)

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if regex.match(sample):
        sum += 1

p = sum/epochs
print(reg)
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
print("###################################")

reg = ".*[a-m].*"
regex = re.compile(reg)

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if regex.match(sample):
        sum += 1

p = sum/epochs
print(reg)
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
print("###################################")

reg = ".*[a-m]{4}.*"
regex = re.compile(reg)

sum = 0
for j in range(epochs):
    sample = ''.join(random.choice(letters) for i in range(5))
    if regex.match(sample):
        sum += 1

p = sum/epochs
print(reg)
print("Prozentueller Anteil: " + str(p*100) + "%")
print("Calculated samples: " + str(8235540*p))
print("###################################")
"""