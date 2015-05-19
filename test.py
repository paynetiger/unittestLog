import unittest
import os
import time
from pipeRewrite import *

class testTmp(unittest.TestCase, pipeRewrite):
    def setUp(self):
        pipeRewrite.__init__(self, "testTmp")

    def tearDown(self):
        pass

    def testPass(self):
        time.sleep(5)
        self.assertEqual(0, 0)

    def testFail(self):
        time.sleep(2)
        self.assertEqual(1, 0)

    def testError(self):
        time.sleep(1)
        afafda

if __name__ == "__main__":
    unittest.main()