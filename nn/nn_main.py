import nn.nn_model as classic
import nn.nn_model as neuralnetwork
import nn.nn_interface as interface
import tensorflow as tf
import os
import datetime
import sys

class nn_fuzzer:
    """
    Implementation of a neural-network based black-box-fuzzer
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

    def start(self):
        """
        Starts the execution of the neural network. First trains the network and then starts fuzzing the system with
        calculated fuzzing samples
        """
        # Initial training phase
        if self._DEBUG: print("Start Training ...")
        self.train()

        # Start Fuzzing
        if self._DEBUG: print("\nQueries used during training: " + str(self.sys.queries) + "\n\nStart Fuzzing ...")
        while(42):
            print("New Test phase")
            # generate Batch
            fuzz_sample_batch = []
            fuzz_vector_batch = []
            for i in range(1000000):
                fuzz_sample = self.itf.get_random_string()
                fuzz_sample_batch.append(fuzz_sample)
                fuzz_vector_batch.append(self.itf.calcvector(fuzz_sample))

            # test samples against network
            calculated_labels = self.nn.calculate(fuzz_vector_batch)

            # query the positive samples
            for i in range(len(calculated_labels)):
                if calculated_labels[i] > 0.5:
                    self.itf.membership_query(fuzz_sample_batch[i])


    def train(self):
        """
        Trains the network until the accuracy is good enough
        """

        while (42 == 42):
            data = self.itf.get_training_batch(self._BATCH_SIZE)
            losses = []
            while(42):
                summary, loss = self.nn.train(data)
                self.summaries.append(summary)
                losses.append(loss)
                if len(losses) > 20:
                    if losses[-1] / losses[-2] > 0.99:
                        break
            acc = self.nn.evaluate(None)
            self.accuracy.append(acc)
            if self.evaluate_learning_rate():
                break

    def evaluate_learning_rate(self):
        """
        Evaluates wheter the training phase should be stopped or not depending on the current accuracy of the model
        :return: bool
        """

        if self._DEBUG: print("Accuracy: " + str(self.accuracy[-1]))

        if self.accuracy[-1] > 0.999:
            return True

        if len(self.accuracy) < 20:
            return False

        diff = self.accuracy[-1] - self.accuracy[-20]

        if (diff < 0.00001 and diff > -0.00001 and diff != 0):
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
