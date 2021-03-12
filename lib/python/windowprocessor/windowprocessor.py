import numpy as np

class windowProcessor:
    def __init__(self, window_size):
        self.window_size = window_size

    def _convert(self, x):
        m = np.empty((len(x), self.window_size))
        for i in range(len(x)):
            c = np.array(eval(x[i]))

            m[i, :] = np.array(eval(x[i]))
        return m

    def fit(self, x):
        m = self._convert(x)
        self.min_value, self.max_value = m.min(), m.max()

    def transform(self, x):
        m = self._convert(x)
        return (m - self.min_value) / (self.max_value - self.min_value)