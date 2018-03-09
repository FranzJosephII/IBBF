from matplotlib import pyplot as plt

def make_plot(x, acc, pre, rec, tnr):
    plt.plot(x, acc, label="Accuracy")
    plt.plot(x, pre, label="Precision")
    plt.plot(x, rec, label="Recall")
    plt.plot(x, tnr, label="True Negative Rate")
    plt.legend()
    plt.xlabel("Training Steps")
    plt.xlim(xmin=x[0])
    plt.ylim(ymin=0)
    plt.show()
    return 0

def print_loss(y, batch, epoch):
    x = []
    for e in range(epoch): x.append((e+1)*batch)
    plt.plot(x, y)
    plt.xlabel("Training Steps")
    plt.ylabel("Total Loss")
    plt.xlim(xmin=x[0])
    #plt.ylim(ymin=0)

    plt.show()
    return 0

def print_details(acc, pre, rec, tnr, batch, epoch):
    x = []
    for e in range(epoch): x.append((e + 1) * batch)
    plt.plot(x, acc, label="Accuracy")
    #plt.plot(x, pre, label="Precision")
    #plt.plot(x, rec, label="Recall")
    #plt.plot(x, tnr, label="True Negative Rate")
    plt.legend()
    plt.xlabel("Training Steps")
    plt.xlim(xmin=x[0])
    plt.ylim(ymin=0)
    plt.show()
    return 0