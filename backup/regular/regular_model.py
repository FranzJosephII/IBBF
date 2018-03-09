import os
import tensorflow as tf
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class regular_nn:

    def __init__(self, max_input):
        """
        Defines the structure and calculation model of the fuzzing network
        """
        # Calculate how much Nodes for layers are needed
        output_nodes = max_input
        hidden_nodes = int(math.sqrt(output_nodes))
        hidden_init_param = 1/math.sqrt(hidden_nodes)

        # Create the model
        self.x = tf.placeholder(tf.float32, [None, 1])
        self.W_1 = tf.Variable(tf.random_uniform([1, hidden_nodes], -0.99, 0.99))
        self.W_2 = tf.Variable(tf.random_uniform([hidden_nodes, output_nodes], -hidden_init_param, hidden_init_param))
        self.model = tf.sigmoid(tf.matmul(tf.nn.sigmoid(tf.matmul(self.x, self.W_1)), self.W_2))

        # Define loss and optimizer
        self.y = tf.placeholder(tf.float32, [None, output_nodes])
        squared_deltas = tf.square(self.model - self.y)
        self.loss = tf.reduce_sum(squared_deltas)
        optimizer = tf.train.GradientDescentOptimizer(0.1)
        self.train_step = optimizer.minimize(self.loss)

        # Define logging data
        tf.summary.scalar("loss", self.loss)
        self.summary_op = tf.summary.merge_all()

        # Create Session
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

    def train(self, data):
        """
        Trains the network with the given dataset
        """
        batch_x, batch_y = data
        #print(batch_x)
        #print(batch_y)
        summary, placeholder = self.sess.run([self.summary_op, self.train_step], feed_dict={self.x: batch_x, self.y: batch_y})
        return summary

    def compute(self, vector):
        """
        Computes an output from a given float value
        """
        # Compute output from a single input vector
        batch_x = [vector]
        return self.sess.run(self.model, feed_dict={self.x: batch_x})