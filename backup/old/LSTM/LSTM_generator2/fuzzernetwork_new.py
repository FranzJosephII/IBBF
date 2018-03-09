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
        steps = 3
        input_size = 5  # number of truncated backprop steps ('n' in the discussion above)
        output_size = 5
        batch_size = 1
        state_size = 5
        learning_rate = 0.1

        # Create the model
        self.x = tf.placeholder(tf.float32, [batch_size, input_size], name='input_placeholder')
        self.y = tf.placeholder(tf.int32, [batch_size, steps, output_size], name='labels_placeholder')

        # Turn our x placeholder into a list of one-hot tensors:
        # rnn_inputs is a list of num_steps tensors with shape [batch_size, num_classes]
        #x_one_hot = tf.one_hot(self.x, num_classes)
        #rnn_input = tf.unstack(x_one_hot, axis=1)
        rnn_input = self.x

        with tf.variable_scope('rnn_cell'):
            W = tf.get_variable('W', [input_size, state_size])
            b = tf.get_variable('b', [state_size], initializer=tf.constant_initializer(0.0))

        def rnn_cell(rnn_input):
            with tf.variable_scope('rnn_cell', reuse=True):
                W = tf.get_variable('W', [input_size, state_size])
                b = tf.get_variable('b', [state_size], initializer=tf.constant_initializer(0.0))
            return tf.tanh(tf.matmul(rnn_input, W) + b)

        self.outputs = []
        for i in range(steps):
            state = rnn_cell(rnn_input)
            rnn_input = state
            self.outputs.append(state)


        # logits and predictions
        with tf.variable_scope('softmax'):
            W = tf.get_variable('W', [input_size, state_size])
            b = tf.get_variable('b', [state_size], initializer=tf.constant_initializer(0.0))
        logits = [tf.matmul(rnn_output, W) + b for rnn_output in self.outputs]
        predictions = [tf.nn.softmax(logit) for logit in logits]

        # Turn our y placeholder into a list of labels
        y_as_list = tf.unstack(self.y, num=steps, axis=1)

        # losses and train_step
        losses = [tf.nn.softmax_cross_entropy_with_logits(labels=label, logits=logit) for \
                  logit, label in zip(logits, y_as_list)]
        self.total_loss = tf.reduce_mean(losses)
        self.train_step = tf.train.AdagradOptimizer(learning_rate).minimize(self.total_loss)

        # Create Session
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()


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

