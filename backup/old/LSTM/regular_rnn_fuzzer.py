from LSTM import regular_rnn_generator as g
from LSTM import regular_rnn_fuzzernetwork as fuzzernetwork
from LSTM import regular_rnn_visualize as v

#http://monik.in/a-noobs-guide-to-implementing-rnn-lstm-using-tensorflow/

_BATCH_SIZE = 100
_STEPS = 100
losses = []
num_samples = []

test0 = []
test5 = []
test1 = []
for i in range(50):
    test0.append(0)
    test5.append(0.5)
    test1.append(1)

fuzzer = fuzzernetwork.fuzzer()
#print("0   --> " + str(g.calcvector(fuzzer.compute(test0))))
#print("0.5 --> " + str(g.calcvector(fuzzer.compute(test5))))
#print("1   --> " + str(g.calcvector(fuzzer.compute(test1))))
for i in range(_STEPS):
    training_dataset = g.gen_epochs(_BATCH_SIZE, 10*5, 1) # static parameters (should be removed)
    loss = fuzzer.train(training_dataset)
    #print(training_dataset)
    print("0   --> " + fuzzer.compute(test0))
    print("0.5 --> " + fuzzer.compute(test5))
    print("1   --> " + fuzzer.compute(test1))
    #print("1   --> " + str(g.calcvector(fuzzer.compute(test1))))
    print("Step: " + str(i+1) + ", Loss: " + str(loss))
    losses.append(loss)
    num_samples.append((i+1)*_BATCH_SIZE)


v.make_plot(num_samples, losses)




