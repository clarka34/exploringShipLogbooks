import pandas as pd
import math

def word_count(data, columns, key_words):
    """
    Generates a list containing the number of counts of each key word in
    each logbook entry.

    Inputs:
        - data: raw logbook data
        - columns: columns of data frame "data" to include in the search
                  (typical value is ['CargoMemo', 'LifeOnBoardMemo', 'OtherRem'])
        - key_words: words to search for.
            Note: a word will be counted if it contains a key word.
                  i.e. "captain" will be counted in a search for "cap"

    Outputs:
        - word_count_list: a list of dictionaries with the same length as data.
                           each dictionary contains an entry for each key word
                           with the number of times that word appeared in an
                           entry.

    """

    # read each row in data
    word_count_list = []
    for index, row in data.iterrows():

        # aggregate words from each specified column
        all_words = []
        for column in columns:
            remark = row[column]
            try:
                math.isnan(remark)
            except:
                all_words += remark.split(' ')

        # find number of instances of each keyword in this entry
        word_count_dict = {}
        for key_word in key_words:
            matches = [s for s in all_words if key_word.upper() in str(s)]
            word_count_dict[key_word] = len(matches)

        # append word count to list
        word_count_list.append(word_count_dict)

        # temporary break after first 100 logs to avoid
        # scanning all data during development
        if index == 100:
            break

    return word_count_list
