import random, string

class gan_interface:
    """
    This class is used for the communication with the given system
    """
    def __init__(self, system, _MAXLENGTH):
        self.system = system
        self._MAXLENGTH = _MAXLENGTH
        self.old_queries = {}
        self.positive_samples = set()
        self.ctr = 0

    """
    #######################
    # Interface functions #
    #######################
    """
    def membership_query(self, sample):
        """
        Returns a boolean value if the given sample is accepted by the system or not
        """
        if sample not in self.old_queries:
            answer = self.system.membership_query(sample)
            self.old_queries[sample] = answer
            if answer:
                self.positive_samples.add(sample)
        return self.old_queries[sample]

    def get_training_batch(self, amount):
        """
        Returns a training batch with the given amount of positive samples
        Finds new samples every time it is called
        """
        # add positive samples
        for i in range(int(amount/10)):
            self.positive_samples.add(self.get_new_positive_sample())

        # find positive samples if empty
        while(len(self.positive_samples) < amount*10):
            self.positive_samples.add(self.get_new_positive_sample())

        # get selection
        selection = random.sample(self.positive_samples, amount)

        # Parse samples to vector
        for i in range(len(selection)):
            selection[i] = self.calcvector(selection[i])

        # return a selection of positive samples
        return selection

    def fuzz(self, s):
        """
        Fuzzes the system with a given sample
        """
        s = self.calcstring(s[0])
        self.membership_query(s)

    def get_new_positive_sample(self):
        """
        Finds a new positive sample of the system which hasn't been observed in the past
        """
        letters = string.ascii_lowercase

        word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))

        while(42):
            if word not in self.old_queries:
                if self.membership_query(word):
                    break
            word = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))

        return word

    """
    ##############################
    # String operation functions #
    ##############################
    """
    def calcvector(self, string):
        """
        Converts the given string to a vector representation
        """
        vector = []
        for c in string:
            b = [int(x) for x in bin(ord(c) - 96)[2:]]
            b.reverse()
            while (len(b) < 5):
                b.append(0)
            b.reverse()
            vector += b
        if len(vector) < self._MAXLENGTH:
            for i in range(self._MAXLENGTH - len(vector)):
                vector.append(0)
        return vector

    def calcstring(self, vector_f):
        """
        Converts the given vector to a string representation
        """
        vector = []
        for i in range(self._MAXLENGTH):
            if vector_f[i] > 0.5:
                vector.append(1)
            else:
                vector.append(0)
        string = ""
        for i in range(int(self._MAXLENGTH / 5)):
            b = []
            for j in range(5):
                b.append(vector[i * 5 + j])
            b = int("".join(str(i) for i in b), 2)
            if b:
                string += chr(b + 96)
            else:
                string += ""

        return string

    """
    ##############################
    # Random generator functions #
    ##############################
    """
    def getRandomInput(self, length):
        """
        Calculates a random vector of the given length as input for the generator net
        """
        vector = []
        for i in range(length):
            vector.append(random.uniform(0.01, 0.99))
        return vector

    def get_random_string(self):
        """
        Returns a random string
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(1, 10)))

    """
    #######################
    # Debugging functions #
    #######################
    """
    def match(self, sample):
        """
        Returns a boolean value wheter the system accepts the given sample or not
        """
        return self.system.match(sample)