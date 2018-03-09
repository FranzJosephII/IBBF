import re
import random
import string
import sys
import time

class system:
    """
    Implementation of a system that should be fuzzed. Defines a logic which only accepts certain inputs
    Has a set of bugs which will terminate the system when evaluated.
    """
    def __init__(self, _MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile):

        self._MIN_LEN = 1
        self._MAX_LEN = _MAXLENGTH
        self._DEBUG = _DEBUG
        self.reportfile = reportfile

        self.start_time = None

        # Generate regex
        if _REGEX == None:
            self.regex = re.compile(self.generate_regex())
        else:
            self.regex = re.compile(_REGEX)

        # Uncomment to set difficulty of regex
        #while(self.calc_regex_difficulty() > 0.5 or self.calc_regex_difficulty() < 0.05):
        #    self.regex = re.compile(self.generate_regex())

        # Define Bug
        if _BUG == None:
            letters = string.ascii_lowercase
            while(42):
                sample = ''.join(random.choice(letters) for i in range(random.randint(self._MIN_LEN, self._MAX_LEN)))
                if self.regex.match(sample):
                    self.bug = sample
                    break
        else:
            self.bug = _BUG

        # Create Query Counter
        self.queries = 0

        if _DEBUG:
            print("Regex = " + str(self.regex.pattern))
            print("Difficulty: " + str((1-self.calc_regex_difficulty())*100) + "%")
            print("Bug = " + self.bug)
            print("System initialized")

    def membership_query(self, sample):
        """
        Returns if a given sample is accepted or not
        Quits execution if a bug is found
        """

        # Start timer on first query
        if self.queries == 0:
            self.start_time = time.time()

        # End execution after certain time (5 minutes)
        if (time.time() - self.start_time) > 60*120:
            if self._DEBUG: print("Reached maximum allowed time, stop execution")
            f = open(self.reportfile, 'a')
            f.write(str(self.queries) + ";FAILED\n")
            f.close()
            sys.exit()


        self.queries += 1

        if self._DEBUG and self.queries%1000000 == 0:
            print("Queries used: " + str(self.queries))

        if sample == self.bug:
            if self._DEBUG:
                print("BUG FOUND!!")
                print(sample)
                print("Query Counter: " + str(self.queries))

            # Write to report file
            f = open(self.reportfile, 'a')
            f.write(str(self.queries) + ";FOUND\n")
            f.close()
            sys.exit()

        #elif self.queries > 10000000:
        #    if self._DEBUG: print("Reached maximum of allowed samples")
        #    f = open(self.reportfile, 'a')
        #    f.write(str(self.queries) + ";FAILED\n")
        #    f.close()
        #    sys.exit()

        if self.regex.match(sample):
            return 1
        else:
            return 0

    def match(self, sample):
        """
        Only for debugging
        Returns if a given sample is accepted or not
        """
        if self.regex.match(sample):
            return True
        else:
            return False

    def generate_regex(self):
        """
        A function which generates a random regex as implementation of the systems internal logic
        """
        letters = string.ascii_lowercase
        def add_core():
            c1 = random.choice(letters)
            c2 = random.choice(letters)
            if c1 == c2:
                return "[" + c1 + "]"
            elif ord(c1) < ord(c2):
                return "[" + c1 + "-" + c2 + "]"
            else:
                return "[" + c2 + "-" + c1 + "]"

        def add_layer(regex):
            # 1 = *, 2 = {x}, 3 = {x, y}
            var = random.randint(1, 3)

            if var == 1:
                return regex + ""
            if var == 2:
                return regex + "{" + str(random.randint(2, 5)) + "}"
            if var == 3:
                i = random.randint(1, 3)
                return regex + "{" + str(i) + "," + str(i + random.randint(1, 3)) + "}"

        def add_last_layer(regex):
            # 1 = nothing, 2 = ^x$, 3 = .*x.*
            var = random.randint(1, 3)

            if var == 1:
                return regex
            if var == 2:
                #return "^" + regex + "$"
                return ".*" + regex + ".*"
            if var == 3:
                return ".*" + regex + ".*"


        # Inner Layer - Get a mix of base chars which are used
        regex = add_core()

        # Middle Layer - Define how many Inner layer should be used
        regex = add_layer(regex)

        # Outer layer - Define how strict pattern should be applied
        regex = add_last_layer(regex)

        return regex

    def calc_regex_difficulty(self):
        """
        Evaluates a given regex according to how much matching strings can be found in a random batch of strings
        """
        ctr = 0
        for i in range(10000):
            letters = string.ascii_lowercase
            s = ''.join(random.choice(letters) for i in range(random.randint(self._MIN_LEN, self._MAX_LEN)))
            if self.regex.match(s):
                ctr += 1
        return ctr / 10000