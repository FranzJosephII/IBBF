import os, math
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class classificator:

    def __init__(self, _MAXLENGTH, interface, reportfile):
        """
        Defines the structure and calculation model of a GAN
        """

        self.reportfile = reportfile

        # Parameter
        self._MAXLENGTH = _MAXLENGTH
        self._MAXWORDLENGTH = int(_MAXLENGTH / 5)
        self.itf = interface
        self.evaldata = None

        # Calculate layer size depending on the maximum word length
        x_nodes = self._MAXLENGTH                       # Size of the input layer
        h_nodes = x_nodes*2                             # Size of the hidden layers
        o_nodes = 1                                     # Size of the output layer
        x2h_nodes = int(math.sqrt(x_nodes * h_nodes))   # Size of the layer between input and hidden layer
        h2o_nodes = int(math.sqrt(h_nodes * o_nodes))   # Size of the layer between hidden and output layer

        # Calculate init parameter for layers depending on the incoming connections N: 1/sqrt(N)
        from_x = 1/math.sqrt(x_nodes)
        from_x2h = 1/math.sqrt(x2h_nodes)
        from_h = 1/math.sqrt(h_nodes)
        from_h2o = 1/math.sqrt(h2o_nodes)

        #print(x_nodes)
        #print(from_x)
        #print(x2h_nodes)
        #print(from_x2h)
        #print(h_nodes)
        #print(from_h)
        #print(h2o_nodes)
        #print(from_h2o)
        #print(o_nodes)


        #sys.exit()


        # Define Layers
        self.X = tf.placeholder(tf.float32, shape=[None, x_nodes])
        W1 = tf.Variable(tf.random_uniform([x_nodes, x2h_nodes], -from_x, from_x))
        B1 = tf.Variable(tf.zeros([x2h_nodes]))
        X2 = tf.nn.relu(tf.matmul(self.X, W1) + B1)

        W2 = tf.Variable(tf.random_uniform([x2h_nodes, h_nodes], -from_x2h, from_x2h))
        B2 = tf.Variable(tf.zeros(h_nodes))
        X3 = tf.nn.relu(tf.matmul(X2, W2) + B2)

        W3 = tf.Variable(tf.random_uniform([h_nodes, h_nodes], -from_h, from_h))
        B3 = tf.Variable(tf.zeros(h_nodes))
        X4 = tf.nn.relu(tf.matmul(X3, W3) + B3)

        W4 = tf.Variable(tf.random_uniform([h_nodes, h2o_nodes], -from_h, from_h))
        B4= tf.Variable(tf.zeros(h2o_nodes))
        X5 = tf.nn.relu(tf.matmul(X4, W4) + B4)

        W5 = tf.Variable(tf.random_uniform([h2o_nodes, o_nodes], -from_h2o, from_h2o))
        B5 = tf.Variable(tf.zeros(o_nodes))

        self.model = tf.sigmoid(tf.matmul(X5, W5) + B5)

        # Define loss and training
        self.Y = tf.placeholder(tf.float32, [None, 1])
        squared_deltas = tf.square(self.model - self.Y)
        self.loss = tf.reduce_sum(squared_deltas)
        optimizer = tf.train.AdamOptimizer()

        self.train_op = optimizer.minimize(self.loss)

        # Define logging data
        tf.summary.scalar("Total loss", self.loss)
        self.summary_op = tf.summary.merge_all()

        # Initialize Session
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def train(self, data):
        """
        Trains the model with given dataset (list of samples)
        """
        samples, labels = data
        summary, placeholder = self.sess.run([self.summary_op, self.train_op], feed_dict={self.X: samples, self.Y: labels})
        return summary

    def calculate(self, sample):
        return self.sess.run(self.model, feed_dict={self.X: sample})[0][0]

    def evaluate(self, data):
        """
        Calculates the accuracy of the model and returns it
        """
        amount = 10000
        if data == None:
            if self.evaldata == None:
                self.evaldata = self.itf.get_training_batch(amount)
                f = open(self.reportfile, 'a')
                f.write(str(self.itf.queries()) + ";" + "START\n")
                f.close()
            samples, labels = self.evaldata
        else:
            samples, labels = data

        answers = self.sess.run(self.model, feed_dict={self.X: samples})

        pos = 0
        for i in range(amount):
            if (labels[i][0] == 1 and answers[i][0] > 0.5) or (labels[i][0] == 0 and answers[i][0] < 0.5):
                pos += 1

        # Write report to file
        f = open(self.reportfile, 'a')
        f.write(str(self.itf.queries()) + ";" + str(pos/amount) + "\n")
        f.close()

        return pos/amount
