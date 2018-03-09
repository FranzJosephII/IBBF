import sys
#import nn.nn_main
import nn.nn_main as class_nn
import lstar.lstar_fuzzer as lstar
import monkey.monkey_fuzzer as monkey
import system as s
#import datetime
#import os
#from multiprocessing import Process
#import time

_DEBUG = False

_REGEX = sys.argv[1]
_BUG = sys.argv[2]
_MAXLENGTH = int(sys.argv[3])
reportfile = sys.argv[4]
method = sys.argv[5]

system = s.system(_MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile)

if method == "monkey":
    fuzzer = monkey.monkey_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)
    fuzzer.start()

elif method == "lstar":
    fuzzer = lstar.lstar_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)
    fuzzer.start()

elif method == "neural":
    fuzzer = class_nn.nn_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)
    fuzzer.start()

else:
    print("ERROR: Method not found")
    sys.exit()

