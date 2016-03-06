import numpy as np
import pandas as pd
import word_count as wc
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB

from .basic_utils import create_widget
from .basic_utils import extract_logbook_data
from .basic_utils import remove_undesired_columns

from .config import *


class LogbookClassifier:

    def __init__(self):

        logbook_data = extract_logbook_data('CLIWOC15.csv')
        undesired_columns = remove_undesired_columns(logbook_data, desired_columns)
        logbook_data = logbook_data.drop(undesired_columns, axis=1)

        mentions_slaves = wc.count_key_words(logbook_data,
                                                text_columns, slave_words)
        slave_index = mentions_slaves[(mentions_key_words['ContainsKeyWord'] != 0)].index

        self.slave_logs = logbook_data.loc[slave_index.values]
        self.unclassified_logs = logbook_data.loc[~(slave_index.values)]

    def encode_data(self):
        """
        """
        pass

    def fit_classifier(self):
        """
        Fit training data to classifier.
        """
        pass

    def predict(self, voyages):
        """
        Predict class of remaining voyages.
        """
        for voyage in voyages:
            pass
