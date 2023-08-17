import numpy as np


class UniformRandom:
    def __init__(self) -> None:
        pass

    def initialize(self, weights_shape, fan_in, fan_out):
        return np.random.rand(*weights_shape)