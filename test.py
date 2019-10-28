import indexing
import tf_idf_tools as tf_idf
import unittest
import numpy as np

class Tests_cossine(unittest.TestCase):
    
    def test_0(self):
        v1 = [1, 0]
        v2 = [0, 1]
        self.assertAlmostEqual(tf_idf.sparse_cossine(v1, v2), 0.0)

    def test_1(self):
        v1 = np.random.rand(100, 1)
        v2 = v1
        self.assertAlmostEqual(tf_idf.sparse_cossine(v1, v2), 1.0)

    def test_2(self):
        v1 = [1, 2]
        v2 = [1, 2]
        self.assertAlmostEqual(tf_idf.sparse_cossine(v1, v2), 1.0)

    def test_2(self):
        v1 = [1, -2]
        v2 = [1, -2]
        self.assertAlmostEqual(tf_idf.sparse_cossine(v1, v2), 1.0)

class Tests_is_messages(unittest.TestCase):
    
    def test_filter_missed_calls(self):
        content = "Name missed your call."
        self.assertFalse(indexing._is_messages(content))

    def test_filter_you_missed_calls(self):
        content = "You missed a call from Erik."
        self.assertFalse(indexing._is_messages(content))

    def test_filter_missed_video_chat(self):
        content = "You missed a video chat with Erik."
        self.assertFalse(indexing._is_messages(content))
        
    def test_filter_missed_video_chat(self):
        content = "bby missed your video chat."
        self.assertFalse(indexing._is_messages(content))

    def test_is_message(self):
        content = "Hello, I  missed your call."
        self.assertTrue(indexing._is_messages(content))



if __name__ == '__main__':
    unittest.main()
