import numpy as np
import pandas as pd
from . import wordCount as wc
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
import warnings

from .basic_utils import extract_logbook_data
from .basic_utils import isolate_columns
from .basic_utils import isolate_training_data
from .basic_utils import clean_data
from .basic_utils import encode_data_df
from .fuzz_replacement import fuzzy_wuzzy_classification

from .config import *


class LogbookClassifier:

    def __init__(self, classification_algorithm='Decision Tree'):

        if classification_algorithm == "Decision Tree":
            self.classifier = MultinomialNB(alpha = 1.0, class_prior = None,
                                            fit_prior = True)
        elif classification_algorithm == "Naive Bayes":
            self.classifier = tree.DecisionTreeClassifier()
        else:
            raise KeyError("Please enter a valid classification type",
                           " (Decision Trees or Naive Bayes)")

        self.classification_algorithm = classification_algorithm

    def load_data(self, data_sets = ['slave_voyages', 'cliwoc']):

        if 'slave_voyages' in data_sets:
            file_name = './exploringShipLogbooks/data/tastdb-exp-2010'
            self.slave_voyage_logs = pd.read_pickle(file_name)

        if 'cliwoc' in data_sets:
            self.cliwoc_data = extract_logbook_data('CLIWOC15.csv')

        if 'slave_voyages' not in data_sets and 'cliwoc' not in data_sets:
            warning('Warning: no data loaded. Currently data extraction is',
                  ' only implemented for cliwoc15 data (cliwoc) and slave',
                  'voyages logs (slave_voyages).')

    def find_logs_that_mention_slaves(self):
        self.slave_mask = wc.count_key_words(self.cliwoc_data, text_columns, slave_words)
        print('Found ', len(self.slave_mask[self.slave_mask==True]),
              ' logs that mention slaves')

    def find_training_data(self, criteria):
        """

        """
        self.training_mask = isolate_training_data(self.cliwoc_data, criteria)

    def encode_ship_names(self):
        label_encoding = preprocessing.LabelEncoder().fit(self.cliwoc_data['LogbookIdent']).classes_
        self.cliwoc_data['LogbookIdent'] = preprocessing.LabelEncoder().fit_transform(self.cliwoc_data['LogbookIdent'])

    def clean_and_sort_data(self):
        # set slave logs column to 0 for cliwoc data
        self.cliwoc_data['slave_logs'] = np.zeros(len(self.cliwoc_data))

        # searches all values in a voyage to determine if it contains slave mentions
        slave_log_locations = self.cliwoc_data['LogbookIdent'].isin(list(self.cliwoc_data['LogbookIdent']
                                                                         [self.slave_mask].unique()))

        # set value of slave log columns for training and validation data
        # cliwoc data (unclassified) = 0
        # cliwoc_data (no slaves) = 1
        # cliwoc_data (slaves) = 2
        # slave voyages data = 3
        self.cliwoc_data.loc[self.training_mask,'slave_logs'] = 1
        self.cliwoc_data.loc[slave_log_locations,'slave_logs'] = 2

        # sort by logbookIdent and set as index
        self.cliwoc_data = self.cliwoc_data.sort_values('LogbookIdent', ascending=True)
        self.cliwoc_data_all = self.cliwoc_data.copy.set_index('LogbookIdent', drop=False).copy()
        self.cliwoc_data = self.cliwoc_data.set_index('LogbookIdent', drop = False)
        self.cliwoc_data = self.cliwoc_data.drop_duplicates('LogbookIdent')

        # isolate desired columns from cliwoc data
        self.cliwoc_data = isolate_columns(self.cliwoc_data, desired_columns)

        # drop slave_voyage_logs with empty year column
        year_ind = ~(self.slave_voyage_logs['yeardep'].isnull())
        self.slave_voyage_logs = self.slave_voyage_logs[year_ind]

        # drop slave_voyage data from before beginning of cliwoc data
        ind = (self.slave_voyage_logs['yeardep'] > self.cliwoc_data['Year'].min()) \
            & (self.slave_voyage_logs['yeardep'] < self.cliwoc_data['Year'].max())
        self.slave_voyage_logs = self.slave_voyage_logs[ind]

        # clean slave_voyage logs to have columns that match cliwoc
        slave_voyage_desired_cols = list(slave_voyage_conversions.keys())
        self.slave_voyage_logs = isolate_columns(self.slave_voyage_logs,
                                            slave_voyage_desired_cols)

        self.slave_voyage_logs.rename(columns=slave_voyage_conversions, inplace=True)
        self.slave_voyage_logs['slave_logs'] = 3
        slave_voyage_indices = range(len(self.slave_voyage_logs)) + (self.cliwoc_data.tail(1).index[0]+1)
        self.slave_voyage_logs = self.slave_voyage_logs.set_index(slave_voyage_indices)

    def join_data(self):

        self.all_data = pd.concat([self.cliwoc_data, self.slave_voyage_logs], ignore_index=True)
        self.all_data = clean_data(self.all_data)

    def match_similar_words(self):

        fuzz_columns = ['Nationality', 'ShipType', 'VoyageFrom', 'VoyageTo']
        for col in fuzz_columns:
            self.all_data = fuzzy_wuzzy_classification(self.all_data, col)

    def encode_data(self):
        # this will use the encoder class.
        self.all_data = encode_data_df(self.all_data, self.classification_algorithm)
        # drop NaNs
        self.all_data['no_data'] = self.all_data['nan'].apply(lambda x: x.any(), axis=1).astype(int)
        self.all_data = self.all_data.drop('nan', axis=1)

    def fit_classifier(self, indexes):
        # indexes will be 1 and 3 with the current code (negative and positive
        # training data, respectively)

        classifier.fit(training_data[::,1::], classes)
        # convert to np array
        # join all masks and classes (i.e. pos and neg)
        # add what columns
        # fit data
        pass


    def validate_classifier(self, masks, desired_vals):
        pass

    def classify(self, masks):
        pass
