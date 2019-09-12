import indexing
import msgstats
import unittest
import numpy as np

class Tests_cossine(unittest.TestCase):
    
    def test_0(self):
        v1 = [1, 0]
        v2 = [0, 1]
        self.assertAlmostEqual(msgstats.sparse_cossine(v1, v2), 0.0)

    def test_1(self):
        v1 = np.random.rand(100, 1)
        v2 = v1
        self.assertAlmostEqual(msgstats.sparse_cossine(v1, v2), 1.0)

    def test_2(self):
        v1 = [1, 2]
        v2 = [1, 2]
        self.assertAlmostEqual(msgstats.sparse_cossine(v1, v2), 1.0)

    def test_2(self):
        v1 = [1, -2]
        v2 = [1, -2]
        self.assertAlmostEqual(msgstats.sparse_cossine(v1, v2), 1.0)

if __name__ == '__main__':
    unittest.main()
