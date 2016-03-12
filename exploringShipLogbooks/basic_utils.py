import zipfile
import warnings
import numpy as np
import pandas as pd
import ipywidgets as widgets

from IPython.display import display
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


def extract_logbook_data(desired_filename):
    """
    Fetch logbook data and extract trips as dataframe

    Input: desired_filename -- name of .csv file you would like to extract

    Output: pandas dataframe containing the file or error message
    """
    try:
        zf = zipfile.ZipFile('./exploringShipLogbooks/data/climate-data-from-ocean-ships.zip')
        file_handle = zf.open(desired_filename)
        return pd.read_csv(file_handle)
    except:
        raise KeyError('Please enter valid filename.')


def isolate_columns(df, desired_columns):
    """
    Removes undesired columns from the data set

    Inputs:
    df -- dataframe containing logbook data
    desired_columns -- columns that user wants to user
    -- formatted as w.value (where w is the output of creating_widget)


    Ouput:
    unwanted_columns -- columns that the user does not want
    """

    # Initializes list of all columns and then removes the desired columns
    # from the list

    undesired_columns = remove_undesired_columns(df, desired_columns)

    df = df.drop(undesired_columns, axis=1)

    return df


def remove_undesired_columns(df, desired_columns):
    """
    Determines undesired columns from the data set
    Inputs:
    df -- dataframe containing logbook data
    desired_columns -- columns that user wants to user
    -- formatted as w.value (where w is the output of creating_widget)
    Ouput:
    unwanted_columns -- columns that the user does not want
    """

    # Initializes list of all columns and then removes the desired columns
    # from the list

    undesired_columns = list(df.columns.values)

    for value in desired_columns:
        try:
            undesired_columns.remove(value)
        except:
            warnings.warn('Column not found')

    return undesired_columns


def create_widget(df):
    """
    Creates widget to select desired columns

    Inputs:
    df -- dataframe containing logbook data

    Ouput:
    desired_columns -- columns that the user wants
    """
    w = widgets.SelectMultiple(description="Select desired columns",
                               options=list(df.columns.values))

    display(w)

    button = widgets.Button(description="Done!")
    display(button)

    def on_button_clicked(b):
        w.close()
        button.close()

    button.on_click(on_button_clicked)

    return w


def clean_data(df):
    """
    Makes all the data lower case and also strips the white space from the end
    of each entry

    Input: df -- dataframe containing the logbook data

    Ouput: df -- dataframe containing the cleaned data
    """
    for column in list(df.columns.values):
        try:
            if not ((df[column].dtypes == 'int') or
                    (df[column].dtypes == 'float')):
                df[column] = df[column].astype(str).map(lambda x: x.lower().
                                                        rstrip())
        except:
            pass

    return df


def label_encoder(column):
    """
    Converts categorical data to numerical data
    """
    return LabelEncoder().fit_transform(column)


def label_encoder_key(column):
    """
    Key for the conversion of categorical data to numerical data
    """
    return LabelEncoder().fit(column).classes_


def one_hot_encoder(column):
    """
    Converts numerical data to one hot encoded data
    """
    return OneHotEncoder().fit_transform(label_encoder(column).
                                         reshape(-1, 1)).toarray()


def encode_data(df, classification_algorithm):
    '''
    Transforms all columns of the dataframe specified using LabelEncoder() and
    OneHotEncoder(). Performs one hot encoding only if classification_algorithm
    is naive_bayes. Otherwise, only LabelEncoder is used.

    Input: df -- dataframe containing the logbook data

    Ouput: encoded_data -- dataframe containing the one hot encoded data
           encoder -- keys for the one hot encoded data
    '''
    encoded_data = []
    encoder = []

    for col in df.columns:
        # if type is string?
        if (df[col].dtype == 'int') or (df[col].dtype == 'float'):
            encoded_data.append(np.array([df[col]]).T)
            encoder.append(col)
        else:
            if classification_algorithm == 'Decision Tree':
                encoded_data.append(label_encoder(df[col]))
                encoder.append(label_encoder_key(df[col]))
            elif classification_algorithm == 'Naive Bayes':
                encoded_data.append(one_hot_encoder(df[col]))
                encoder.append(label_encoder_key(df[col]))

    encoded_data = np.hstack(encoded_data)
    encoder = np.hstack(encoder)
    return encoded_data, encoder


def encode_data_df(df):
    '''
    Creates a pandas dataframe of the encoded date with each column labelled

    Input: df -- dataframe containing the logbook data

    Output: encoded_df -- dataframe containing the encoded data
    '''

    encoded_data, encoder = encode_data(df)

    encoded_df = pd.DataFrame(encoded_data, columns=encoder)

    return encoded_df


def isolate_training_data(df, criteria):
    """
    Isolates data from the data frame (df) that meets criteria

    Criteria is a dictionary with key name of the column name,
    and a list of permissible values.

    NOTE: currently only works for one column name at a time

    i.e {'Nationality":['dutch', 'french']} would isolate all dutch
    and french logs.
    """

    for col in criteria:
        # clean relevant columns
        try:
            if not ((df[col].dtypes == 'int') or (df[col].dtypes == 'float')):
                df[col] = df[col].astype(str).map(lambda x: x.lower().rstrip())
        except:
            pass
        # find rows with desired values
        desired_vals = criteria[col]
        mask = df[col].isin(desired_vals)

    return mask
