import numpy as np
import pandas as pd
from . import wordcount as wc
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
import warnings
import collections

from .basic_utils import extract_logbook_data
from .basic_utils import isolate_columns
from .basic_utils import isolate_training_data
from .basic_utils import clean_data
from .basic_utils import encode_data_df
from .fuzz_replacement import fuzzy_wuzzy_classification

from .config import *


class LogbookClassifier:
    """
    Handles loading, cleaning, and classification of ship logbook data.
    """
    def __init__(self, classification_algorithm='Decision Tree'):

        # initialize classifier based on desired algorithm
        if classification_algorithm == "Decision Tree":
            self.classifier = tree.DecisionTreeClassifier()
        elif classification_algorithm == "Naive Bayes":
            self.classifier = MultinomialNB(alpha=1.0, class_prior=None,
                                            fit_prior=True)
        else:
            raise KeyError("Please enter a valid classification type",
                           " (Decision Trees or Naive Bayes)")

        self.classification_algorithm = classification_algorithm

    def load_data(self, data_sets=['slave_voyages', 'cliwoc']):
        """
        Load data. All data is stored in the sub-directory "data".

        slave_voyage_logs is data from www.slavevoyages.org.
            - stored in pickle format, because website .csv file is corrupted
              and the .sav file format requires r package to read.
        cliwoc_data is data from kaggle website, collected for a NOAA project.
            - extracted from zip file
        """
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
        """
        Use word count function to find all logs in cliwoc_data that explicitly
        mention slaves in logbook text. This will later be used as a validation
        data set for classification.
        """
        self.slave_mask = wc.count_key_words(self.cliwoc_data, text_columns, slave_words)
        print('Found ', len(self.slave_mask[self.slave_mask]),
              ' logs that mention slaves')

    def find_training_data(self, criteria={'ShipName': non_slave_ships}):
        """
        Isolate training data from cliwoc_data. This training data will be used
        as negative (non-slave-trade) training data. Default is to isolate by
        ship name for ships that have been proven to be non-slave ships by
        historical research.

        Criteria is given as a dictionary with key as column name,
        and a list of desired values.
        """

        self.training_mask = isolate_training_data(self.cliwoc_data, criteria)

    def encode_ship_IDs(self):
        """
        Convert ship ID for each voyage in CLIWOC data to numerical values.
        """

        label_encoding = preprocessing.LabelEncoder().fit(self.cliwoc_data['LogbookIdent']).classes_
        self.cliwoc_data['LogbookIdent'] = preprocessing.LabelEncoder().fit_transform(self.cliwoc_data['LogbookIdent'])

    def clean_and_sort_data(self):
        """
        Cleans data sets before joining slave_voyage_logs and cliwoc_data.

        Performs the following operations:
            - adds "slave_logs" column which contains a numerical ID indicating
            - converts cliwoc_data from all logs to one entry per voyage (voyages
              determined by LogbookIdent). If any logs in a voyage mention slaves,
              the voyage is considered a slave ship (ID 2, see below)
            - the data classification. IDs are as follows:
                - 0 = unclassified data
                - 1 = negative training data (from cliwoc_data)
                - 2 = positive training/validadtion data (from cliwoc_data)
                - 3 = slave_voyages_data (positive training data)
            - Drops undesired columns from all data
            - Changes column names in slave_voyage_logs to match cliwoc data
            - Re-indexes slave_voyage_logs to start indexes after end of cliwoc_data.
              This will prevent duplicate indices after joining data sets.
        """
        # set slave logs column to 0 for cliwoc data
        self.cliwoc_data['slave_logs'] = np.zeros(len(self.cliwoc_data))

        # searches all values in a voyage to determine
        # if it contains slave mentions
        slave_log_locations = self.cliwoc_data['LogbookIdent'].isin(list(self.cliwoc_data['LogbookIdent']
                                                                         [self.slave_mask].unique()))

        # set value of slave log columns for training and validation data
        self.cliwoc_data.loc[self.training_mask, 'slave_logs'] = 1
        self.cliwoc_data.loc[slave_log_locations, 'slave_logs'] = 2

        # sort by logbookIdent and set as index
        self.cliwoc_data = self.cliwoc_data.sort_values('LogbookIdent', ascending=True)
        self.cliwoc_data_all = self.cliwoc_data.set_index('LogbookIdent', drop=False).copy()
        self.cliwoc_data = self.cliwoc_data.set_index('LogbookIdent', drop=False)
        self.cliwoc_data = self.cliwoc_data.drop_duplicates('LogbookIdent')

        # isolate desired columns from cliwoc data
        self.cliwoc_data = isolate_columns(self.cliwoc_data, desired_columns)

        # drop slave_voyage_logs with empty year column
        year_ind = ~(self.slave_voyage_logs['yeardep'].isnull())
        self.slave_voyage_logs = self.slave_voyage_logs[year_ind]

        # drop cliwoc data befor 1750 (only one instance)
        self.cliwoc_data = self.cliwoc_data[self.cliwoc_data['Year'] > 1750]
        # drop slave_voyage data from before beginning of cliwoc data
        ind = (self.slave_voyage_logs['yeardep'] > self.cliwoc_data['Year'].min()) \
            & (self.slave_voyage_logs['yeardep'] < self.cliwoc_data['Year'].max())
        self.slave_voyage_logs = self.slave_voyage_logs[ind]

        # clean slave_voyage logs to have columns that match cliwoc
        slave_voyage_desired_cols = list(slave_voyage_conversions.keys())
        self.slave_voyage_logs = isolate_columns(self.slave_voyage_logs, slave_voyage_desired_cols)
        self.slave_voyage_logs.rename(columns=slave_voyage_conversions, inplace=True)

        self.slave_voyage_logs['slave_logs'] = 3
        self.slave_voyage_indices = (range(len(self.slave_voyage_logs)) + (self.cliwoc_data.tail(1).index[0] + 1))
        self.slave_voyage_logs = self.slave_voyage_logs.set_index(self.slave_voyage_indices)

    def join_data(self):
        """
        Join cliwoc and slave_voyage_logs data sets and clean data by converting
        all strings to lower case.

        This operation should be performed after cleaning the data.
        """
        self.all_data = pd.concat([self.cliwoc_data, self.slave_voyage_logs],
                                  ignore_index=True)
        self.all_data = clean_data(self.all_data)

        del self.cliwoc_data, self.slave_voyage_logs

    def match_similar_words(self):
        """
        Uses fuzzy string comparison to match similar values in the data.

        This operation is optional, but can help to match cognates in different
        languages and eliminate typos in data transcription.

        For example, frigate (English) and fregate (Spanish) would be converted
        to the same value before classification.
        """
        fuzz_columns = ['Nationality', 'ShipType', 'VoyageFrom', 'VoyageTo']
        for col in fuzz_columns:
            self.all_data = fuzzy_wuzzy_classification(self.all_data, col)

    def encode_data(self):
        """
        Encode categorical values before classification.

        For Decision Trees classification, label encoding is used and all unique
        string values in the data are converted to unique numerical values.

        For Naive Bayes Classification, label encoding is performed followed by
        one-hot-encoding, which creates a column of boolean values for each unique
        category in the data set.

        See ski-kit-learn prepcessing documention for further description of
        encoding algorithms.
        """
        # encode data
        self.all_data = encode_data_df(self.all_data, self.classification_algorithm)

        # drop NaNs from one hot encoded data
        if self.classification_algorithm == 'Naive Bayes':
            self.all_data['no_data'] = self.all_data['nan'].apply(lambda x: x.any(), axis=1).astype(int)
            self.all_data = self.all_data.drop('nan', axis=1)

    def extract_data_sets(self, multiplier=True):
        """
        After encoding and cleaning data, extract training and validation data sets.
        """
        # extract logs to classify later
        self.unclassified_logs = self.all_data[self.all_data['slave_logs'] == 0]

        # extract first validation data set
        self.validation_set_1 = self.all_data[self.all_data['slave_logs'] == 2]

        # reserve first 20% of slave_voyage_logs as validation set 2
        validation_set_2_indices = range(self.slave_voyage_indices.min(),
                                         self.slave_voyage_indices.min() + round(len(self.slave_voyage_indices) * .2))
        self.validation_set_2 = self.all_data.iloc[validation_set_2_indices]

        # extract training data for positive and negative
        training_logs_pos = self.all_data.drop(validation_set_2_indices)
        training_logs_pos = training_logs_pos[training_logs_pos['slave_logs'] == 3]

        training_logs_neg = self.all_data[self.all_data['slave_logs'] == 1]

        # calculate multiplier to make data sets equal size
        if multiplier:
            repeat_multiplier = round(len(training_logs_pos) / len(training_logs_neg))
        else:
            # set multiplier to one if no multipler is desired
            repeat_multiplier = 1

        # create list of classes for training data
        # (0 is for non-slave, 1 is for slave)
        # index matches training_data
        training_classes = np.zeros(len(training_logs_neg)).repeat(repeat_multiplier)
        self.training_classes = np.append(training_classes,
                                          np.ones(len(training_logs_pos)))

        # join training data
        neg_rep = pd.concat([training_logs_neg] * repeat_multiplier)
        self.training_data = pd.concat([neg_rep, training_logs_pos],
                                       ignore_index=True)

        del self.all_data

    def fit_classifier(self):
        """
        Fit classifier with training data.
        """
        columns = list(self.training_data.columns)
        columns.remove('slave_logs')

        self.classifier.fit(self.training_data[columns], self.training_classes)

    def validate_classifier(self):
        """
        Determine predicted classes of validation data sets, and print results.

        For the current configuration, all validation data sets are expected to
        be positively identified as slave ships.
        """
        validation_sets = [self.validation_set_1, self.validation_set_2]

        for i, validation_set in enumerate(validation_sets):
            columns = list(validation_set.columns)
            columns.remove('slave_logs')
            predictions = self.classifier.predict(validation_set[columns])

            counts = collections.Counter(predictions)
            print('validation set', i, ' results: ', counts)

    def classify(self):
        """
        Classify remaining unclassified data and print results.
        """

        # predict class of data (for all columns except for slave_logs, which
        # will hold the classification result)
        columns = list(self.unclassified_logs.columns)
        columns.remove('slave_logs')
        predictions = self.classifier.predict(self.unclassified_logs[columns])

        # revalue slave_log ID column to indicate classification
        self.unclassified_logs['slave_logs'] = predictions + 4

        # print statstics
        counts = collections.Counter(predictions)
        for key in counts:
            percent = (counts[key] / (len(predictions)) * 100)
            print(round(percent, 2), 'of data was classified as ', key)

    def export_data(self, save_filename='classifier_results.csv'):
        """
        Export results to be plotted in Fusion Tables google app.
        """
        # assign the classifier results to the cliwoc data frame
        for val in self.unclassified_logs['slave_logs'].unique():
            ind = self.unclassified_logs[self.unclassified_logs['slave_logs'] == val].index
            self.cliwoc_data_all.loc[ind, 'slave_logs'] = val

        # isolate the columns that we would like to save
        columns = ['ShipName', 'ShipType', 'slave_logs',
                  'Nationality', 'Year', 'Lat3', 'Lon3']
        self.cliwoc_data_all = isolate_columns(self.cliwoc_data_all, columns)

        # save the altered cliwoc dataframe to a csv file
        self.cliwoc_data_all.to_csv(save_filename)

        return

    def load_clean_and_classify(self, fuzz=False, export_csv=True):
        """
        Perform all functions, and print status updates.

        Input: fuzz = boolean value, default is false. Fuzzy string matching will
                      only be performed if fuzz = True.
        """
        print("Loading data...")
        self.load_data()
        self.encode_ship_IDs()

        print("Finding ship logs that mention slaves...")
        self.find_logs_that_mention_slaves()

        print("Finding training data...")
        self.find_training_data({'ShipName': non_slave_ships})

        print("Cleaning data...")
        self.clean_and_sort_data()

        print("Joining data sets...")
        self.join_data()

        if fuzz:
            print("Matching similar string values with fuzzy wuzzy...")
            self.match_similar_words()

        print("Encoding data...")
        self.encode_data()

        print("Extracting training and validation data...")
        self.extract_data_sets()

        print("Fiting classifier...")
        self.fit_classifier()

        print("Validating Classifier...")
        print()
        self.validate_classifier()

        print("Classifing unknown data...")
        print()
        self.classify()

        if export_csv:
            print("Exporting data...")
            self.export_data()
