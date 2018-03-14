import lstar.APModules.alphabet_parser as ap
import lstar.IBBFObjects.basicObject as ObjectClass
import lstar.MQModules.interface as mq
import lstar.TableModules.optimizedTable as t
import lstar.CQModules.randomCQ as cq
import os

"""
Implements the l* algorithm, returns a DFSM
"""
class lstar_fuzzer:
    def __init__(self, system, _MAX_LEN, _DEBUG, reportfile):
        self.system = system
        self._MAX_LEN = _MAX_LEN
        self.reportfile = reportfile

        testFlag = 0
        if _DEBUG:
            debugFlag = 1
        else:
            debugFlag = 0
        DFSM_output = "logs/result.png"

        # parse Alphabet
        parser = ap.AlphabetParser("C:/Users/AGANDO/PycharmProjects/IBBF/lstar/APModules/alphabet", ObjectClass)
        A = parser.getAlphabet()

        # Init Modules
        MQModule = mq.MQModule(debugFlag, self.system)
        self.tableModule = t.TableModule(ObjectClass, MQModule, A, debugFlag, testFlag)
        self.CQModule = cq.CQModule(ObjectClass, MQModule, parser, debugFlag, self._MAX_LEN, testFlag, DFSM_output)

    def start(self):
        #self.algorithm()
        #"""
        try:
            self.algorithm()
        except SystemExit:
            return
        except:
            print("Test FAILED")
            try:
                os.remove(self.reportfile)
            except:
                print("")
            #f = open(self.reportfile, 'w')
            #f.write("TEST FAILED")
            #f.close()
            return
        #"""

    def algorithm(self):
        # Algorithm
        while 42 == 42:
            self.tableModule.fixTable()
            DFSM = self.tableModule.getDFSM()
            counterexample = self.CQModule.isCorrect(DFSM, self.reportfile)
            if counterexample is not "":
                self.tableModule.addCounterexample(counterexample)
                continue
            break



