import unittest
import os
import time
from pipeRewrite import *

class testTmp1(unittest.TestCase, pipeRewrite):
    def setUp(self):
        pipeRewrite.__init__(self, "testTmp1")

    def tearDown(self):
        pass

    def testPass(self):
        time.sleep(2)
        self.assertEqual(0, 0)

    def testFail(self):
        time.sleep(3)
        self.assertEqual(1, 0)

if __name__ == "__main__":
    unittest.main()