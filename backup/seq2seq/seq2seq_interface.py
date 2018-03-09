import random, string, re
import system

#regex = re.compile("^l.*d$")

class s2s_interface:

    def __init__(self, system):
        self.system = system

    def membership_query(self, sample):
        return self.system.membership_query(sample)

    def fuzz(self, sample):
        self.system.membership_query(sample)

    def get_positive_sample(self):
        letters = string.ascii_lowercase

        output = ""
        word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))

        while not self.membership_query(word):
            word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))
        for c in word:
            output += c
        return output


    def get_negative_sample(self):
        letters = string.ascii_lowercase

        output = ""
        word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))

        while(self.membership_query(word)):
            word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))
        for c in word:
            output += c
        return output


    def give_sample(self):
        if random.randint(0, 1):
            input = "1"
            output = self.get_positive_sample()
        else:
            input = "0"
            output = self.get_negative_sample()
        return input, output
