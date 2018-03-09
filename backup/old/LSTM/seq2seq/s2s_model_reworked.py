#https://medium.com/@ilblackdragon/tensorflow-sequence-to-sequence-3d9d2e238084

import logging

import tensorflow as tf
from tensorflow.contrib import layers
import seq2seq.input_parser as ip

#import seq2seq.timeline_module as timeline


GO_TOKEN = 0
END_TOKEN = 1
UNK_TOKEN = 2


def seq2seq(mode, features, labels, params):
    vocab_size = params['vocab_size']
    embed_dim = params['embed_dim']
    num_units = params['num_units']
    input_max_length = params['input_max_length']
    output_max_length = params['output_max_length']

    inp = features['input']
    output = features['output']
    batch_size = tf.shape(inp)[0]
    start_tokens = tf.zeros([batch_size], dtype=tf.int64)
    train_output = tf.concat([tf.expand_dims(start_tokens, 1), output], 1)
    input_lengths = tf.reduce_sum(tf.to_int32(tf.not_equal(inp, 1)), 1)
    output_lengths = tf.reduce_sum(tf.to_int32(tf.not_equal(train_output, 1)), 1)
    input_embed = layers.embed_sequence(
        inp, vocab_size=vocab_size, embed_dim=embed_dim, scope='embed')
    output_embed = layers.embed_sequence(
        train_output, vocab_size=vocab_size, embed_dim=embed_dim, scope='embed', reuse=True)
    with tf.variable_scope('embed', reuse=True):
        embeddings = tf.get_variable('embeddings')

    cell = tf.contrib.rnn.GRUCell(num_units=num_units)
    encoder_outputs, encoder_final_state = tf.nn.dynamic_rnn(cell, input_embed, dtype=tf.float32)

    train_helper = tf.contrib.seq2seq.TrainingHelper(output_embed, output_lengths)

    pred_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(
        embeddings, start_tokens=tf.to_int32(start_tokens), end_token=1)

    def decode(helper, scope, reuse=None):
        with tf.variable_scope(scope, reuse=reuse):
            attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(
                num_units=num_units, memory=encoder_outputs,
                memory_sequence_length=input_lengths)
            cell = tf.contrib.rnn.GRUCell(num_units=num_units)
            attn_cell = tf.contrib.seq2seq.AttentionWrapper(
                cell, attention_mechanism, attention_layer_size=num_units / 2)
            out_cell = tf.contrib.rnn.OutputProjectionWrapper(
                attn_cell, vocab_size, reuse=reuse
            )
            decoder = tf.contrib.seq2seq.BasicDecoder(
                cell=out_cell, helper=helper,
                initial_state=out_cell.zero_state(
                    dtype=tf.float32, batch_size=batch_size))
                #initial_state=encoder_final_state)
            outputs = tf.contrib.seq2seq.dynamic_decode(
                decoder=decoder, output_time_major=False,
                impute_finished=True, maximum_iterations=output_max_length
            )
            return outputs[0]
    train_outputs = decode(train_helper, 'decode')
    pred_outputs = decode(pred_helper, 'decode', reuse=True)

    tf.identity(train_outputs.sample_id[0], name='train_pred')
    weights = tf.to_float(tf.not_equal(train_output[:, :-1], 1))
    #print(train_outputs.rnn_output)
    #print(output)
    loss = tf.contrib.seq2seq.sequence_loss(train_outputs.rnn_output, output, weights=weights)
    train_op = layers.optimize_loss(
        loss, tf.train.get_global_step(),
        optimizer=params.get('optimizer', 'Adam'),
        learning_rate=params.get('learning_rate', 0.001),
        summaries=['loss', 'learning_rate'])

    tf.identity(pred_outputs.sample_id[0], name='predictions')
    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=pred_outputs.sample_id,
        loss=loss,
        train_op=train_op
    )


def train_seq2seq(input_filename, output_filename, vocab_filename, model_dir):
    vocab = ip.load_vocab(vocab_filename)
    params = {
        'vocab_size': len(vocab),
        'batch_size': 32,
        'input_max_length': 30,
        'output_max_length': 30,
        'embed_dim': 100,
        'num_units': 256
    }
    est = tf.estimator.Estimator(
        model_fn=seq2seq,
        model_dir=model_dir, params=params)

    input_fn, feed_fn = ip.make_input_fn(
        params['batch_size'],
        "test_0",
        output_filename,
        vocab, params['input_max_length'], params['output_max_length'])

    #print("###################################### BEFORE HOOKING #################################################")

    # Make hooks to print examples of inputs/predictions.
    print_inputs = tf.train.LoggingTensorHook(
        ['input_0', 'output_0'], every_n_iter=10,
        formatter=ip.get_formatter(['input_0', 'output_0'], vocab))

    print_predictions = tf.train.LoggingTensorHook(
        ['predictions', 'train_pred'], every_n_iter=10,
        formatter=ip.get_formatter(['predictions', 'train_pred'], vocab))


    #timeline_hook = timeline.TimelineHook(model_dir, every_n_iter=100)

    #print(input_fn)
    #print(feed_fn)

    #est.train(input_fn=input_fn, hooks=[tf.train.FeedFnHook(feed_fn), print_inputs, print_predictions, timeline_hook], steps=10000)
    #est.train(input_fn=input_fn, hooks=[tf.train.FeedFnHook(feed_fn), print_inputs], steps=1000)
    #print("FINISHED TRAINING")


    i = 0
    for s in est.predict(input_fn=input_fn, hooks=[tf.train.FeedFnHook(feed_fn)]):
        print(ip.to_str(s, vocab))
        i += 1
        if i >= 10:
            break


    #print("###################################### AFTER HOOKING #################################################")


def main():
    tf.logging._logger.setLevel(logging.INFO)
    train_seq2seq('input', 'output', 'vocab', 'model/seq2seq')


if __name__ == "__main__":
    main()
