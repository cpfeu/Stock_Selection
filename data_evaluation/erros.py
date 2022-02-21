import math
import numpy as np


class FormatError(RuntimeError):
    """Exception raised for formatting errors."""


class ErrorAnalyzer:

    def __init__(self, original, forecast):
        self.a = original
        self.b = forecast

    def check(self):
        if len(self.a) != len(self.b):
            raise FormatError('Sizing failure between time series lists')

    def get_rmse(self):
        """
        Return scalar of RMSE between two vectors
        """
        self.check()
        return math.sqrt(np.mean((np.array(self.a) - np.array(self.b)) ** 2))

    def get_mae(self):
        """
        Return scalar of MAE between two vectors
        """
        self.check()
        return np.mean(np.absolute(np.array(self.a) - np.array(self.b)))

    def get_mape(self):
        """
        Compute mean absolute percentage error (MAPE)
        """
        y_true, y_pred = np.array(self.a), np.array(self.b)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def get_momentum_error(self):
        """
        Return scalar of momentum error between two vectors
        """
        self.check()
        momentum = [0]
        for i in range(len(self.b)-1):
            m_a = 1 if (self.a[i+1] >= self.a[i]) else 0
            m_b = 1 if (self.b[i+1] >= self.b[i]) else 0
            momentum.append(1 if (m_a == m_b) else -1)
        return np.mean(np.array(momentum))

    def get_correlation(self):
        return np.corrcoef(self.b, self.a)[0, 1]
