import lstar.addons.alphabet_parser as ap
import lstar.addons.IBBFObjects.basicObject as ObjectClass
import lstar.interface as mq
import lstar.optimizedTable as t
import lstar.randomCQ as cq
import os


class lstar_fuzzer:
    """
    Implements a lstar based black-box-fuzzer
    """
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
        parser = ap.AlphabetParser("C:/Users/AGANDO/PycharmProjects/IBBF/lstar/addons/alphabet", ObjectClass)
        A = parser.getAlphabet()

        # Init Modules
        MQModule = mq.MQModule(debugFlag, self.system)
        self.tableModule = t.TableModule(ObjectClass, MQModule, A, debugFlag, testFlag)
        self.CQModule = cq.CQModule(ObjectClass, MQModule, parser, debugFlag, self._MAX_LEN, testFlag, DFSM_output)

    def start(self):
        """
        Starts the lstar fuzzer which then learns and starts a fuzzing session after each conjecture-query
        """
        try:
            self.algorithm()
        except SystemExit:
            return
        except:
            print("Test FAILED")
            try:
                os.remove(self.reportfile)
            except:
                pass
            return

    def algorithm(self):
        """
        Implementation of the basic lstar-algorithm
        """
        # Algorithm
        while 42 == 42:
            self.tableModule.fixTable()
            DFSM = self.tableModule.getDFSM()
            counterexample = self.CQModule.isCorrect(DFSM, self.reportfile)
            if counterexample is not "":
                self.tableModule.addCounterexample(counterexample)
                continue
            break



