import regular.regular_model as model
import regular.input_parser as ip
import regular.regular_interface as iface
import tensorflow as tf
import os
import datetime
import random

class regular_nn_fuzzer:

    def __init__(self, system, _BATCH_SIZE, _MAXLENGTH, _DEBUG):

        self._DEBUG = _DEBUG
        self._BATCH_SIZE = _BATCH_SIZE
        self._MAXLENGTH = _MAXLENGTH * 5

        self.summaries = []

        ip._MAXLENGTH = self._MAXLENGTH
        self.nn = model.regular_nn(self._MAXLENGTH)

        self.interface = iface.regular_interface(system)

    def train(self, _STEPS):

        loss = 0
        ctr = 0
        for s in range(_STEPS):

            # Train fuzzer with samples
            # First generate n/2 positive samples
            #generated_samples = []
            #for i in range(int(self._BATCH_SIZE / 2)):
            #    generated_samples.append(self.nn.compute([random.uniform(0.5, 0.99)]))
            # Then send them to the interface to get training batch
            #self.interface.fuzz(generated_samples)
            # Train network and remember summary
            #summary = self.nn.train((batch_y, batch_x))
            #self.summaries.append(summary)
            for i in range(self._BATCH_SIZE):
                summary = self.nn.train(([[0.01], [0.99]], [ip.calcvector(self.interface.get_negative_sample()), ip.calcvector(self.interface.get_positive_sample())]))
                self.interface.fuzz(self.nn.compute([0.99]))
                self.summaries.append(summary)

            # Debug Output
            if self._DEBUG:
                if ctr % 10 == 0:
                    print("##################################")
                    print("0.01 --> " + str(ip.calcstring(self.nn.compute([0.01])[0])))
                    print("0.5  --> " + str(ip.calcstring(self.nn.compute([0.4])[0])))
                    print("0.99 --> " + str(ip.calcstring(self.nn.compute([0.99])[0])))
                ctr += 1

    def print_loss(self):

        now = datetime.datetime.now()
        path = "logs\\regular\\" + str(now.day) + "." + str(now.month) + "." + str(now.year) + "." + str(now.hour) + "." + str(now.minute) + "." + str(now.second)

        writer = tf.summary.FileWriter(path, graph=tf.get_default_graph())
        for i in range(len(self.summaries)):
            writer.add_summary(self.summaries[i], i*10)

        os.system("tensorboard --logdir=" + path)
