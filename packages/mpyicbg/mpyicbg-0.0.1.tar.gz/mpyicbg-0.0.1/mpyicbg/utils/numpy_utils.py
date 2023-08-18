import numpy


def get_random_state(seed):
    try:
        return numpy.random.RandomState(seed)
    except TypeError:
        if isinstance(seed, numpy.random.RandomState):
            return seed
    raise ValueError(
        "cannot initialize random state with seed {}".format(seed))
