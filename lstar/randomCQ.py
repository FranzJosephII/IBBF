import random
import time
from lstar.addons.IBBFPrintModules import lstar_printer
import lstar.addons.IBBFPrintModules.lstar_drawer as lstar_drawer
import numpy

drawer = 1

class CQModule:
    """
	Init lstar instance
	"""

    def __init__(self, ObjectClass, MQModule, parser, debugFlag, _MAX_LEN, testFlag, DFSM_output):

        self._DEBUG_ = debugFlag
        self._TIME_ = 0
        self._TEST_ = testFlag
        self.drawer_para = DFSM_output

        self.MQModule = MQModule
        self.Parser = parser
        self.ObjectClass = ObjectClass

        self.testdata = None

        self.accs = [0]

        self.length = _MAX_LEN

        self.probs = []
        sum = 0
        for i in range(1, self.length + 1):
            self.probs.append(26 ** i)
            sum += self.probs[-1]

        for i in range(0, self.length):
            self.probs[i] /= sum

    def getTime(self):
        return self._TIME_

    @staticmethod
    def getTestParameter():
        return "1000000,50"

    """
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""

    def membershipQuery(self, teststring):
        return self.MQModule.isMember(teststring)

    def getSample(self, A, initState, stateTransTable, finiteStates):

        # Generate random example
        example = []
        for j in range(0, numpy.random.choice(numpy.arange(1, 6), p=self.probs)):
            example.append(A[random.randint(0, len(A) - 1)].identifier[0])

        # Calculate membership according to own DFSM
        answer = initState
        for a in example:
            answer = stateTransTable[(answer, a)]
        if answer in finiteStates:
            answer = '1'
        else:
            answer = '0'
        return (example, answer)


    """
	Generates x examples, if no counterexample was found the given DFSM, by chance, is correct
	"""
    def isCorrect(self, DFSM, reportfile):


        self.accs.append(self.evaluate(DFSM, reportfile))

        start_time = time.time()

        initState = DFSM[0]
        finiteStates = DFSM[1]
        ttable = DFSM[2]
        A = DFSM[3]

        # Generate table for mapping state transitions
        stateTransTable = {'': ''}
        stateTransTable.clear()

        for key in ttable:
            for i in range(0, len(A)):
                stateTransTable[(key, A[i].identifier[0])] = ttable[key][i]

        if self.accs[-1] == 1. or self.accs[-1] < self.accs[-2]:
            amount = 1000000000

        # Calculate how many positive samples should be tested before switching to random samples
        amount = len(A) * len(ttable) * 10000

        # Generate examples and query them
        tries = 0
        while (42 == 42):

            # Get sample
            example, answer = self.getSample(A, initState, stateTransTable, finiteStates)
            if len(finiteStates) > 0 and tries < amount and answer != '1':
                #print(answer)
                continue
            if answer == '1':
                tries += 1
                #if tries % 1000 == 0:
                    #print(tries)

            # Generate Query object
            query = self.ObjectClass.IBBFObj('')
            for a in example:
                query += self.ObjectClass.IBBFObj(a)

            # Compare
            if answer != self.membershipQuery(query):
                if self._DEBUG_ and not self._TEST_:
                    lstar_printer.LstarPrinter.printDFSM(DFSM, "Following is not the correct DFSM", self.ObjectClass)
                self._TIME_ += time.time() - start_time
                return [''] + example

        self._TIME_ += time.time() - start_time
        if not self._TEST_:
            if self.drawer_para != 0 and drawer != 0:
                lstar_drawer.LstarPrinter().drawDFSM(DFSM, "Following is the correct DFSM", self.ObjectClass,
                                                     self.drawer_para)
            else:
                lstar_printer.LstarPrinter.printDFSM(DFSM, "Following is the correct DFSM", self.ObjectClass)
        return ''

    def evaluate(self, DFSM, reportfile):
        initState = DFSM[0]
        finiteStates = DFSM[1]
        ttable = DFSM[2]
        A = DFSM[3]
        amount = 10000

        # Generate table for mapping state transitions
        stateTransTable = {'': ''}
        stateTransTable.clear()

        for key in ttable:
            for i in range(0, len(A)):
                stateTransTable[(key, A[i].identifier[0])] = ttable[key][i]

        # Generate testdata
        if self.testdata == None:
            examples = []
            answers = []
            pos = 0
            neg = 0
            amount = 10000

            while (amount * 9 / 10 > neg and amount * 9 / 10 > pos and amount > (neg + pos)):
                example = []
                for j in range(0, numpy.random.choice(numpy.arange(1, 6), p=self.probs)):
                    example.append(A[random.randint(0, len(A) - 1)].identifier[0])
                query = self.ObjectClass.IBBFObj('')
                for a in example:
                    query += self.ObjectClass.IBBFObj(a)

                answer = self.MQModule.isMember(query)
                #print(answer)
                if answer == '1':
                    pos += 1
                else:
                    neg += 1

                examples.append(example)
                answers.append(answer)

            #print(pos)
            #print(neg)

            # Fill rest of the training batch with missing positive or negative samples
            example = []
            answer = None
            if pos < neg:
                for i in range(amount - neg - pos):
                    while(42):
                        example = []
                        for j in range(0, numpy.random.choice(numpy.arange(1, 6), p=self.probs)):
                            example.append(A[random.randint(0, len(A) - 1)].identifier[0])
                        query = self.ObjectClass.IBBFObj('')
                        for a in example:
                            query += self.ObjectClass.IBBFObj(a)

                        answer = self.MQModule.isMember(query)
                        if answer == '1':
                            #print(example)
                            break
                    examples.append(example)
                    answers.append(answer)
                    pos += 1
            else:
                for i in range(amount - neg - pos):
                    while (42):
                        example = []
                        for j in range(0, numpy.random.choice(numpy.arange(1, 6), p=self.probs)):
                            example.append(A[random.randint(0, len(A) - 1)].identifier[0])
                        query = self.ObjectClass.IBBFObj('')
                        for a in example:
                            query += self.ObjectClass.IBBFObj(a)

                        answer = self.MQModule.isMember(query)
                        if answer == '0':
                            break
                    examples.append(example)
                    answers.append(answer)
                    neg += 1

            #print(pos)
            #print(neg)

            self.testdata = (examples, answers)
            #print("Claculated test data")

            """
            for i in range(amount):
                example = []
                for j in range(0, random.randint(0, self.length - 1)):
                    example.append(A[random.randint(0, len(A) - 1)].identifier[0])
                examples.append(example)

                query = self.ObjectClass.IBBFObj('')
                for a in example:
                    query += self.ObjectClass.IBBFObj(a)
                answers.append(self.MQModule.isMember(query))
                self.testdata = (examples, answers)
            """

        # Evaluate on test data
        examples, answers = self.testdata
        pos = 0
        for i in range(amount):
            # Get sample
            example = examples[i]
            answer_sys = answers[i]

            answer_dfsm = initState
            for a in example:
                answer_dfsm = stateTransTable[(answer_dfsm, a)]
            if answer_dfsm in finiteStates:
                answer_dfsm = '1'
            else:
                answer_dfsm = '0'


            if (answer_sys == answer_dfsm):
                #print("TRUE")
                pos += 1
            #else:
            #    print(False)
        acc = pos/amount
        print("Accuracy: " + str(acc))

        f = open(reportfile, 'a')
        f.write(str(self.MQModule.queries()) + ";" + str(acc) + "\n")
        f.close()

        return acc