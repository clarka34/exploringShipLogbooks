import collections
import copy

import numpy as np
import pandas as pd

from fuzzywuzzy import process

from .config import fuzz_threshold


def finding_fuzzy_matches(slave_log_values, all_log_values, slave_log_values):
    matching_name = {}

    for ind, unique in enumerate(all_log_values):
        unique_values = copy.deepcopy(slave_log_values)
        if unique in unique_values:
            unique_values.remove(unique)
        matching_name[unique] = process.extract(unique, unique_values)
    return matching_name


def deleting_matches_below_threshold(threshold, my_dict):
    for key in my_dict:
        for i, match in reversed(list(enumerate(my_dict[key]))):
            match_percent = match[-1]

            if match_percent <= threshold:
                del my_dict[key][i]
    return my_dict


def matching_values(my_dict, fuzzy_df):
    for key, value in my_dict.items():
        for y in value:
            key_mask = (fuzzy_df['log_values'] == key)
            y_mask = (fuzzy_df['log_values'] == y[0])
            if ((fuzzy_df.loc[key_mask, 'count'] == 0).values[0] and
               (fuzzy_df.loc[y_mask, 'count'] == 0).values[0]):
                temp_count = fuzzy_df['count'].max()+1
                fuzzy_df.loc[key_mask, 'count'] = temp_count
                fuzzy_df.loc[y_mask, 'count'] = temp_count
            elif (fuzzy_df.loc[key_mask, 'count'] == 0).values[0]:
                fuzzy_df.loc[key_mask, 'count'] = fuzzy_df.loc[y_mask, 'count']
            elif (fuzzy_df.loc[y_mask, 'count'] == 0).values[0]:
                fuzzy_df.loc[y_mask, 'count'] = fuzzy_df.loc[key_mask, 'count']
    return fuzzy_df


def building_fuzzy_dict(fuzzy_df):
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
    my_dict = inding_fuzzy_matches(slave_log_values,
                                   all_log_values, slave_logs)

    # filter this dictionary to only include matches above a certain threshold
    my_dict = deleting_matches_below_threshold(fuzz_threshold, my_dict)

    # update the count column to assign the same count to matching strings
    fuzzy_df = matching_values(my_dict, fuzzy_df)

    # remove the values in the pandas dataframe that do not have any matches
    fuzzy_df = fuzzy_df[(fuzzy_df['count'] != 0)]

    # build the dictionary to merge the values in the original dataframe
    fuzzy_dict = building_fuzzy_dict(fuzzy_df)

    df[column] = df[column].replace(fuzzy_dict)

return df
