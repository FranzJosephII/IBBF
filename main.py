import nn.nn_main as class_nn
import lstar.lstar_fuzzer as lstar
import system as s


_MAXLENGTH = 5  # Characters
_DEBUG = True
_REGEX = "a.*"  # If None randomly generated
_BUG = "abcah"  # If None randomly generated
#_REGEX = None  # If None randomly generated
#_BUG = None  # If None randomly generated
reportfile = "testing\\logs\\dummy"


system = s.system(_MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile)

# Init fuzzer
#fuzzer = class_nn.nn_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # Neural network based fuzzer
fuzzer = lstar.lstar_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # L* based fuzzer
fuzzer.start()





