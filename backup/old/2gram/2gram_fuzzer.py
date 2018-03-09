import GAN
import fuzzernetwork
import old_generator as g

_DEBUG = True
_BATCH_SIZE = 100

GAN_p = GAN.GAN("positive")
GAN_n = GAN.GAN("negative")
fuzzer = fuzzernetwork.fuzzer()

if _DEBUG: ctr = 0

while(42):
    # Train GANs
    GAN_p.train(_BATCH_SIZE)
    GAN_n.train(_BATCH_SIZE)

    # Train fuzzer with artificial samples
    for i in range(_BATCH_SIZE):
        fuzzer.train(([[0.99], [0.01]], [GAN_p.getSample()[0], GAN_n.getSample()[0]]))

    """
    # Fuzz system
    fuzzing_samples = []
    for i in range(_BATCH_SIZE*2):
        fuzzing_samples.append(fuzzer.compute(g.getFuzzerInput()))
    """

    # Debug Output
    if _DEBUG:
        if ctr % 10 == 0:
            print("##################################")
            print("0.01 --> " + str(g.gramToString(fuzzer.compute([0.01])[0])))
            print("0.5  --> " + str(g.gramToString(fuzzer.compute([0.5])[0])))
            print("0.99 --> " + str(g.gramToString(fuzzer.compute([0.99])[0])))
        ctr += 1
