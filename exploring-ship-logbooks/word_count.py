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

    Note: a word will be counted if it contains a key word. (i.e. "captain" will
    be counted in a search for "cap")

    Outputs:
        - total_key_word_count: dictionary with number of occurences of each specified
                                key word
        - mentions_key_words: pandas data frame containing shipID (ship name + voyage
                              from + voyage to) and whether there were any mentions of
                              key words for each log

    """

    all_words = []
    mentions_slaves = []

    # for every row in data
    for index, row in data.iterrows():

        remarks = []
        # aggregate words from each specified column
        for column in columns:
            remark = row[column]
            if isinstance(remark, str):
                remarks += remark.split(' ')

        added = 0
        if remarks:
            for key_word in key_words:
                # determine if any mentions of key_words in log
                if remarks.count(key_word.upper()) and not added:
                    mentions_slaves.append(1)
                    added = 1

            if not added:
                mentions_slaves.append(0)

            all_words += remarks

        else:
            mentions_slaves.append(0)

    # generate ship ID (name of ship, home and destination for each log)
    ship_ID = data['ShipName'] + ' ' + data['VoyageFrom'] + ' ' + data['VoyageTo']

    # format pandas dataframe with ship ID and whether there are any
    # mentions of key words (boolean)
    mentions_key_words = pd.DataFrame.from_items([('ShipID', ship_ID), ('ContainsKeyWord', mentions_slaves)])

    # count total number of mentions for each key word
    # (this could help determine which words are useful, etc)
    total_key_word_count = {}
    for key_word in key_words:
        total_key_word_count[key_word] = all_words.count(key_word.upper())

    return total_key_word_count, mentions_key_words


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
            if isinstance(remark,str):
                all_words += remark.split(' ')

    word_count_dict = Counter(all_words)

    # create sorted pandas dataframe with data
    word_count_pd = pd.DataFrame(data=list(word_count_dict.items()),columns=['Word','Count'])
    word_count_pd = word_count_pd.sort(columns = 'Count', ascending = False)
    word_count_pd.index = range(1,len(word_count_pd) + 1)

    return word_count_pd

def slave_mentions_by_voyage(data, columns, key_words):
    """
    Finds the total number of logs that mention slave keywords for each unique
    voyage (identified by ship name, starting location, and end location)
    """

    total_key_word_count, mentions_key_words = count_key_words(data, columns, key_words)

    # find all unique ship IDs
    ship_IDs = mentions_key_words.ShipID.unique()

    log_mentions = []
    for index, ship_ID in enumerate(ship_IDs):
        ship_data = mentions_key_words[mentions_key_words['ShipID'] == ship_ID]
        log_mentions.append(sum(ship_data['ContainsKeyWord']))

    voyage_mentions = pd.DataFrame.from_items([('ShipID', ship_IDs), ('LogMentions',log_mentions)])

    return voyage_mentions
