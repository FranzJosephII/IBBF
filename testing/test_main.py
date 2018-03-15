import sys
import nn.nn_main as class_nn
import lstar.lstar_fuzzer as lstar
import system.regular as regular
import system.contextfree as contextfree
import system.contextsensitive as contextsensitive

_DEBUG = False

_REGEX = sys.argv[1]
_BUG = sys.argv[2]
_MAXLENGTH = int(sys.argv[3])
reportfile = sys.argv[4]
method = sys.argv[5]

system = regular.system(_MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile)
#system = contextfree.system(_MAXLENGTH, _BUG, _DEBUG, reportfile)
#system = contextsensitive.system(_MAXLENGTH, _BUG, _DEBUG, reportfile)

if method == "lstar":
    fuzzer = lstar.lstar_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)
    fuzzer.start()

elif method == "neural":
    fuzzer = class_nn.nn_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)
    fuzzer.start()

else:
    print("ERROR: Method not found")
    sys.exit()

