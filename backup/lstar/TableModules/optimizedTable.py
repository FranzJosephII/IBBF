from APModules import alphabet_parser
from IBBFObjects import basicObject
from MQModules import regexMQ
from CQModules import randomCQ
from IBBFPrintModules import lstar_printer
import sys
from sets import Set
import time

class TableModule:
    """
    Init lstar instance
    """

    def __init__(self, ObjectClass, MQModule, A, debugFlag, params, testFlag):

        self._DEBUG_ = debugFlag
        self.MQModule = MQModule
        self.ObjectClass = ObjectClass
        self._TIME_ = 0
        self._TEST_ = testFlag

        self.A = Set(A)
        self.SA = Set()
        self.S = Set()
        self.addS(self.ObjectClass.IBBFObj(''))
        self.E = Set()
        self.E.add(self.ObjectClass.IBBFObj(''))

        self.lookupTable = {}

        self.printTable("Initial Table")

    def getTime(self):
        return self._TIME_

    @staticmethod
    def getTestParameter():
        return ""

    def addS(self, obj):
        self.S.add(obj)
        for a in self.A:
            self.SA.add(obj+a)
        return 1

    def getValue(self, obj):
        if obj not in self.lookupTable:
            self.lookupTable[obj] = self.membershipQuery(obj)
        return self.lookupTable[obj]

    """
    Fixes Table so it is closed and consistent
    """
    def fixTable(self):

        start_time = time.time()

        while 42 == 42:
            answer = self.testTableClosed()
            if answer != 1:
                self.fixTableNotClosed(answer)
                self.printTable("Table after closing it")
                continue
            answer = self.testTableConsistent()
            if answer != 1:
                self.fixTableInconsistent(answer)
                self.printTable("Table after fixing inconsistency")
                continue
            self._TIME_ += time.time() - start_time
            return 1

        self._TIME_ += time.time() - start_time
        return 0

    """
    Tests if the Table is consistent, returns '' if yes and the value of s_1 and s_2 if not
    """
    def testTableConsistent(self):

        # Search for identical rows in S
        for s1 in self.S:
            for s2 in self.S:
                if self.queryRow(s1) == self.queryRow(s2):

                    # if found, test if row(s1+a) == row(s_2+a)
                    for a in self.A:
                        if self.queryRow(s1+a) != self.queryRow(s2+a):
                            return s1, s2
        return 1

    """
    Fixes a table which is not consistent, returns 1 on success and 0 on failure
    """
    def fixTableInconsistent(self, s):

        # Search for suitable candidates of a and e to fix the inconsistency of the given values s_1, s_2
        for a in self.A:
            for e in self.E:
                if self.getValue(s[0] + a + e) is not self.getValue(s[1] + a + e):

                    # add suitable value (ae) to E
                    self.E.add(a + e)
                    return 1
        return 0

    """
    Test if the table is closed, returns '' if yes and the value if not
    """
    def testTableClosed(self):

        for sa in self.SA:
            found = 0
            for s in self.S:
                if self.queryRow(sa) == self.queryRow(s):
                    found = 1
                    break
            if found == 0:
                return sa
        return 1

    """
    Fixes a table which is not closed by adding the missing value and returns 1 on success and 0 on failure
    """
    def fixTableNotClosed(self, obj):

        self.addS(obj)
        self.SA.discard(obj)
        return 1

    """
    Returns a whole row to a given value from S or SA
    """
    def queryRow(self, obj):

        row = ''
        for e in self.E:
            row += self.getValue(obj+e)
        return row

    """
    Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
    """
    def membershipQuery(self, teststring):

        return self.MQModule.isMember(teststring)

    """
    Constructs a DFSM candidate and does a conjecture query
    """
    def getDFSM(self):

        start_time = time.time()

        initState = 0
        finalStates = []
        ttable = {}
        states = {}
        ttable_row = []

        # parse different states
        for s in self.S:
            states[self.queryRow(s)] = s

        # parse initial and final states
        for s in states:
            if self.getValue(states[s]+self.ObjectClass.IBBFObj('')) == '1':
                finalStates.append(states[s])
            if states[s] == self.ObjectClass.IBBFObj(''):
                initState = states[s]

        # Create transition table
        for s in states:
            for a in self.A:
                ttable_row.append(states[self.queryRow(states[s]+a)])
            ttable[states[s]] = ttable_row
            ttable_row = []

        self._TIME_ += time.time() - start_time
        return initState, finalStates, ttable, list(self.A)

    """
    Adds a given counterexample to the Table
    """
    def addCounterexample(self, counterexample):

        start_time = time.time()

        # Generate list of objects to add
        example = self.ObjectClass.IBBFObj(counterexample[0])
        example_list = [example]
        for i in range(1, len(counterexample)):
            example += self.ObjectClass.IBBFObj(counterexample[i])
            example_list.append(example)

        # add objects
        for e in example_list:
            self.addS(e)

        # Clean SA
        self.SA = self.SA.difference(self.S)

        self.printTable("Table after adding counterexample \"" + str(counterexample) + "\"")

        self._TIME_ += time.time() - start_time
        return 1

    """
    Prints a visual representation of the Table (S,E,T)
    """
    def printTable(self, description):

        if self._DEBUG_ and not self._TEST_:
            print "\n\n################################################\n" + description + "\n" \
                  "################################################ "

            header = "T\t\t"
            splitline = "\n---------"
            for e in self.E:
                header += "| " + str(e.identifier) + "\t\t|"
                splitline += "--------"

            rows_S = ""
            for s in self.S:
                rows_S += "\n" + str(s.identifier) + "\t\t|"
                for e in self.E:
                    rows_S += " " + self.getValue(s+e) + "\t\t|"

            rows_SA = ""
            for sa in self.SA:
                rows_SA += "\n" + str(sa.identifier) + "\t\t|"
                for e in self.E:
                    rows_SA += " " + self.getValue(sa+e) + "\t\t|"

            print (header + splitline + rows_S + splitline + rows_SA)
            return 1

"""
def testMain():

    # make instance:
    ObjectClass = basicObject
    parser = alphabet_parser.AlphabetParser("C:/_Daten/Daten/IBBF/test_alphabet.txt", ObjectClass)
    A = parser.getAlphabet()
    MQModule = regexMQ.MQModule(1, "1[0,1]*1")
    CQModule = randomCQ.CQModule(ObjectClass, MQModule, parser, 0, '10000,50', 0)

    TestInstance = TableModule(ObjectClass, MQModule, A, 1, "", 0)
    answer = TestInstance.testTableClosed()

    if answer != 1:
        TestInstance.fixTableNotClosed()
    TestInstance.printTable("Test")

    DFSM = TestInstance.getDFSM()

    #lstar_printer.LstarPrinter.printDFSM(DFSM, "TEST", ObjectClass)

    answer = CQModule.isCorrect(DFSM)

    return 1

testMain()

"""