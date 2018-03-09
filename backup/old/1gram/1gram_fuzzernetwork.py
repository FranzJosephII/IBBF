import os

import old_generator as g
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class fuzzer:

    def __init__(self):
        """
        Defines the structure and calculation model of the fuzzing network
        """
        # Create the model
        self.x = tf.placeholder(tf.float32, [None, 1])
        self.W_1 = tf.Variable(tf.random_uniform([1, 13], -1, 1))
        self.W_2 = tf.Variable(tf.random_uniform([13, 26], -0.27, 0.27))
        self.model = tf.sigmoid(tf.matmul(tf.nn.sigmoid(tf.matmul(self.x, self.W_1)), self.W_2))

        # Define loss and optimizer
        self.y = tf.placeholder(tf.float32, [None, 26])
        squared_deltas = tf.square(self.model - self.y)
        loss = tf.reduce_sum(squared_deltas)
        optimizer = tf.train.GradientDescentOptimizer(0.3)
        self.train_step = optimizer.minimize(loss)

        # Create Session
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

    def train(self, data):
        """
        Trains the network with the given dataset
        """
        batch_x, batch_y = data
        self.sess.run(self.train_step, feed_dict={self.x: batch_x, self.y: batch_y})

    def compute(self, vector):
        """
        Computes an output from a given float value
        """
        # Compute output from a single input vector
        batch_x = [vector]
        return self.sess.run(self.model, feed_dict={self.x: batch_x})

    def evaluate(self, size):
        """
        Evaluates the model according to whether the generated samples
        from input range 0.45 to 0.55 are in the correct spectrum.
        Returns accuracy of generated samples.
        """
        # evaluates the model
        correct_answers = 0
        for i in range(size):
            answer = self.sess.run(self.model, feed_dict={self.x: [g.getFuzzerInput()]})[0][0]
            if (answer < 0.6 and answer > 0.4):
                correct_answers += 1
        return correct_answers / size