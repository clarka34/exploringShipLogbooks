""" Unit tests for basic_utils.py """
import exploringShipLogbooks
import pep8
import unittest

import exploringShipLogbooks.basic_utils as bu
import numpy as np
import os.path as op
import pandas as pd


class TestBasicUtils(unittest.TestCase):
    def setUp(self):
        # set up the values to be used in the unit tests
        d = {'ID': [0, 1, 2, 3], 'WindDirection': ['North', 'easT', 'sOuTh',
             'west'], 'ProbWindDD': [4, 5, 6, 7]}
        self.df = pd.DataFrame(d)
        self.desired_columns = ['ID']

    def testDataFolderExists(self):
        # test to make sure the zip file containing the data exists
        data_path = op.join(exploringShipLogbooks.__path__[0], 'data')
        path_exists = op.exists(data_path + '/climate-data-from-ocean-ships.zip')
        self.assertTrue(path_exists)

    def testFilenameCorrect(self):
        # test to make sure the function works if a valid filename is entered
        test_data = bu.extract_logbook_data('Lookup_UK_WindDirection.csv')
        self.assertTrue(test_data.columns.values[0], 'ID')
        self.assertTrue(test_data.columns.values[0], 'WindDirection')
        self.assertTrue(test_data.columns.values[0], 'ProbWindDD')

    def testWrongFilename(self):
        # test to make sure a KeyError is raised if an invalid filename is
        # entered
        self.assertRaises(KeyError, bu.extract_logbook_data('fake_filename'))

    def testDesiredColumns(self):
        # test to make sure isolate_columns returns a dataframe with the
        # desired columns
        df_copy = bu.isolate_columns(self.df.copy(), self.desired_columns)
        self.assertTrue(df_copy.columns.values[0], 'ID')

    def testUndesiredColumns(self):
        # test to make sure the names of the undesired columns are returned
        undesired_columns = bu.remove_undesired_columns(self.df.copy(),
                                                        self.desired_columns)
        self.assertTrue(undesired_columns[0], 'ProbWindDD')
        self.assertTrue(undesired_columns[1], 'WindDirection')

    def testCleanData(self):
        # test to make sure the string values are converted to lower case
        df_copy = bu.clean_data(self.df.copy())
        self.assertTrue(df_copy['WindDirection'][0], 'north')
        self.assertTrue(df_copy['WindDirection'][1], 'east')
        self.assertTrue(df_copy['WindDirection'][2], 'south')
        self.assertTrue(df_copy['WindDirection'][3], 'west')

    def testLabelEncoder(self):
        # test to make sure the LabelEncoder converts categorical data to
        # numerical data
        encoded_data = bu.label_encoder(self.df['WindDirection'])
        self.assertTrue(np.array_equal(encoded_data, np.array([0, 1, 2, 3])))

    def testLabelEncoderKey(self):
        # test to make check that the LabelEncoder returns the correct key
        encoded_data_key = bu.label_encoder_key(self.df['WindDirection'])
        self.assertTrue(encoded_data_key[0], 'North')
        self.assertTrue(encoded_data_key[1], 'easT')
        self.assertTrue(encoded_data_key[2], 'sOuTh')
        self.assertTrue(encoded_data_key[3], 'west')

    def testOneHotEncoder(self):
        # test to make sure the OneHotEncoder converts numerical data to one
        # hot encoded data
        encoded_data = bu.one_hot_encoder(self.df['WindDirection'])
        self.assertTrue(np.array_equal(encoded_data[:, 0],
                        np.array([1, 0, 0, 0])))

    def TestEncodeDataNaiveBayes(self):
        # test encoder using the Naive Bayes algorithm and one hot encoding
        encoded_data, encoder = bu.encode_data(self.df, 'Naive Bayes')
        self.assertTrue(np.array_equal(encoded_data[:, 2],
                        np.array([1, 0, 0, 0])))

    def TestEncodeDataDecisionTree(self):
        # test encoder using the decision tree algorithm and label encoding
        encoded_data, encoder = bu.encode_data(self.df, 'Decision Tree')
        self.assertTrue(np.array_equal(encoded_data[:, 2],
                        np.array([0, 1, 2, 3])))

    def TestEncodeDataNaiveBayesDF(self):
        # test conversion of encoded data to pandas dataframe using using the
        # Naive Bayes classification algorithm
        encoded_df = bu.encode_data_df(self.df, 'Naive Bayes')
        columns = encoded_df.columns.values
        self.assertEqual(columns[0], 'ID')
        self.assertEqual(columns[1], 'ProbWindDD')
        self.assertEqual(columns[2], 'North')
        self.assertEqual(columns[3], 'easT')
        self.assertEqual(columns[4], 'sOuTh')
        self.assertEqual(columns[5], 'west')

    def TestEncodeDataDecisionTreeDF(self):
        # test conversion of encoded data to pandas dataframe using using the
        # decision tree classification algorithm
        encoded_df = bu.encode_data_df(self.df, 'Decision Tree')
        columns = encoded_df.columns.values
        self.assertEqual(columns[0], 'ID')
        self.assertEqual(columns[1], 'ProbWindDD')
        self.assertEqual(columns[2], 'WindDirection')
