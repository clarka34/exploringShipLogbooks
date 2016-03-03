import zipfile

import pandas as pd

def extract_logbook_data(desired_filename):
    """
    Fetch logbook data (if needed) and extract trips as dataframe

    Input: desired_filename -- name of .csv file you would like to extract

    Output: pandas data frame containing the file or error message
    """
    try:
        zf = zipfile.ZipFile('./exploring-ship-logbooks/data/ \
                             climate-data-from-ocean-ships.zip')
        file_handle = zf.open(desired_file)
        return pd.read_csv(file_handle)
    except:
        return 'Please enter valid filename.'

if __name__ == "__main__":
    import sys
    extract_logbook_data(int(sys.argv[1]))
