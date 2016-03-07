# Import modules needed for the following functions
import zipfile

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
        pass
    #    raise KeyError('Please enter valid filename.')


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

    undesired_columns = determine_undesired_columns(df, desired_columns)

    df = df.drop(undesired_columns, axis = 1)

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
        undesired_columns.remove(value)

    return undesired_columns


def create_widget(df):
    """
    Creates widget to select desired columns

    Inputs:
    df -- dataframe containing logbook data

    Ouput:
    desired_columns -- columns that the user wants
    """
    w = widgets.SelectMultiple(
        description="Select desired columns",
        options=list(df.columns.values)
    )
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
            df[column] = df[column].astype(str).map(lambda x: x.lower().rstrip())
        except:
            pass

    #df['VoyageFrom'] = df['VoyageFrom'].astype(str).map(lambda x: x.lower().rstrip())
    #df['VoyageTo'] = df['VoyageTo'].astype(str).map(lambda x: x.lower().rstrip())
    #df['ShipName'] = df['ShipName'].astype(str).map(lambda x: x.lower().rstrip())
    #df['ShipType'] = df['ShipType'].astype(str).map(lambda x: x.lower().rstrip())
    #df['Company'] = df['Company'].astype(str).map(lambda x: x.lower().rstrip())
    #df['Nationality'] = df['Nationality'].astype(str).map(lambda x: x.lower().rstrip())
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
    return OneHotEncoder().fit_transform(label_encoder(column).reshape(-1,1)).toarray()

def encode_data(df):
    '''
    Transforms all columns of the dataframe specified using LabelEncoder() and
    OneHotEncoder().

    Input: df -- dataframe containing the logbook data

    Ouput: encoded_data -- dataframe containing the one hot encoded data
           encoder -- keys for the one hot encoded data
    '''
    encoded_data = []
    encoder = []
    # Encodes only the specified columns in the function call
    for col in df.columns:
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

    encoded_df = pd.DataFrame(encoded_data, columns = encoder)

    return encoded_df
