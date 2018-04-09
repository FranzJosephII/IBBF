from matplotlib import pyplot as plt

batch_size = 40
test_amount = 5

##################
# global summary #
##################

lstar_summary = []
neural_summary = []

lstar_data_full = []
neural_data_full = []

report_summary = "\t| lstar\t\t| neural\t|\n-----------------------------\n"

for j in range(test_amount):
    testcase = str(j+1)

    # read data
    lstar_directory = "logs\\" + testcase + "\\lstar_fuzzer\\"
    neural_directory = "logs\\" + testcase + "\\neural_network_fuzzer\\"

    lstar_data = []
    neural_data = []

    for i in range(batch_size):
        lstar_file = lstar_directory + "run_" + str(i+1)
        neural_file = neural_directory + "run_" + str(i+1)

        data = []
        f = open(lstar_file, 'r')
        for line in f.readlines():
            line = line.strip()
            line = line.split(';')
            data.append(line)
        lstar_data.append(data)
        f.close()

        data = []
        f = open(neural_file, 'r')
        for line in f.readlines():
            line = line.strip()
            line = line.split(';')
            data.append(line)
        neural_data.append(data)
        f.close()

    lstar_data_full.append(lstar_data)
    neural_data_full.append(neural_data)

    # lstar
    sum = 0
    pos = 0
    for test in lstar_data:
        if test[-1][1] == 'FOUND':
            sum += int(test[-1][0])
            pos += 1
    if pos != 0:
        lstar_summary.append(int(sum / pos))
    else:
        lstar_summary.append("na")

    # neural
    sum = 0
    pos = 0
    for test in neural_data:
        if test[-1][1] == 'FOUND':
            sum += int(test[-1][0])
            pos += 1
    if pos != 0:
        neural_summary.append(int(sum / pos))
    else:
        neural_summary.append("na")

    # parse line
    line = str(j+1) + "\t| "

    if len(str(lstar_summary[j])) > 5:
        line += str(lstar_summary[j]) + "\t| "
    else:
        line += str(lstar_summary[j]) + "\t\t| "

    if len(str(neural_summary[j])) > 5:
        line += str(neural_summary[j]) + "\t|"
    else:
        line += str(neural_summary[j]) + "\t\t|"

    report_summary += line + "\n"




#############################
# global testcase lern-rate #
#############################

report_learnamount_neural = "NEURAL_NETWORK-LEARNING-RATES:\n\t| Samples\t| Accuracy\t| Standardabweichung\t\n------------------------------------------------"
i = 0
for testcase in neural_data_full:
    i += 1
    learnamount = 0
    accuracy = 0
    varianz = 0
    failed = 0
    for run in testcase:
        if len(run) > 1:
            learnamount += float(run[-2][0])
            accuracy += float(run[-2][1])
        else:
            failed += 1
    learnamount /= (batch_size - failed)
    accuracy /= (batch_size - failed)
    accuracy = "{0:.4f}".format(accuracy)

    failed = 0
    for run in testcase:
        if len(run) > 1:
            varianz += (float(run[-2][0]) - learnamount)**2
        else:
            failed += 1
    varianz /= (batch_size - failed)

    report_learnamount_neural += "\n" + str(i) + "\t| " + str(int(learnamount)) + "\t\t| " + str(accuracy) + "\t| " + str(int(varianz**0.5)) + "\t"


report_learnamount_lstar = "LSTAR-LEARNING-RATES:\n\t| Samples\t| Accuracy\t| Standardabweichung\t\n------------------------------------------------"
i = 0
for testcase in lstar_data_full:
    i += 1
    learnamount = 0
    accuracy = 0
    varianz = 0
    for run in testcase:
        learnamount += float(run[-2][0])
        accuracy += float(run[-2][1])
    learnamount /= batch_size
    accuracy /= batch_size

    for run in testcase:
        varianz += (float(run[-2][0]) - learnamount)**2
    varianz /= batch_size

    report_learnamount_lstar += "\n" + str(i) + "\t| " + str(int(learnamount)) + "\t\t| " + str(accuracy) + "\t\t| " + str(int(varianz**0.5)) + "\t"


#####################
# write report      #
#####################

# write report to file:
f = open("logs\\global_report", 'w')
f.write(report_summary)
f.write("\n\n" + report_learnamount_lstar)
f.write("\n\n" + report_learnamount_neural)
f.close()


#####################
# make lstar graphs #
#####################

for j in range(test_amount):
    x_sum = []
    y_sum = []
    for i in range(batch_size):
        x = [0]
        y = [0]
        for data in lstar_data_full[j][i]:
            if not (data[1] == "START" or data[1] == "FOUND" or data[1] == "FAILED"):
                x.append(int(data[0]))
                y.append(float(data[1]))

        if len(x) > 2:
            diff = x[1]-(x[2]-x[1])
            for v in range(1, len(x)):
                x[v] = x[v] - diff
        else:
            diff = 10000
            for v in range(1, len(x)):
                x[v] = x[v] - diff

        x_sum.append(x)
        y_sum.append(y)

        plt.plot(x, y)
        plt.ylabel("Accuracy")
        plt.xlabel("Used Samples")
        plt.savefig("logs\\" + str(j+1) + "\\lstar_fuzzer\\run" + str(i+1) + ".png")
        plt.close()

    for k in range(batch_size):
        plt.plot(x_sum[k], y_sum[k])
    plt.ylabel("Accuracy")
    plt.xlabel("Used Samples")
    plt.savefig("logs\\" + str(j + 1) + "\\lstar.png")
    plt.close()

######################
# make neural graphs #
######################
for j in range(test_amount):
    x_sum = []
    y_sum = []
    for i in range(batch_size):
        x = [0]
        y = [0]
        for data in neural_data_full[j][i]:
            if not (data[1] == "START" or data[1] == "FOUND" or data[1] == "FAILED"):
                x.append(int(data[0]))
                y.append(float(data[1]))

        # Clean data:
        if len(x) > 2:
            diff = x[1]-(x[2]-x[1])
            for v in range(1, len(x)):
                x[v] = x[v] - diff

        x_sum.append(x)
        y_sum.append(y)

        plt.plot(x, y)
        plt.ylabel("Accuracy")
        plt.xlabel("Used Samples")
        plt.savefig("logs\\" + str(j+1) + "\\neural_network_fuzzer\\run" + str(i+1) + ".png")
        plt.close()

    for k in range(batch_size):
        plt.plot(x_sum[k], y_sum[k])
    plt.ylabel("Accuracy")
    plt.xlabel("Used Samples")
    plt.savefig("logs\\" + str(j + 1) + "\\neural_network.png")
    plt.close()

