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
    def __init__(self, _MAXLENGTH, _BUG, _DEBUG, reportfile):

        self._MIN_LEN = 1
        self._MAX_LEN = _MAXLENGTH
        self._DEBUG = _DEBUG
        self.reportfile = reportfile

        self.start_time = None

        # Define Bug
        self.bug = _BUG

        # Create Query Counter
        self.queries = 0

        if _DEBUG:
            print("Grammar := (a^n)(b^n)(c^n):n>=1")
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

        if self.match(sample):
            return 1
        else:
            return 0

    def match(self, sample):
        """
        Only for debugging
        Returns if a given sample is accepted or not
        """
        ctr1 = 0
        ctr2 = 0
        ctr3 = 0
        class1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        class2 = ['j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']
        class3 = ['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        i = 0

        while(i < len(sample)):
            if sample[i] in class1:
                ctr1 += 1
                i += 1
            else:
                break

        while(i < len(sample)):
            if sample[i] in class2:
                ctr2 += 1
                i += 1
            else:
                break

        while(i < len(sample)):
            if sample[i] in class3:
                ctr3 += 1
                i += 1
            else:
                return False

        #print(ctr1)
        #print(ctr2)
        #print(ctr3)


        if ctr1 >= ctr2 >= ctr3:
            return True
        return False

#print(match("ajaz"))






