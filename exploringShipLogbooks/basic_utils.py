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

    for column in all_columns:
        if column not in desired_columns:
            df.drop(column, axis = 1)

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


class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns

    #Selects the columns that you would like to encode (if specified)
    # TODO: What does this function do?

    def fit(self,X,y=None):
       return self

    # Encodes each column and stores the encoded values
    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        output_one_hot = []
        encoding = pd.DataFrame(index=X.index,columns=X.columns)

        # Encodes only the specified columns in the function call
        if self.columns is not None:
            for col in self.columns:
                encoding[col][0:len(LabelEncoder().fit(output[col]).classes_)] = LabelEncoder().fit(output[col]).classes_
                output[col] = LabelEncoder().fit_transform(output[col])
                output_one_hot.append(OneHotEncoder().fit_transform(output[col].reshape(-1,1)).toarray())

        # Encodes all columns in the dataframe
        else:
            for col in output.columns:
                encoding[col][0:len(LabelEncoder().fit(output[col]).classes_)] = LabelEncoder().fit(output[col]).classes_
                output[col] = LabelEncoder().fit_transform(output[col])
                output_one_hot.append(OneHotEncoder().fit_transform(output[col].reshape(-1,1)).toarray())

        encoding = encoding.dropna(axis=0, how='all')
        output_one_hot = np.hstack(output_one_hot)
        return output, output_one_hot, encoding

    # Function call to combine both the fit and transform functions above
    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)
