import numpy as np
import pandas as pd
from . import wordCount as wc
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB

from .basic_utils import extract_logbook_data
from .basic_utils import isolate_columns
from .basic_utils import isolate_training_data
from .basic_utils import clean_data

from .config import *


class LogbookClassifier:

    def __init__(self):
        self.classifier = MultinomialNB(alpha=1.0,
                                        class_prior=None,
                                        fit_prior=True)

    def load_data(self, data_sets):

        if 'slave_voyages' in data_sets:
            file_name = './exploringShipLogbooks/data/tastdb-exp-2010'
            self.slave_voyage_logs = pd.read_pickle(file_name)

        if 'cliwoc' in data_sets:
            self.cliwoc_data = extract_logbook_data('CLIWOC15.csv')

        if 'slave_voyages' not in data_sets and 'cliwoc' not in data_sets:
            print('Warning: no data loaded. Currently data extraction is',
                  ' only implemented for cliwoc15 data (cliwoc) and slave',
                  'voyages logs (slave_voyages).')

    def find_logs_that_mention_slaves(self):
        self.slave_mask = wc.count_key_words(self.cliwoc_data, text_columns, slave_words)

    def find_training_data(self, criteria):
        """

        """
        self.training_mask = isolate_training_data(self.cliwoc_data, criteria)

    def encode_ship_names(self):
        label_encoding = preprocessing.LabelEncoder().fit(self.cliwoc_data['LogbookIdent']).classes_
        self.cliwoc_data['LogbookIdent'] = preprocessing.LabelEncoder().fit_transform(self.cliwoc_data['LogbookIdent'])

    def join_data(self):
        self.cliwoc_data['slave_logs'] = np.zeros(len(self.cliwoc_data))
        slave_log_locations = self.cliwoc_data['LogbookIdent'].isin(list(self.cliwoc_data['LogbookIdent']
                                                                         [self.slave_mask].unique()))

        # cliwoc data (unclassified) = 0
        # cliwoc_data (no slaves) = 1
        # cliwoc_data (slaves) = 2
        # slave voyages data = 3
        self.cliwoc_data.loc[self.training_mask,'slave_logs'] = 1
        self.cliwoc_data.loc[slave_log_locations,'slave_logs'] = 2

        self.cliwoc_data = self.cliwoc_data.sort_values('LogbookIdent', ascending=True)
        self.cliwoc_data = self.cliwoc_data.drop_duplicates('LogbookIdent')
        self.cliwoc_data = self.cliwoc_data.set_index('LogbookIdent')

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

        self.all_data = pd.concat([self.cliwoc_data, self.slave_voyage_logs], ignore_index=True)
        self.all_data = clean_data(self.all_data)


    def encode_data(self):
        # this will use the encoder class.
        pass

    def fit_classifier(self, masks, classes):
        # convert to np array
        # join all masks and classes (i.e. pos and neg)
        # add what columns
        # fit data
        pass


    def validate_classifier(self, masks, desired_vals):
        pass

    def classify(self, masks):
        pass
