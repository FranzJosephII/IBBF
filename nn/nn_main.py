import nn.nn_model as classic
import nn.nn_model as neuralnetwork
import nn.nn_interface as interface
import tensorflow as tf
import os
import datetime
import sys

class nn_fuzzer:
    """
    Implementation of a GAN which fuzzes the given system
    """
    def __init__(self, system, _MAXLENGTH, _DEBUG, reportfile):

        self._DEBUG = _DEBUG
        self._BATCH_SIZE = 100
        self._MAXLENGTH = _MAXLENGTH * 5

        self.summaries = []

        self.sys = system
        self.itf = interface.nn_interface(system, self._MAXLENGTH)
        self.nn = neuralnetwork.classificator(self._MAXLENGTH, self.itf, reportfile)

        self.accuracy = []
        self.epoch_acc = [-4, -3, -2, -1, 0]
        self.strikes = 0

        self.false_positives = []

    def start(self):
        # Initial training phase
        if self._DEBUG: print("Start Training ...")
        while(float(self.epoch_acc[-1]) < 1. and self.epoch_acc[len(self.epoch_acc)-1] > self.epoch_acc[len(self.epoch_acc)-5]):
            self.train(None)


        # Start Fuzzing
        if self._DEBUG: print("\nQueries used during training: " + str(self.sys.queries) + "\n\nStart Fuzzing ...")
        while(42):
            fuzz_sample = self.itf.get_random_string()
            # if calculated sample acceptance is below average or the sample is a known false positive skip fuzzing
            if self.nn.calculate([self.itf.calcvector(fuzz_sample)]) < 0.5 or fuzz_sample in self.false_positives:
                continue
            # if the sample is a false positive add it to a list
            if self.itf.membership_query(fuzz_sample) == 0:
                if self._DEBUG: print("False Positive: " + fuzz_sample)
                self.false_positives.append(fuzz_sample)
                continue


    def train(self, input):
        self.strikes = 0

        if input == None:
            while (42 == 42):
                data = self.itf.get_training_batch(self._BATCH_SIZE)
                for i in range(10): self.summaries.append(self.nn.train(data))
                acc = self.nn.evaluate(None)
                self.accuracy.append(acc)
                if self.evaluate_learning_rate():
                    break
        else:
            data = input
            for i in range(10): self.summaries.append(self.nn.train(data))



    def evaluate_learning_rate(self):

        if len(self.accuracy) < 10:
            return False

        difference = 0
        pos = len(self.accuracy)-1
        for i in range(9):
            difference += (self.accuracy[pos-i]-self.accuracy[pos-(i+1)])

        if difference <= 0:
            self.strikes += 1

        if self.strikes > 10:
            self.epoch_acc.append(self.accuracy[len(self.accuracy)-1])
            if self._DEBUG: print("Current Accuracy: " + str(self.accuracy[len(self.accuracy)-1]) + "\nQueries used so far: " + str(self.sys.queries))
            return True
        return False


    def print_loss(self):
        """
        Creates a tensorboard instance from the logged data
        """
        now = datetime.datetime.now()
        path = "logs\\" + str(now.day) + "." + str(now.month) + "." + str(now.year) + "." + str(now.hour) + "." + str(now.minute) + "." + str(now.second)

        writer = tf.summary.FileWriter(path, graph=tf.get_default_graph())
        for i in range(len(self.summaries)):
            writer.add_summary(self.summaries[i], (i+1)*self._BATCH_SIZE)

        os.system("tensorboard --logdir=" + path)
