import os
import seq2seq.seq2seq_model as net
import datetime
import seq2seq.seq2seq_interface as itf

class seq2seq_nn_fuzzer:
    def __init__(self, system, _BATCH_SIZE, _DEBUG):

        self._DEBUG = _DEBUG
        self._BATCH_SIZE = _BATCH_SIZE

        now = datetime.datetime.now()
        self.model_dir_name = "logs\\seq2seq\\" + str(now.day) + "." + str(now.month) + "." + str(now.year) + "." + str(now.hour) + "." + str(now.minute) + "." + str(now.second)
        self.vocab_filename = "vocab"

        self.itf = itf.s2s_interface(system)

        self.s2s = net.seq2seq(self.itf, self.vocab_filename, self.model_dir_name)

    def train(self, _STEPS):

        for i in range(_STEPS):
            self.s2s.train(self._BATCH_SIZE)

            #for i in range(self._BATCH_SIZE):
            #    s = self.s2s.compute("1")
            #    print(s)
            #    self.itf.membership_query(s)

            if self._DEBUG:
                print("0   --> " + self.s2s.compute("0"))
                print("0.5 --> " + self.s2s.compute("0.5"))
                print("1   --> " + self.s2s.compute("1") + "\n")

    def print_loss(self):
        os.system("tensorboard --logdir=" + self.model_dir_name)
