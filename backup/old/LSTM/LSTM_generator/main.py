from old.LSTM_generator import LSTM_module as lstm
from old.LSTM_generator import visualize as v

_BATCH_SIZE = 100
_STEPS = 500

lstm = lstm.LSTM()
losses = []
num_samples = []
for i in range(_STEPS):
    loss = lstm.train(_BATCH_SIZE)
    print("Step: " + str(i+1) + ", Loss: " + str(loss))
    losses.append(loss)
    num_samples.append((i+1)*_BATCH_SIZE)
    print("1 --> " + str(lstm.compute([1])))
v.make_plot(num_samples, losses)




