import os, sys
import tensorflow as tf
import random
import old.LSTM_generator2.generator as g

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class fuzzer:

    def __init__(self):
        """
        Defines the structure and calculation model of the fuzzing network
        """
        # Create the model
        l = 3
        self.x = tf.placeholder(tf.float32, [1, 5])
        self.W = tf.Variable(tf.random_uniform([5, 10], -0.99, 0.99))
        self.b = tf.Variable(tf.zeros([10]))
        self.y = tf.placeholder(tf.float32, [1, l, 5])

        self.input = self.x
        self.labels = tf.unstack(self.y)[0]

        self.model = tf.nn.sigmoid(tf.matmul(self.input, self.W) + self.b)

        self.outputs = []

        for s in range(l):
            self.output, self.state = tf.split(self.model, [5, 5], 1)
            self.outputs.append(self.output)
            self.input = self.state

        y_series = tf.unstack(self.y, num=3, axis=1)

        losses = [tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels) for logits, labels in zip(self.outputs, y_series)]
        self.total_loss = tf.reduce_mean(losses)
        self.train_step = tf.train.AdagradOptimizer(0.3).minimize(self.total_loss)


        # Define loss and optimizer
        #squared_deltas = tf.square(self.outputs[2] - self.labels[2])
        #self.total_loss = tf.reduce_sum(squared_deltas)
        #optimizer = tf.train.AdagradOptimizer(0.1)
        #self.train_step = optimizer.minimize(self.total_loss)


        # Create Session
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        #i, l, o = self.sess.run([self.input, self.outputs], feed_dict={self.x: [[1, 1, 1, 1, 1]], self.y: [g.getPositiveSample()]})
        #print("Input: " + str(i) + "\n#####")
        #print("Labels: " + str(l) + "\n#####")
        #print("outputs: " + str(o) + "\n#####")


    def train(self, data):
        
        #Trains the network with the given dataset
        
        batch_x, batch_y = data
        #print(batch_x)
        #print(batch_y)
        loss, placeholder = self.sess.run([self.total_loss, self.train_step], feed_dict={self.x: batch_x, self.y: batch_y})
        return loss

    def compute(self, vector):
        
        #Computes an output from a given float value
        
        # Compute output from a single input vector
        batch_x = [vector]
        return self.sess.run(self.outputs, feed_dict={self.x: batch_x})

    def evaluate(self, pos, neg):
        fp = 0
        fn = 0
        tp = 0
        tn = 0
        pre = 0
        rec = 0
        tnr = 0

        # Test positive samples
        for a in pos:
            #print(a)
            answer = g.calcstring(a)
            if g.testSample(answer):
                tp += 1
            else:
                fp += 1

        # Test negative samples
        for a in neg:
            answer = g.calcstring(a)
            if g.testSample(answer):
                fn += 1
            else:
                tn += 1

        acc = (tp + tn)/(fp + fn + tp + tn)
        if tp + fp is not 0: pre = tp / (tp + fp)
        if tp + fn is not 0: rec = tp / (tp + fn)
        if tn + fp is not 0: tnr = tn / (tn + fp)

        return acc, pre, rec, tnr
