import os, sys
import datetime

#           1       2           3               4           5
_REGEX = [  "a.*",  ".*a.*",    ".*[a-m].*",    ".*aa.*",   ".*a.{2}a.*"]
_BUG = [    "abcd", "abcd",     "abcd",         "zaaz",     "azza"]
_MAX_LEN = [5,      5,          5,             5,          5]

testcases = len(_REGEX)
run = 0
while(42):
    run += 1
    for testcase in range(testcases):

        # set test parameter
        MAX_LEN = _MAX_LEN[testcase]
        REGEX = _REGEX[testcase]
        BUG = _BUG[testcase]

        # set path of testcase once and add test overview
        name = str(testcase + 1)
        path = "logs\\" + name
        try:
            os.makedirs(path)
            f = open(path + "\\test_summary", 'w')
            f.write("Regex:\t" + REGEX + "\nBug:\t" + BUG + "\nLength: " + str(MAX_LEN))
            f.close()
        except:
            pass

        ##########
        # lstar #
        ##########
        subpath = path + "\\lstar_fuzzer\\"
        try:
            os.makedirs(subpath)
        except:
            pass

        # Call Test
        # Define report file
        reportfile = subpath + "run_" + str(run)
        # Execute testcase
        while (not os.path.isfile(reportfile)):
            # define process parameter
            params = "python test_main.py " + REGEX + " " + BUG + " " + str(
                MAX_LEN) + " " + reportfile + " lstar"

            # Start new process with parameter
            print("Starting lstar-run " + str(run) + " of testcase " + str(testcase + 1) + "  (" + str(
                datetime.datetime.now()) + ")")
            os.system(params)

        ##########
        # neural #
        ##########
        subpath = path + "\\neural_network_fuzzer\\"
        try:
            os.makedirs(subpath)
        except:
            pass

        # Call Test
        # Define report file
        reportfile = subpath + "run_" + str(run)
        # Execute testcase
        while (not os.path.isfile(reportfile)):
            # define process parameter
            params = "python test_main.py " + REGEX + " " + BUG + " " + str(
                MAX_LEN) + " " + reportfile + " neural"

            # Start new process with parameter
            print("Starting neural-run " + str(run) + " of testcase " + str(testcase + 1) + "  (" + str(
                datetime.datetime.now()) + ")")
            os.system(params)