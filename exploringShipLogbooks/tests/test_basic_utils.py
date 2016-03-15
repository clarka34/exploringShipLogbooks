""" Unit tests for basic_utils.py """

import pep8
import unittest
from basic_utils import extract_logbook_data


class TestExtractData(unittest.TestCase):

    # Test for primes
    def testData(self):
    # 1 digit
    result = primeChecker(7)
    self.assertTrue(result[0])
    # 2 digit
    result = primeChecker(31)
    self.assertTrue(result[0])
    # 3 digit
    result = primeChecker(113)
    self.assertTrue(result[0])

    # Test non-primes
    def testNoData(self):
    # 1 digit
    result = primeChecker(8)
    self.assertFalse(result[0])
    # 2 digit
    result = primeChecker(33)
    self.assertFalse(result[0])
    # 3 digit
    result = primeChecker(112)
    self.assertFalse(result[0])

    # Test explanation for non-prime
    def testExplanation(self):
    result = primeChecker(32)
    self.assertFalse(result[0])
    expected_explanation = "2 times 16 is 32"
    self.assertEqual(result[1], expected_explanation)

from basic_utils import isolate_columns

class TestIsolateColumns(unittest.TestCase):

    # Test for primes
    def testData(self):
    isolate_columns(df, desired_columns)


class TestCodeFormat(unittest.TestCase):
    def test_pep8_conformance(self):
        #pep8style = pep8.StyleGuide(quiet=True)
        pep8style.options.ignore = pep8style.options.ignore + tuple(['E501'])
        pep8style.input_dir('exploringShipLogbooks')
        pep8style.options.max_line_length = 100
        result = pep8style.check_files()
        self.assertEqual(result.total_errors, 0, "PEP8 POLICE - WOOOOOWOOOOOOOOOO")
