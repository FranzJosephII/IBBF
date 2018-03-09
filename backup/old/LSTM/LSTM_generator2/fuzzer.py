import sys
#import old.LSTM_generator2.fuzzernetwork_new as fuzzernetwork
import old.LSTM_generator2.fuzzernetwork as fuzzernetwork
import old.LSTM_generator2.generator as g
import old.LSTM_generator2.visualize as v

_DEBUG = True
_DETAILS = True
_BATCH_SIZE = 100
_EPOCHS = 20


fuzzer = fuzzernetwork.fuzzer()
#print("1 -> " + g.calcstring(fuzzer.compute([1, 1, 1, 1, 1])))
#sys.exit()

losses = []
accuracy = []
precision = []
recall = []
truenegativerate = []

for e in range(_EPOCHS):
    eval_pos = []
    eval_neg = []
    batch_loss = 0
    for bs in range(_BATCH_SIZE):
        batch_loss += fuzzer.train(([[1, 1, 1, 1, 1]], [g.getPositiveSample()]))
        batch_loss += fuzzer.train(([[0, 0, 0, 0, 0]], [g.getNegativeSample()]))
        eval_pos.append(fuzzer.compute([1, 1, 1, 1, 1]))
        eval_neg.append(fuzzer.compute([0, 0, 0, 0, 0]))
    losses.append(batch_loss)
    if _DETAILS:
        acc, pre, rec, tnr = fuzzer.evaluate(eval_pos, eval_neg)
        accuracy.append(acc)
        precision.append(pre)
        recall.append(rec)
        truenegativerate.append(tnr)
    if _DEBUG:
        print("0 -> " + g.calcstring(fuzzer.compute([0, 0, 0, 0, 0])))
        print("1 -> " + g.calcstring(fuzzer.compute([1, 1, 1, 1, 1])))
v.print_loss(losses, _BATCH_SIZE, _EPOCHS)
if _DETAILS:
    v.print_details(accuracy, precision, recall, truenegativerate, _BATCH_SIZE, _EPOCHS)

"""
def simple_opt_fuzzing():
    fuzzer = fuzzernetwork.fuzzer()

    if _DEBUG: ctr = 0

    accuracy = []
    precision = []
    recall = []
    truenegativerate = []
    losses = [0] * (_STEPS)
    num_samples = []
    for s in range(_STEPS):

        eval_pos = []
        eval_neg = []

        # Train fuzzer with samples
        total_loss = 0
        for i in range(_BATCH_SIZE):
            loss = fuzzer.train(([[0.99], [0.01]], [g.getPositiveSample(), g.getNegativeSample()]))
            losses[s] += loss
            eval_pos.append(fuzzer.compute([0.99]))
            eval_neg.append(fuzzer.compute([0.01]))
        num_samples.append((s + 1) * _BATCH_SIZE)
        acc, pre, rec, tnr = fuzzer.evaluate(eval_pos, eval_neg)
        accuracy.append(acc)
        precision.append(pre)
        recall.append(rec)
        truenegativerate.append(tnr)

        """"""
        # Fuzz system
        fuzzing_samples = []
        for i in range(_BATCH_SIZE*2):
            fuzzing_samples.append(fuzzer.compute(g.getFuzzerInput()))
        """"""

        # Debug Output
        if _DEBUG:
            print("##################################")
            print("0.01 --> " + str(g.calcstring(fuzzer.compute([0.01])[0])))
            print("0.5  --> " + str(g.calcstring(fuzzer.compute([0.4])[0])))
            print("0.99 --> " + str(g.calcstring(fuzzer.compute([0.99])[0])))

    #print(num_samples)
    #print(losses)
    v.make_plot(num_samples, accuracy, precision, recall, truenegativerate)


#simple_opt_fuzzing()
"""