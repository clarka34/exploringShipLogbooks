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
        - word_count_list: a list of dictionaries with the same length as data.
                           each dictionary contains an entry for each key word
                           with the number of times that word appeared in an
                           entry.

    """

    all_words = []

    # for every row in data
    for index, row in data.iterrows():

        # aggregate words from each specified column
        for column in columns:
            remark = row[column]
            if isinstance(remark,str):
                all_words += remark.split(' ')

    # count each key word
    key_word_count = {}
    for key_word in key_words:
        key_word_count[key_word] = all_words.count(key_word.upper())

    return key_word_count

from collections import Counter

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

    word_count_pd = pd.DataFrame(data=list(word_count_dict.items()),columns=['Word','Count'])
    word_count_pd = word_count_pd.sort(columns = 'Count', ascending = False)
    word_count_pd.index = range(1,len(word_count_pd) + 1)

    return word_count_pd
