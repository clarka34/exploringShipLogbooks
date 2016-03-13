import pandas as pd
from collections import Counter


def count_key_words(data, columns, key_words):
    """
    Generates a list containing the number of counts of each key word in
    each logbook entry.

    Inputs:
        - data: raw logbook data
        - columns: columns of data frame "data" to include in the search
                (typical value is ['CargoMemo', 'LifeOnBoardMemo', 'OtherRem'])
        - key_words: words to search for.

    Outputs:
        - total_key_word_count: dictionary with number of occurences of each
                                specified key word
        - mentions_key_words: pandas data frame containing ship info (ship name
                              + voyage from + voyage to) and whether there were
                              any mentions of key words for each log
    """

    mentions_slaves = []

    # for every row in data
    for index, row in data.iterrows():

        remarks = []
        # aggregate words from each specified column
        for column in columns:
            remark = row[column]
            if isinstance(remark, str):
                remark = remark.upper()
                remarks += remark.split(' ')

        added = 0
        if remarks:
            for key_word in key_words:
                # determine if any mentions of key_words in log
                if remarks.count(key_word.upper()) and not added:
                    mentions_slaves.append(1)
                    added = 1
                    break
            if not added:
                mentions_slaves.append(0)

        else:
            mentions_slaves.append(0)

    # format pandas dataframe with ship ID and whether there are any
    # mentions of key words (boolean)
    slave_mask = (pd.Series(mentions_slaves) != 0)

    return slave_mask


def count_all_words(data, columns):
    """returns a dataframe containing a count of all words in the logbooks
    (columns in pandas dataframe data)
    """

    all_words = []

    # for every row in data
    for index, row in data.iterrows():

        # aggregate words from each specified column
        for column in columns:
            remark = row[column]
            if isinstance(remark, str):
                all_words += remark.split(' ')

    word_count_dict = Counter(all_words)

    # create sorted pandas dataframe with data
    word_count_pd = pd.DataFrame(data=list(word_count_dict.items()),
                                 columns=['Word', 'Count'])
    word_count_pd = word_count_pd.sort(columns='Count', ascending=False)
    word_count_pd.index = range(1, len(word_count_pd) + 1)

    return word_count_pd
