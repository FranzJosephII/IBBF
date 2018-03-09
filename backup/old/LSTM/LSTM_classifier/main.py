from backup.old.LSTM.LSTM_classifier import LSTM_module as lstm
from backup.old.LSTM.LSTM_classifier import visualize as v

_BATCH_SIZE = 1000
_STEPS = 10

lstm = lstm.LSTM()
losses = []
num_samples = []
for i in range(_STEPS):
    loss = lstm.train(_BATCH_SIZE)
    print("Step: " + str(i+1) + ", Loss: " + str(loss))
    losses.append(loss)
    num_samples.append((i+1)*_BATCH_SIZE)
    print("gabadkkkkk --> " + str(lstm.compute("gabadkkkkk")))
v.make_plot(num_samples, losses)




