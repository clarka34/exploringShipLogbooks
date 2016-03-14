"""
Unit tests for wordcount functions
"""

import unittest
import wordcount as wc
import pandas as pd


class test_wordcount(unittest.TestCase):

    def test_count_key_words(self):
        # test case where the key words are mentioned in the data frame for
        # all columns and for a selection of columns
        col1 = ['dogs are so cute', 'I have a cat', 'turtles are best']
        col2 = ['snake!!!!', 'remember cat dog shaped cheezits?', 'soup']
        col3 = ['dog dog dog', 'cat cat cats', 'mushroom']
        df = pd.DataFrame({'col1': col1, 'col2': col2, 'col3': col3})

        key_words = ['dog', 'dogs', 'cat', 'cats']

        result = wc.count_key_words(df, list(df.columns), key_words)
        expected_result = pd.Series([True, True, False])

        self.assertTrue(pd.Series.equals(result, expected_result))

        result = wc.count_key_words(df, ['col2'], key_words)
        expected_result = pd.Series([False, True, False])

        self.assertTrue(pd.Series.equals(result, expected_result))

        # test case where the key words are not mentioned in the data frame
        key_words = ['bears', 'bumblebees', 'brontosaurus']
        result = wc.count_key_words(df, ['col1', 'col2', 'col3'], key_words)
        expected_result = pd.Series([False, False, False])

        self.assertTrue(pd.Series.equals(result, expected_result))

    def test_count_all_words(self):
        # test case for counting all columns
        col1 = ['cat cat cat', 'dog dog dog', 'cat']
        col2 = ['turtle', 'dog dog', 'cat cat cat']
        col3 = ['elephant elephant', 'dog', 'dog dog']
        df = pd.DataFrame({'col1': col1, 'col2': col2, 'col3': col3})

        result = wc.count_all_words(df, list(df.columns))
        expected_result = pd.DataFrame()
        expected_result['Word'] = ['dog', 'cat', 'elephant', 'turtle']
        expected_result['Count'] = [8, 7, 2, 1]
        expected_result.index = [1, 2, 3, 4]

        self.assertTrue(pd.DataFrame.equals(result, expected_result))

        # test case for counting only selected columns
        result = wc.count_all_words(df, ['col1', 'col2'])
        expected_result = pd.DataFrame()
        expected_result['Word'] = ['cat', 'dog', 'turtle']
        expected_result['Count'] = [7, 5, 1]
        expected_result.index = [1, 2, 3]

        self.assertTrue(pd.DataFrame.equals(result, expected_result))

if __name__ == '__main__':
    unittest.main()
