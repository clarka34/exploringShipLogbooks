import pandas as pd
import math

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

    # initialize word count list
    word_count_list = []

    # intitialize dictionary for total word count
    word_count_total = {}
    for key_word in key_words:
        word_count_total[key_word] = 0

    # for every row in data
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
            word_count_total[key_word] += len(matches)

        # append word count to list
        word_count_list.append(word_count_dict)

    return word_count_list, word_count_total

def count_all_words(data, columns):
    """returns a dataframe containing a count of all words in the logbooks (columns in pandas dataframe
    data)
    """
    # intitialize dictionary for total word count
    word_count_dict = {}

    # for every row in data
    for index, row in data.iterrows():

        # aggregate words from each specified column
        all_words = []
        for column in columns:
            remark = row[column]

            if isinstance(remark,str):
                all_words += remark.split(' ')

        for word in all_words:
            try:
                word_count_dict[word] += 1
            except:
                word_count_dict[word] = 1

        if index == 10:
            break

    word_count_pd = pd.DataFrame(data=list(word_count_dict.items()),columns=['Word','Count'])
    word_count_pd = word_count_pd.sort(columns = 'Count', ascending = False)
    word_count_pd.index = range(1,len(word_count_pd) + 1)

    return word_count_pd
