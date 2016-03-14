import collections
import copy

import numpy as np
import pandas as pd

from fuzzywuzzy import process

from .config import *


def finding_fuzzy_matches(all_log_values, slave_log_values):
    """
    Extracts the top 5 fuzzy matches from slave_log_values for each value
    in all_log_values

    Inputs: all_log_values -- unique values in a column in the combined
                              datasets
            slave_log_values -- unique values in a column for the slave logs
                                dataset

    Output: matching_name -- a dictionary containing the fuzzywuzzy results
    """
    matching_name = {}

    for ind, unique in enumerate(all_log_values):
        unique_values = copy.deepcopy(slave_log_values)
        if unique in unique_values:
            unique_values.remove(unique)
        matching_name[unique] = process.extract(unique, unique_values)
    return matching_name


def deleting_matches_below_threshold(threshold, my_dict):
    """
    Deletes the fuzzy matches below a certain set threshold

    Inputs: threshold -- threshold value for matching strings set in config.py
            my_dict -- dictionary containing fuzzywuzzy matches

    Output: my_dict -- dictionary containing fuzzywuzzy matches above a
                        certain threshold
    """
    for key in my_dict:
        for i, match in reversed(list(enumerate(my_dict[key]))):
            match_percent = match[-1]

            if match_percent <= threshold:
                del my_dict[key][i]
    return my_dict


def matching_values(my_dict, fuzzy_df):
    """
    Finds all the strings that match

    Inputs: my_dict -- dictionary containing fuzzywuzzy matches above a
                        certain threshold
            fuzzy_df -- dataframe to help with fuzzywuzzy matching

    Output: fuzzy_df -- dataframe to help with fuzzywuzzy matching with numbers
                        for each matching string
    """
    # Sets the same value for each key in the dictionary and the matching
    # strings contained in the key's values
    for key, value in my_dict.items():
        for y in value:
            key_mask = (fuzzy_df['log_values'] == key)
            y_mask = (fuzzy_df['log_values'] == y[0])
            if ((fuzzy_df.loc[key_mask, 'count'] == 0).values[0] and
               (fuzzy_df.loc[y_mask, 'count'] == 0).values[0]):
                temp_count = fuzzy_df['count'].max() + 1
                fuzzy_df.loc[key_mask, 'count'] = temp_count
                fuzzy_df.loc[y_mask, 'count'] = temp_count
            elif (fuzzy_df.loc[key_mask, 'count'] == 0).values[0]:
                fuzzy_df.loc[key_mask, 'count'] = fuzzy_df.loc[y_mask, 'count']
            elif (fuzzy_df.loc[y_mask, 'count'] == 0).values[0]:
                fuzzy_df.loc[y_mask, 'count'] = fuzzy_df.loc[key_mask, 'count']
    return fuzzy_df


def building_fuzzy_dict(fuzzy_df, slave_log_values):
    """
    Builds another dictionary to replace matching values with the corresponding
    matching string value in the pandas dataframe

    Inputs: fuzzy_df -- dataframe to help with fuzzywuzzy matching with numbers
                        for each matching string
            slave_log_values -- unique values in a column for the slave logs
                                dataset

    Output: fuzzy_dict -- dictionary to replace matching values with the
                          corresponding matching string value in the pandas
                          dataframe
    """
    alist = []
    for count in fuzzy_df['count'].unique():
        s_ind = fuzzy_df['log_values'][fuzzy_df['count'] ==
                                       count].isin(slave_log_values)
        key = s_ind.index[~s_ind].tolist()
        value = s_ind.index[s_ind].tolist()
        adict = {el: fuzzy_df['log_values'].loc[value].tolist() for el
                 in fuzzy_df['log_values'].loc[key].tolist()}
        alist.append(adict)

    fuzzy_dict = collections.defaultdict(list)

    for d in alist:
        for k, v in d.items():
            fuzzy_dict[k].append(v)

    return fuzzy_dict


def fuzzy_wuzzy_classification(df, column):
    """
    Runs fuzzy string matching on selected column of a pandas dataframe
    and returns the same dataframe with the matching strings renamed with the
    corresponding matching value contained in the slave logs dataset

    Inputs: df -- dataframe containing the cliwoc dataset and the slave logs
                  dataset
            column -- column to run fuzzywuzzy string matching on

    Output: df -- dataframe containing the cliwoc dataset and the slave logs
                  dataset with the fuzzywuzzy string matching
    """
    slave_log_indices = (df['slave_logs'] == 3)
    slave_log_values = list(df[column][slave_log_indices].unique())
    all_log_values = list(df[column].unique())

    # create dataframe to store matching values
    fuzzy_array = np.concatenate(([all_log_values],
                                  [np.zeros(len(all_log_values), dtype=int)]))
    fuzzy_df = pd.DataFrame(fuzzy_array,
                            index=['log_values', 'count']).transpose()
    fuzzy_df['count'] = fuzzy_df['count'].astype(int)

    # create dictionary of fuzzy matches
    my_dict = finding_fuzzy_matches(all_log_values, slave_log_values)

    # filter this dictionary to only include matches above a certain threshold
    my_dict = deleting_matches_below_threshold(fuzz_threshold, my_dict)

    # update the count column to assign the same count to matching strings
    fuzzy_df = matching_values(my_dict, fuzzy_df)

    # remove the values in the pandas dataframe that do not have any matches
    fuzzy_df = fuzzy_df[(fuzzy_df['count'] != 0)]

    # build the dictionary to merge the values in the original dataframe
    fuzzy_dict = building_fuzzy_dict(fuzzy_df, slave_log_values)

    if any(fuzzy_dict):
        df[column] = df[column].replace(fuzzy_dict)

    return df
