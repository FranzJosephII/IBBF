import tensorflow as tf
import seq2seq.seq2seq_interface as itf

GO_TOKEN = 0
END_TOKEN = 1
UNK_TOKEN = 2


def make_input_fn(batch_size, vocab, input_max_length, output_max_length, test, itf):

    def format(str):
        out = ""
        for c in str:
            out += c + " "
        return out[:-1]

    def tokenize_and_map(line, vocab):
        return [vocab.get(token, UNK_TOKEN) for token in line.split(' ')]

    def sample():
        # get sample from generator
        in_line, out_line = itf.give_sample()
        in_line = format(in_line)
        out_line = format(out_line)
        if test != None:
            in_line = test
        #print("1:: \"" + in_line + "\" --> \"" + out_line + "\"")
        return {
            'input': tokenize_and_map(in_line, vocab)[:input_max_length - 1] + [END_TOKEN],
            'output': tokenize_and_map(out_line, vocab)[:output_max_length - 1] + [END_TOKEN]
        }

    def input_fn():
        inp = tf.placeholder(tf.int64, shape=[None, None], name='input')
        output = tf.placeholder(tf.int64, shape=[None, None], name='output')
        tf.identity(inp[0], 'input_0')
        tf.identity(output[0], 'output_0')
        return {
            'input': inp,
            'output': output,
        }, None

    def feed_fn():
        inputs, outputs = [], []
        input_length, output_length = 0, 0
        for i in range(batch_size):
            #rec = sample_me.next()
            rec = sample()
            #print("2:: " + str(rec))
            inputs.append(rec['input'])
            outputs.append(rec['output'])
            input_length = max(input_length, len(inputs[-1]))
            output_length = max(output_length, len(outputs[-1]))
        # Pad me right with </S> token.
        for i in range(batch_size):
            inputs[i] += [END_TOKEN] * (input_length - len(inputs[i]))
            outputs[i] += [END_TOKEN] * (output_length - len(outputs[i]))
        return {
            'input:0': inputs,
            'output:0': outputs
        }

    return input_fn, feed_fn


def load_vocab(filename):
    vocab = {}
    with open(filename) as f:
        for idx, line in enumerate(f):
            vocab[line.strip()] = idx
    return vocab


def get_rev_vocab(vocab):
    return {idx: key for key, idx in vocab.items()}


def to_str(sequence, vocab):
    tokens = [
        get_rev_vocab(vocab).get(x, "<UNK>") for x in sequence]
    return ' '.join(tokens)

