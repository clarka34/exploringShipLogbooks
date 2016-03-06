# Import modules needed for the following functions
import zipfile

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

    all_columns = df.columns.values.tolist()
    drop_columns = []
    for column in all_columns:
        if column not in desired_columns:
            drop_columns.append(column)

    df.drop(drop_columns, axis = 1)

    return df


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

def label_encoder(column):
    return LabelEncoder().fit_transform(column)

def one_hot_encoder(column):
    return OneHotEncoder().fit_transform(label_encoder(column).reshape(-1,1)).toarray()

def encode_data(df):
    '''
    Transforms all columns of the dataframe specified using
    LabelEncoder() and OneHotEncoder().
    '''
    encoded_data = []

    # Encodes only the specified columns in the function call
    for col in df.columns:
        encoded_data.append(one_hot_encoder(df[col]))

    encoded_data = np.hstack(encoded_data)
    return encoded_data
