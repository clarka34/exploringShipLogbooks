""" Unit tests for basic_utils.py """
import exploringShipLogbooks
import pep8
import unittest

import numpy as np
import pandas as pd

import exploringShipLogbooks.fuzz_replacement as fuzzy


class RatioTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"
        self.s7 = 'new york city mets - atlanta braves'

        self.nationality_strings = [
            'dutch',
            'french',
            'spanish',
            'spain',
            'english',
            'england',
            'france'
        ]

    def testEqual(self):
        self.assertEqual(fuzz.ratio(self.s1, self.s1a), 100)

    def testCaseInsensitive(self):
        self.assertNotEqual(fuzz.ratio(self.s1, self.s2), 100)
        self.assertEqual(fuzz.ratio(utils.full_process(self.s1),
                         utils.full_process(self.s2)), 100)

    def testPartialRatio(self):
        self.assertEqual(fuzz.partial_ratio(self.s1, self.s3), 100)
