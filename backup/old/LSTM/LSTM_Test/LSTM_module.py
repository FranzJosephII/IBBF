import os

import tensorflow as tf

from old.LSTM_Test import generator as g

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class LSTM:
    def __init__(self):
        # Global config variables
        self.num_steps = 10 * 5
        self.batch_size = 1
        num_classes = 2
        state_size = 10
        learning_rate = 0.1
        num_layers = 1

        self.x = tf.placeholder(tf.int32, [self.batch_size, self.num_steps], name='input_placeholder')
        self.y = tf.placeholder(tf.int32, [self.batch_size, self.num_steps], name='labels_placeholder')

        x_one_hot = tf.one_hot(self.x, num_classes)
        rnn_inputs = tf.unstack(x_one_hot, axis=1)

        cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.LSTMCell(state_size) for _ in range(num_layers)])
        self.init_state = cell.zero_state(self.batch_size, tf.float32)
        self.rnn_outputs, self.final_state = tf.contrib.rnn.static_rnn(cell, rnn_inputs, initial_state=self.init_state)

        with tf.variable_scope('softmax'):
            W = tf.get_variable('W', [state_size, num_classes])
            b = tf.get_variable('b', [num_classes], initializer=tf.constant_initializer(0.0))
        logits = [tf.matmul(rnn_output, W) + b for rnn_output in self.rnn_outputs]
        self.predictions = [tf.nn.softmax(logit) for logit in logits]

        # Turn our y placeholder into a list of labels
        y_as_list = tf.unstack(self.y, num=self.num_steps, axis=1)

        #losses and train_step
        """
        loss_weights = [tf.ones([self.batch_size]) for i in range(self.num_steps)]
        losses = tf.contrib.legacy_seq2seq.sequence_loss_by_example(logits, y_as_list, loss_weights)
        total_loss = tf.reduce_mean(losses)
        self.train_step = tf.train.AdamOptimizer(learning_rate).minimize(total_loss)
        """
        self.losses = [tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label, logits=logit) for \
                  logit, label in zip(logits, y_as_list)]
        self.total_loss = tf.reduce_mean(self.losses)
        self.train_step = tf.train.AdagradOptimizer(learning_rate).minimize(self.total_loss)

        # Create Session
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        print("Initialized ...")


    def train(self, num_epochs):
        total_loss = 0
        for idx, epoch in enumerate(g.gen_epochs(num_epochs, self.num_steps, self.batch_size)):
            for step, (X, Y) in enumerate(epoch):
                    loss, placeholder = self.sess.run([self.total_loss, self.train_step], feed_dict={self.x: X, self.y: Y})
                    total_loss += loss
        return total_loss


    def compute(self, sample):
        o = self.sess.run(self.predictions, feed_dict={self.x: [g.calcvector(sample)]})
        output = []
        print(o)
        for i in o:
            output.append(i[0][1])
        return g.calcstring(output)