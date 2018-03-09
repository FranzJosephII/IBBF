import nn.nn_main as class_nn
import lstar.lstar_fuzzer as lstar
import monkey.monkey_fuzzer as monkey
import system as s
import datetime
import os
from multiprocessing import Process
import time

_MAXLENGTH = 5  # Characters
_DEBUG = True
_REGEX = ".*a.{2}a.*"  # If None randomly generated
_BUG = "aaazza"  # If None randomly generated
#_REGEX = None  # If None randomly generated
#_BUG = None  # If None randomly generated
reportfile = "logs\\dummy"


system = s.system(_MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile)

# Init fuzzer

fuzzer = class_nn.nn_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # Neural network based fuzzer
#fuzzer = lstar.lstar_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # L* based fuzzer
fuzzer.start()





