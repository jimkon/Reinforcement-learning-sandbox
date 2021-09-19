import numpy as np


def clip(n, low, high):
    if low > high:
        raise AttributeError("Low argument has to be less or equal than high argument.")
    return low if n < low else high if n > high else n


class Map1D:
    def __init__(self, in_low, in_high, out_a, out_b, clip=False):
        if in_low > in_high:
            raise AttributeError("in_low argument has to be less than in_high argument.")

        if in_low == in_high:
            raise AttributeError("in_low argument and in_high argument cannot be equal.")

        if out_a == out_b:
            raise AttributeError("out_a argument and out_b argument cannot be equal.")

        self.in_low, self.in_high = in_low, in_high
        self.in_range = self.in_high-self.in_low

        self.out_a, self.out_b, self.out_low = out_a, out_b, min(out_a, out_b)
        self.out_range = self.out_b-self.out_a

        self.f = lambda x: self.__map_clipped(x) if clip else self.__map(x)

    def __map(self, x):
        x_0 = x - self.in_low
        x_n = x_0 / self.in_range
        x_mapped = x_n * self.out_range + self.out_a
        return x_mapped

    def __map_clipped(self, x):
        return self.__map(clip(x, self.in_low, self.in_high))

    def map(self, x):
        return self.f(x)

    def __call__(self, x):
        return self.map(x)


class MapFloatToInteger:
    def __init__(self, low, high, n, clip_flag=True):
        if low > high:
            raise AttributeError("low argument has to be less than high argument.")

        if low == high:
            raise AttributeError("low argument and high argument cannot be equal.")

        if n < 2 or not isinstance(n, int):
            raise AttributeError("n argument must be an integer >= 2.")

        self.__map_in = Map1D(low, high, 0, n-1, clip=clip_flag)
        self.__map_out = Map1D(0, n-1, low, high, clip=clip_flag)

        # if clip_flag:
        #     self.clip_f = lambda x : clip(x, 0, n-1)
        # else:
        #     self.clip_f = lambda x : x

    def map(self, x):
        return round(self.__map_in(x))

    def reverse(self, n):
        return self.__map_out(n)

