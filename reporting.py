from matplotlib import pyplot as plt

batch_size = 19
test_amount = 5



##################
# global summary #
##################

monkey_summary = []
lstar_summary = []
neural_summary = []

monkey_data_full = []
lstar_data_full = []
neural_data_full = []

report = "\t| monkey\t| lstar\t\t| neural\t|\n-----------------------------------------\n"

for j in range(test_amount):
    testcase = str(j+1)

    # read data
    monkey_directory = "logs\\" + testcase + "\\monkey_fuzzer\\"
    lstar_directory = "logs\\" + testcase + "\\lstar_fuzzer\\"
    neural_directory = "logs\\" + testcase + "\\neural_network_fuzzer\\"

    monkey_data = []
    lstar_data = []
    neural_data = []

    for i in range(batch_size):
        monkey_file = monkey_directory + "run_" + str(i+1)
        lstar_file = lstar_directory + "run_" + str(i+1)
        neural_file = neural_directory + "run_" + str(i+1)

        data = []
        f = open(monkey_file, 'r')
        for line in f.readlines():
            line = line.strip()
            line = line.split(';')
            data.append(line)
        monkey_data.append(data)
        f.close()

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

    monkey_data_full.append(monkey_data)
    lstar_data_full.append(lstar_data)
    neural_data_full.append(neural_data)

    # monkey
    sum = 0
    pos = 0
    for test in monkey_data:
        if test[-1][1] == 'FOUND':
            sum += int(test[-1][0])
            pos += 1
    if pos != 0:
        monkey_summary.append(int(sum / pos))
    else:
        monkey_summary.append("na")

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
    if len(str(monkey_summary[j])) > 5:
        line += str(monkey_summary[j]) + "\t| "
    else:
        line += str(monkey_summary[j]) + "\t\t| "

    if len(str(lstar_summary[j])) > 5:
        line += str(lstar_summary[j]) + "\t| "
    else:
        line += str(lstar_summary[j]) + "\t\t| "

    if len(str(neural_summary[j])) > 5:
        line += str(neural_summary[j]) + "\t|"
    else:
        line += str(neural_summary[j]) + "\t\t|"

    report += line + "\n"


report += "\n\n\t| monkey\t| lstar\t\t\t\t\t| neural\t\t\t\t|\n-----------------------------------------------------------------\n"
for j in range(test_amount):
    if lstar_summary[j] != "na" and neural_summary[j] != "na":
        report += str(j+1) + "\t| 1\t\t\t| " + str(lstar_summary[j]/monkey_summary[j]) + "\t| " + str(neural_summary[j]/monkey_summary[j]) + "\t|\n"
    elif lstar_summary[j] == "na" and neural_summary[j] != "na":
        report += str(j + 1) + "\t| 1\t\t\t| na\t\t\t\t\t| " + str(neural_summary[j] / monkey_summary[j]) + "\t|\n"
    elif lstar_summary[j] != "na" and neural_summary[j] == "na":
        report += str(j+1) + "\t| 1\t\t\t| " + str(lstar_summary[j]/monkey_summary[j]) + "\t| na\t\t\t\t\t|\n"
    else:
        report += str(j+1) + "\t| 1\t\t\t| na\t\t\t\t\t| na\t\t\t\t\t|\n"

# write report to file:
f = open("logs\\global_report", 'w')
f.write(report)
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
        #if len(y) > 0:
        #    y[0] = 0

        if len(x) > 2:
            diff = x[1]-(x[2]-x[1])
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

        #print(x)
        # Clean data:
        if len(x) > 2:
            diff = x[1]-(x[2]-x[1])
            for v in range(1, len(x)):
                x[v] = x[v] - diff
        #print(x)

        #sys.exit()

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

