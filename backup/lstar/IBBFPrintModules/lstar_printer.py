from collections import defaultdict

class LstarPrinter:

    def __init__(self):
        # Nothing to do here
        print ""

    @staticmethod
    def printDFSM(DFSM, description, ObjectClass):

        print "\n\n################################################\n" + description + "\n" \
                  "################################################ "

        initState = DFSM[0]
        finiteStates = DFSM[1]
        ttable = DFSM[2]
        A = DFSM[3]
        ttable_new = defaultdict(list)

        # parse to readable form by exchanging state names with values of the form q_i:
        i = 0
        mapping = {ObjectClass.IBBFObj(''): 'q0'}

        for key in ttable:
            mapping[key] = 'q' + str(i)
            i += 1

        initState = mapping[initState]
        for i in range(0, len(finiteStates)):
            finiteStates[i] = mapping[finiteStates[i]]

        for key in ttable:
            for i in range(0, len(A)):
                ttable[key][i] = mapping[ttable[key][i]]

        for key in ttable:
            ttable_new[mapping[key]] = ttable[key]

        ttable = ttable_new

        # parse headline
        headline = "\ntransition table"
        for i in range(0, len(A)):
            headline += "| " + ''.join(A[i].identifier) + "\t"

        # parse line
        line = ""
        for i in range(0, len(A) + 2):
            line += "--------"

        # parse content
        body = ""
        for key in ttable:
            body += " " + key + "\t-->\t"
            for i in range(0, len(A)):
                body += "| " + ttable[key][i] + "\t"
            body += "\n"

        print headline
        print line
        print body
        print "\nInitial state: " + str(initState)
        print "Final states: " + str(finiteStates)

        return 1