# Import modules needed for the following functions
import zipfile

import pandas as pd
import ipywidgets as widgets

from IPython.display import display

def extract_logbook_data(desired_filename):
    """
    Fetch logbook data and extract trips as dataframe

    Input: desired_filename -- name of .csv file you would like to extract

    Output: pandas dataframe containing the file or error message
    """
    try:
        zf = zipfile.ZipFile('./data/climate-data-from-ocean-ships.zip')
        file_handle = zf.open(desired_filename)
        return pd.read_csv(file_handle)
    except:
        return 'Please enter valid filename.'


def remove_undesired_columns(df, desired_columns):
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
