from collections import defaultdict
import os
import webbrowser
import importlib
gv = (importlib.import_module('graphviz'))

class LstarPrinter:

    def __init__(self):
        # Nothing to do
        print ""

    def drawDFSM(self, DFSM, description, ObjectClass, filename):

        filename = filename.split('.')

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

        # Print to console
        print "\n\n################################################\n" + description + "\n" \
                  "################################################ "
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


        # init Machine object
        g = gv.Digraph(format=filename[1])

        # add states
        for t in ttable:
            if t not in finiteStates:
                g.node(t)
            else:
                g.attr('node', shape='doublecircle')
                g.node(t)
                g.attr('node', shape='circle')

        # add edges
        stateTransTable = {'': ''}
        stateTransTable_tmp = {'': ''}
        stateTransTable.clear()
        stateTransTable_tmp.clear()

        # summarize transitions
        for key in ttable:
            for i in range(0, len(A)):
                stateTransTable[(key, "".join(A[i].identifier[0]))] = ttable[key][i]


        for t_1 in stateTransTable:
            tmp_string = t_1[1]
            for t_2 in stateTransTable:
                if t_1[0] == t_2[0] and stateTransTable[t_1] == stateTransTable[t_2] and t_1 is not t_2:
                    tmp_string += "," + t_2[1]
                    stateTransTable[t_2] = ''
            stateTransTable_tmp[(t_1[0], tmp_string)] = stateTransTable[t_1]
        stateTransTable = stateTransTable_tmp

        for t in stateTransTable:
            if stateTransTable[t] is not '':
                g.edge(t[0], stateTransTable[t], self.sanitize(t[1]))

        # draw DFSM
        g.render(filename[0])
        os.remove(filename[0])
        webbrowser.open('.'.join(filename))

        return 1

    def sanitize(self, string):

        list_org = string.split(',')
        list_org.sort()
        list_tmp = []
        list_new = []

        # Following Code summarizes characters (eg: a,b,c,d -> a-d)
        # Automatically detects if only character are used.
        for e in list_org:
            if len(e) != 1:
                list_tmp.append(e)
        for e in list_tmp:
            list_org.remove(e)

        i = 0
        while i < len(list_org):
            j = 1
            while(42):
                if not(i+j == len(list_org)) and ord(list_org[i]) == ord(list_org[i+j])-j:
                    j += 1
                    continue
                else:
                    if j > 1:
                        list_new.append(list_org[i] + "-" + list_org[i+j-1])
                    else:
                        list_new.append(list_org[i])
                    break
            i += j
        list_new += list_tmp
        string = ",".join(list_new)

        return string