import os
import urllib3

import pandas as pd

from urllib3.exceptions import MaxRetryError, LocationValueError

def download_if_needed(url, filename):
    """
    Download from URL to filename unless filename already exists
    Inputs:
        - url: url of the website where the data will be downloaded from
        - filename: name that will be given to the downloaded file
    Outputs:
        - no ouputs; saves file to specified location
    """

    # check to see if the file is already downloaded
    if os.path.exists(filename):
        filename_exists=(filename, 'already exists')
        return filename_exists

    # if the file has not been downloaded, use urllib3 to download the file
    # exceptions add for possible connection errors
    else:
        import requests
        urllib3.disable_warnings()
        try:
            connection_pool = urllib3.PoolManager(retries=urllib3.Retry(5))
            resp = connection_pool.request('GET',url,timeout=urllib3.Timeout(total=5.0))
            f = open(filename, 'wb')
            f.write(resp.data)
            f.close()
            resp.release_conn()
            download_successful=('Downloading', filename)
            return download_successful
        except MaxRetryError as e:
            exception='Could not connect to server. Please check to make sure the URL is valid and try again.'
            return exception
        except LocationValueError as e:
            exception=str(e)
            return exception
