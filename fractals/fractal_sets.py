#
# (C) Andreas Gaiser, 2019
#
''' A simple generator for Julia sets. '''

import numpy as np
import matplotlib.pyplot as plt

class FractalSet(object):

    def __init__(self, size, stop_update_after=100.0):
        self._size = size
        self._a =  np.zeros([size, size], dtype = complex)
        delta = 4.0 / size
        for x in range(0, size):
            for y in range(0, size):
                self._a[x,y] = np.complex(x*delta-2.0, y*delta-2.0)
        self._stop_after = stop_update_after

    def iterate(self, number_iterations, animate=True):
        for i in range(0, number_iterations):
            self._iteration()
            if animate:
                plt.imshow(np.abs(self._a), cmap='gray')
                plt.pause(0.05)
        plt.imshow(np.abs(self._a), cmap='gray')
        plt.show()


class MandelbrotSet(FractalSet):

    def _one_step(self, old_value, c):
        return old_value * old_value + c

    def _iteration(self):
        delta = 4.0 / self._size
        for x in range(0, self._size):
            for y in range(0, self._size):
                if abs(self._a[x, y]) > self._stop_after:
                    continue
                c = np.complex(x * delta - 2.0, y * delta - 2.0)
                self._a[x, y] = self._one_step(self._a[x, y], c)


class JuliaSet(FractalSet):

    def __init__(self, c, size, stop_update_after=100.0):
        super().__init__(size, stop_update_after)
        self._c = c

    def _one_step(self, old_value):
        return old_value * old_value + self._c

    def _iteration(self):
        for x in range(0, self._size):
            for y in range(0, self._size):
                if abs(self._a[x, y]) > self._stop_after:
                    continue
                self._a[x, y] = self._one_step(self._a[x,y])



if __name__ == '__main__':

    js = JuliaSet(np.complex(-0.5, 0.5), 1000, 4.0)
    js.iterate(20)

    #ms = MandelbrotSet(1000, 3.0)
    #ms.iterate(25)
    print("Done.")