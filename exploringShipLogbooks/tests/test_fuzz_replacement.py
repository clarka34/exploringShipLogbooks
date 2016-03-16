""" Unit tests for basic_utils.py """
import exploringShipLogbooks
import pep8
import unittest

import numpy as np
import pandas as pd

import exploringShipLogbooks.fuzz_replacement as fr


class TestFuzzReplacement(unittest.TestCase):

    def setUp(self):
        self.all_log_values = [
            'dutch',
            'french',
            'spanish',
            'spain',
            'english',
            'england',
            'france'
        ]

        self.slave_log_values = [
            'dutch',
            'french',
            'spain',
            'england',
        ]

        self.matches = fr.finding_fuzzy_matches(self.all_log_values,
                                                self.slave_log_values)

        fuzzy_array = np.concatenate(([self.all_log_values], [np.zeros(len(
                                     self.all_log_values), dtype=int)]))
        fuzzy_df = pd.DataFrame(fuzzy_array, index=['log_values',
                                'count']).transpose()
        fuzzy_df['count'] = fuzzy_df['count'].astype(int)

        # create dictionary of fuzzy matches
        self.my_dict = fr.finding_fuzzy_matches(self.all_log_values,
                                                self.slave_log_values)

        # filter dictionary to only include matches above certain threshold
        self.my_dict_2 = fr.deleting_matches_below_threshold(60, self.my_dict)

        # update the count column to assign the same count to matching strings
        self.fuzzy_df = fr.matching_values(self.my_dict_2, fuzzy_df)

        # build the dictionary to merge the values in the original dataframe
        self.fuzzy_dict = fr.building_fuzzy_dict(self.fuzzy_df,
                                                 self.slave_log_values)

    def testFindingFuzzyMatches(self):
        # test to make sure fuzzywuzzy process returns the desired dictionary
        self.assertCountEqual(self.matches.keys(), self.all_log_values)
        # self.assertCountEqual(matching_name.values(), self.slave_log_values)

    def testDeletingMatchesBelowThreshold(self):
        expected_result = [[], [], [('spain', 67)], [], [('french', 67)],
                           [], []]
        self.assertCountEqual(self.my_dict_2.keys(), self.all_log_values)
        self.assertCountEqual(self.my_dict_2.values(), expected_result)

    def testMatchingValues(self):
        self.assertTrue(np.array_equal(self.fuzzy_df['log_values'],
                        self.all_log_values))
        self.assertCountEqual(list(self.fuzzy_df['count']),
                              [0, 2, 1, 1, 0, 0, 2])

    def testBuildingFuzzyDict(self):
        keys_fuzzy = ['english', 'spanish', 'france']
        values_fuzzy = [[['dutch', 'england']], [['spain']], [['french']]]
        self.assertCountEqual(self.fuzzy_dict.keys(), keys_fuzzy)
        self.assertCountEqual(self.fuzzy_dict.values(), values_fuzzy)
