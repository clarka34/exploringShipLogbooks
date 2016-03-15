""" Unit tests for basic_utils.py """
import exploringShipLogbooks
import pep8
import unittest

import exploringShipLogbooks.basic_utils as bu
import os.path as op
import pandas as pd

class TestBasicUtils(unittest.TestCase):
    def setUp(self):
        d = {'ID': [0, 1, 2, 3], 'WindDirection': ['North', 'easT', 'sOuTh',
             'west'], 'ProbWindDD': [4, 5, 6, 7]}
        self.df = pd.DataFrame(d)
        self.desired_columns = ['ID']

    def testDataFolderExists(self):
        data_path = op.join(exploringShipLogbooks.__path__[0], 'data')
        path_exists = op.exists(data_path + '/climate-data-from-ocean-ships.zip')
        self.assertTrue(path_exists)

    def testFilenameCorrect(self):
        test_data = bu.extract_logbook_data('Lookup_UK_WindDirection.csv')
        self.assertTrue(test_data.columns.values[0], 'ID')
        self.assertTrue(test_data.columns.values[0], 'WindDirection')
        self.assertTrue(test_data.columns.values[0], 'ProbWindDD')

    def testWrongFilename(self):
        test_data = bu.extract_logbook_data('fake_filename')
        self.assertTrue('Please enter valid filename.', test_data)

    def testDesiredColumns(self):
        df_copy = bu.isolate_columns(self.df.copy(), self.desired_columns)
        self.assertTrue(df_copy.columns.values[0], 'ID')

    def testUndesiredColumns(self):
        undesired_columns = bu.remove_undesired_columns(self.df.copy(),
                                                        self.desired_columns)
        self.assertTrue(undesired_columns[0], 'ProbWindDD')
        self.assertTrue(undesired_columns[1], 'WindDirection')

    def testCleanData(self):
        df_copy = bu.clean_data(self.df.copy())
        self.assertTrue(df_copy['WindDirection'][0], 'north')

    # def testLabelEncoder(self):
    #    encoded_data = bu.label_encoder(self.df['WindDirection'])
    #    self.assertTrue(encoded_data[0], 0)
    #    self.assertTrue(encoded_data[1], 1)
    #    self.assertTrue(encoded_data[2], 2)
    #    self.assertTrue(encoded_data[3], 3)

    def testLabelEncoder(self):
        encoded_data = bu.label_encoder(self.df['WindDirection'])
        self.assertEqual(encoded_data[0].astype(int), 0)
        self.assertEqual(encoded_data[1].astype(int), 1)
        self.assertEqual(encoded_data[2].astype(int), 2)
        self.assertEqual(encoded_data[3].astype(int), 3)

    def testLabelEncoderKey(self):
        encoded_data_key = bu.label_encoder_key(self.df['WindDirection'])
        self.assertTrue(encoded_data_key[0], 'North')
        self.assertTrue(encoded_data_key[1], 'easT')
        self.assertTrue(encoded_data_key[2], 'sOuTh')
        self.assertTrue(encoded_data_key[3], 'west')

    def testOneHotEncoder(self):
        encoded_data = bu.one_hot_encoder(self.df['WindDirection'])
        self.assertEqual(encoded_data[0, 0].astype(int), 1)
        self.assertEqual(encoded_data[1, 0].astype(int), 0)
        self.assertEqual(encoded_data[2, 0].astype(int), 0)
        self.assertEqual(encoded_data[3, 0].astype(int), 0)

    def TestEncodeDataNaiveBayes(self):
        encoded_data, encoder = bu.encode_data(self.df, 'Naive Bayes')
        self.assertEqual(encoded_data[0, 2].astype(int), 1)
        self.assertEqual(encoded_data[1, 2].astype(int), 0)
        self.assertEqual(encoded_data[2, 2].astype(int), 0)
        self.assertEqual(encoded_data[3, 2].astype(int), 0)

    def TestEncodeDataDecisionTree(self):
        encoded_data, encoder = bu.encode_data(self.df, 'Decision Tree')
        self.assertEqual(encoded_data[0, 2].astype(int), 0)
        self.assertEqual(encoded_data[1, 2].astype(int), 1)
        self.assertEqual(encoded_data[2, 2].astype(int), 2)
        self.assertEqual(encoded_data[3, 2].astype(int), 3)
#class TestCodeFormat(unittest.TestCase):
#    def test_pep8_conformance(self):
#        # pep8style = pep8.StyleGuide(quiet=True)
#        pep8style.options.ignore = pep8style.options.ignore + tuple(['E501'])
#        pep8style.input_dir('exploringShipLogbooks')
#        pep8style.options.max_line_length = 100
#        result = pep8style.check_files()
#        self.assertEqual(result.total_errors, 0,
#                         "PEP8 POLICE - WOOOOOWOOOOOOOOOO")
