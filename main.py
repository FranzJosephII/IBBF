import nn.nn_main as class_nn
import lstar.lstar_fuzzer as lstar
import system.regular as regular
import system.contextfree as contextfree
import system.contextsensitive as contextsensitive


_MAXLENGTH = 5  # Characters
_DEBUG = True
_REGEX = "a.*"  # If None randomly generated
_BUG = "aajjz"  # If None randomly generated
#_REGEX = None  # If None randomly generated
#_BUG = None  # If None randomly generated
reportfile = "testing\\logs\\dummy"


#system = regular.system(_MAXLENGTH, _REGEX, _BUG, _DEBUG, reportfile)
#system = contextfree.system(_MAXLENGTH, _BUG, _DEBUG, reportfile)
system = contextsensitive.system(_MAXLENGTH, _BUG, _DEBUG, reportfile)



# Init fuzzer
fuzzer = class_nn.nn_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # Neural network based fuzzer
#fuzzer = lstar.lstar_fuzzer(system, _MAXLENGTH, _DEBUG, reportfile)      # L* based fuzzer
fuzzer.start()





