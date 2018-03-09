import random, string

class monkey_fuzzer:
    def __init__(self, system, _MAX_LEN, _DEBUG, reportfile):
        self.system = system
        self._MAX_LEN = _MAX_LEN
        self._DEBUG = _DEBUG

    def gen_sample(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(1, self._MAX_LEN)))

    def start(self):
        if self._DEBUG: print("Start Fuzzing ...")
        while(42==42):
            self.system.membership_query(self.gen_sample())