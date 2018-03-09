from matplotlib import pyplot as plt

def make_plot(x, y):
    plt.plot(x, y)
    plt.ylabel("Total Loss")
    plt.xlabel("Training Steps")
    plt.show()
    return 0