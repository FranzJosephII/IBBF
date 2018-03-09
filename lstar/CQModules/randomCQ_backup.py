import random
import time
from lstar.IBBFPrintModules import lstar_printer
# try:
import lstar.IBBFPrintModules.lstar_drawer as lstar_drawer

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

        # parameter = params.split(",")

        # self.tries = int(parameter[0])
        self.length = _MAX_LEN

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
        for j in range(0, random.randint(0, self.length - 1)):
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

        self.evaluate(DFSM, reportfile)

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

        # Generate examples and query them
        pos = 0
        for i in range(amount):
            # Get sample
            example, answer = self.getSample(A, initState, stateTransTable, finiteStates)
            query = self.ObjectClass.IBBFObj('')
            for a in example:
                query += self.ObjectClass.IBBFObj(a)
            # Compare
            #print(answer)
            #print(self.MQModule.isMember_debug(query))
            if (answer == '1' and self.MQModule.isMember_debug(query)) or (answer == '0' and self.MQModule.isMember_debug(query)):
                #print("TRUE")
                pos += 1
            #else:
            #    print(False)
        acc = pos/amount

        f = open(reportfile, 'a')
        f.write(str(self.MQModule.queries()) + ";" + str(acc) + "\n")
        f.close()