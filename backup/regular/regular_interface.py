import random, string, sys
import regular.input_parser as ip

class regular_interface:
    def __init__(self, system):
        self.system = system

    def membership_query(self, sample):
        return self.system.membership_query(sample)

    def fuzz(self, s):

        # fuzz system with given samples
        s = ip.calcstring(s[0])
        #print(s)
        self.system.membership_query(s)

        #for i in range(len(gs)):

        #return self.give_sample()
        """
        # Generate training samples
        batch_x_p = []
        batch_x_n = []
        while(len(batch_x_n) < len(gs)):
            s = self.get_random_string()
            if self.system.membership_query(s):
                batch_x_p.append([ip.calcvector(s)])
            else:
                batch_x_n.append([ip.calcvector(s)])

        if len(batch_x_p) <= 0:
            while(42):
                s = self.get_random_string()
                if self.system.membership_query(s):
                    batch_x_p.append([ip.calcvector(s)])
                    break

        while(len(batch_x_p) < int(len(gs)/1.5)):
            batch_x_p += batch_x_p

        # Concat lists
        batch_x = batch_x_n
        batch_y = []
        for i in range(len(batch_x_n)):
            batch_y.append([0.01])
        batch_x += batch_x_p
        for i in range(len(batch_x_p)):
            batch_y.append([0.99])

        return batch_x, batch_y
        """

    def get_random_string(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(1, 10)))

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

