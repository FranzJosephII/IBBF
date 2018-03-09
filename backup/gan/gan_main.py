import gan.gan_model as model
import gan.gan_interface as interface
import tensorflow as tf
import os
import datetime

class gan_nn_fuzzer:
    """
    Implementation of a GAN which fuzzes the given system
    """
    def __init__(self, system, _MAXLENGTH):

        self._DEBUG = 1
        self._BATCH_SIZE = 100
        self._MAXLENGTH = _MAXLENGTH * 5

        self.summaries = []

        self.itf = interface.gan_interface(system, self._MAXLENGTH)
        self.nn = model.GAN(self._MAXLENGTH, self.itf)

    def start(self):
        self.train(100000)
        """
        while (42):
            self.itf.add_samples(100000)
            print("##########\nNEW EPOCH\n##########")

            for i in range(1000):
                self.nn.train(self.itf.get_training_batch(1000))

                #sample = self.itf.calcstring(self.nn.getSample()[0])
                #if self.itf.match((sample)):
                #    print("Output: TRUE \t " + sample)
                #else:
                #    print("Output: FALSE \t " + sample)

            g_acc, d_acc = self.nn.evaluate()
            print("Generator Accuracy: " + str(g_acc) + "\nDiscriminator Accuracy: " + str(d_acc))
            break
        """

    def train(self, _STEPS):
        """
        Trains the network the given amount of steps with a batch of training samples
        """

        loss = 0
        ctr = 0

        for s in range(_STEPS):

            # Get training samples, train and remember training summary
            training_batch = self.itf.get_training_batch(self._BATCH_SIZE)
            self.summaries.append(self.nn.train(training_batch))

            # Debug Output
            if self._DEBUG:
                if ctr % 10 == 0:
                    sample = self.itf.calcstring(self.nn.getSample()[0])
                    if self.itf.match((sample)):
                        print("Output: TRUE \t " + sample)
                    else:
                        print("Output: FALSE \t " + sample)
                ctr += 1

        #batch = self.itf.get_training_batch(100000)
        #for i in range(10): self.nn.train(self.itf.get_training_batch(100000))


        print("\n")
        for i in range(20):
            print("Sample: " + self.itf.calcstring(self.nn.getSample()[0]))
            print(self.itf.match(self.itf.calcstring(self.nn.getSample()[0])))
        print("\n")


        if self._DEBUG:
            print("double values: " + str(self.itf.double_ctr))
            print("query values: " + str(len(self.itf.old_queries)))
            print("positive values: " + str(len(self.itf.positive_samples)))
            self.nn.evaluate()

        g_acc, d_acc = self.nn.evaluate()
        print("Generator Accuracy: " + str(g_acc) + "\nDiscriminator Accuracy: " + str(d_acc))


    def print_loss(self):
        """
        Creates a tensorboard instance from the logged data
        """
        now = datetime.datetime.now()
        path = "logs\\gan\\" + str(now.day) + "." + str(now.month) + "." + str(now.year) + "." + str(now.hour) + "." + str(now.minute) + "." + str(now.second)

        writer = tf.summary.FileWriter(path, graph=tf.get_default_graph())
        for i in range(len(self.summaries)):
            writer.add_summary(self.summaries[i], i*10)

        os.system("tensorboard --logdir=" + path)
