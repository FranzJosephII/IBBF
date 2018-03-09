from old.LSTM_Test import LSTM_module as lstm
from old.LSTM_Test import visualize as v

_BATCH_SIZE = 10
_STEPS = 50

lstm = lstm.LSTM()
losses = []
num_samples = []
for i in range(_STEPS):
    loss = lstm.train(_BATCH_SIZE)
    #print("abcdefghij" + " --> " + lstm.compute("abcdefghij") + " with a total loss of " + str(loss))
    print("Step: " + str(i+1) + ", Loss: " + str(loss))
    losses.append(loss)
    num_samples.append((i+1)*_BATCH_SIZE)
v.make_plot(num_samples, losses)




