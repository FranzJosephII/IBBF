import os

import old_generator as g
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class GAN:

    def __init__(self, model):
        """
        Defines the structure and calculation model of a GAN, sets if the GAN learns from positive or negative samples
        """

        # Defines if GAN is positive or negative
        self.model = model

        # Generator model
        self.G_X = tf.placeholder(tf.float32, shape=[None, 64])
        G_W1 = tf.Variable(tf.random_uniform([64, 128], -0.037, 0.037))
        G_W2 = tf.Variable(tf.random_uniform([128, 702], -0.088, 0.088))
        G_model_part1 = tf.nn.relu(tf.matmul(self.G_X, G_W1))
        self.G_model = tf.sigmoid(tf.matmul(G_model_part1, G_W2))

        # Discriminator model
        self.D_X = tf.placeholder(tf.float32, shape=[None, 702])
        D_W1 = tf.Variable(tf.random_uniform([702, 128], -0.18, 0.18))
        D_W2 = tf.Variable(tf.random_uniform([128, 1], -0.088, 0.088))
        D_model_part1_X = tf.nn.relu(tf.matmul(self.D_X, D_W1))
        D_model_X = tf.sigmoid(tf.matmul(D_model_part1_X, D_W2))
        D_model_part1_G = tf.nn.relu(tf.matmul(self.G_model, D_W1))
        D_model_G = tf.sigmoid(tf.matmul(D_model_part1_G, D_W2))

        # Define loss functions
        D_loss = -tf.reduce_mean(tf.log(D_model_X) + tf.log(1. - D_model_G))
        G_loss = -tf.reduce_mean(tf.log(D_model_G))

        # Define train functions
        self.D_train = tf.train.AdamOptimizer().minimize(D_loss, var_list=[D_W1, D_W2])
        self.G_train = tf.train.AdamOptimizer().minimize(G_loss, var_list=[G_W1, G_W2])

        # Initialize Session
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def train(self, size):
        """
        Trains the GAN with a given amount of samples, differentiate between positive and negative GAN
        """
        if self.model == "positive":
            for i in range(size):
                self.sess.run(self.D_train, feed_dict={self.D_X: [g.getPositiveSample()], self.G_X: [g.getRandomInput()]})
                self.sess.run(self.G_train, feed_dict={self.G_X: [g.getRandomInput()]})
        elif self.model == "negative":
            for i in range(size):
                self.sess.run(self.D_train, feed_dict={self.D_X: [g.getNegativeSample()], self.G_X: [g.getRandomInput()]})
                self.sess.run(self.G_train, feed_dict={self.G_X: [g.getRandomInput()]})
        else:
            print("ERROR")

    def getSample(self):
        """
        Returns a sample generated by the Generator Net of the GAN
        """
        return self.sess.run(self.G_model, feed_dict={self.G_X: [g.getRandomInput()]})

    def evaluate(self, size):
        """
        Evaluates the GAN
        Calculates percentage of generated samples which are either above or below 0.5,
        depending on whether the GAN is positive or negative.
        Returns accuracy of generated samples.
        """
        correct_answers = 0
        for i in range(size):
            sample = self.sess.run(self.G_model, feed_dict={self.G_X: [g.getRandomInput()]})[0][0]
            if self.model == "positive" and sample > 0.5:
                correct_answers += 1
            if self.model == "negative" and sample < 0.5:
                correct_answers += 1
        return correct_answers / size
