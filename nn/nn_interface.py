import random, string
import numpy

class nn_interface:
    """
    This class is used for the communication with the given system
    """
    def __init__(self, system, _MAXLENGTH):
        self.system = system
        self._MAXLENGTH = _MAXLENGTH
        self._MAXWORDLENGTH = int(_MAXLENGTH/5)

        self.probs = []
        sum = 0
        for i in range(1, self._MAXWORDLENGTH + 1):
            self.probs.append(26 ** i)
            sum += self.probs[-1]

        for i in range(0, self._MAXWORDLENGTH):
            self.probs[i] /= sum

    """
    #######################
    # Interface functions #
    #######################
    """
    def membership_query(self, sample):
        """
        Returns a boolean value if the given sample is accepted by the system or not
        """
        return self.system.membership_query(sample)

    def get_training_batch(self, amount):
        """
        Returns a training batch
        """
        while(42):
            samples = []
            labels = []
            neg = 0
            pos = 0
            while(amount*9/10 > neg and amount*9/10 > pos and amount > (neg+pos)):
                sample = self.get_random_string()
                samples.append(self.calcvector(sample))
                label = self.membership_query(sample)
                if label == 1:
                    pos += 1
                else:
                    neg += 1
                labels.append([label])

            # Fill rest of the training batch with missing positive or negative samples
            if pos < neg:
                for i in range(amount-neg-pos):
                    samples.append(self.calcvector(self.get_new_sample(True)))
                    labels.append([1])
                    pos += 1
            else:
                for i in range(amount-neg-pos):
                    samples.append(self.calcvector(self.get_new_sample(False)))
                    labels.append([0])
                    neg += 1

            return (samples, labels)

    def get_new_sample(self, bool):
        """
        Returns a new sample which is accepted or not by the system
        """
        word = self.get_random_string()
        while(self.membership_query(word) != bool):
            word = self.get_random_string()
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
    def get_random_string(self):
        """
        Returns a random string
        """
        letters = string.ascii_lowercase
        #return ''.join(random.choice(letters) for i in range(random.randint(1, self._MAXWORDLENGTH)))
        return ''.join(random.choice(letters) for j in range(numpy.random.choice(numpy.arange(1, self._MAXWORDLENGTH+1), p=self.probs)))


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

    def queries(self):
        """
        Returns the current amount of queries which has been used
        :return:
        """
        return self.system.queries