# ExploringShipLogbooks
Class project for CSE 599 to explore ship logbooks dating from 1750-1850

##Collaborators
- Emma DeWitt Cotter
- Alicia Clark
- Zehua (Wedward) Wei

## License file (MIT License)
- chosen because it is a permissive license which offers a wider user-base and developer-base
- additionally it is a GPL-compatible license

## Package Contents (exploringShipLogbooks)
- classification.py
  - contains script to pre-process all data and run classification. Two classification algorithms are implemented (using sci-kit-learn packages): Decision Trees and Multinomial Naive Bayes.
- config.py
  - Manipulate settings and options for classification and data cleaning.
- basic_utils.py
  - Functions for loading, cleaning, and encoding data.
- fuzz_replacement.py
  - Functions for fuzzy string matching
- wordcount.py
  - functions for finding specific words in logbook text.

## Data
- Two data sets are used:
  - slave_voyage_logs - A database of descriptions of trips taken by slave ships in the Atlantic ocean from the 1600's to the 1800's. A description of the data set can be found [here](http://www.slavevoyages.org/)
  - cliwoc_data - A database of transcriptions of logs from ships from 1750-1850. A description of the data set can be found [here](https://www.kaggle.com/kaggle/climate-data-from-ocean-ships)

## Project Objective
- The CLIWOC data has been well-used to study climate change and weather patterns. However, because data set is concurrent with a large portion of the Slave Voyage data, there may be information contained in the CLIWOC data that could be added to the Slave Voyages data without requiring the transcrition of additional slave logs. Because the data for both data sets was crowd-sourced, this could facilitate cross-disciplinary sharing of data without requring additional manual effort.
- The goal of the project is to classify voyages in the CLIWOC data set as either related to the slave trade or not, and visualize the results.
## Package Use
### Using the package to classify 17th century ship voyages
  - The LogbookClassifier class combines all functions to load, clean, process, and classify 17th century ship voyages as related or unrelated to the slave trade.
  - An example of how to use this functionality can be found in classifier-notebook-clean.ipynb, a Jupyter Notebook.
  - Relevant configuration parameters in config.py include:
    - text_columns - a list of column names including the columns that contain logbook text in the cliwoc data.
    - Desired columns - a list of columns that will be used for classification (except for slave_logs, which is a column used to indicate the type of the data as training, validation, or unclassified"
    - slave_words: a list of words meaning "slave" that are used to find mentions of slaves in the cliwoc ship logs data set.
    - non_slave_ships: A list of ship names used as negative training data (ships not related to the slave trade)
    - slave_voyage_conversions - a dictionary containing the conversion of column names from the slave voyages data set to the cliwoc data set. 
    - fuzz_threshold - the cutoff value for precent match when fuzzy string matching is being used.

### Using the package to match similar words in a pandas data frame
- blah blah blah

### Using the package to count instances of words in a pandas data frame
- The following functions are included in wordcount.py
  - count_key_words: This function counts instances of wors contained in the list key_words in the specified columns in a pandas data frame.
  -  count_all_words: This function counts instances of all words that are found in the specified columns in a pandas data frame.

## Future Improvements
- The poor false-positve and false-negative rates observed in the classification can be attributed to several factors:
  - We only have a small amount of negative trianing data, compoared to a large positive training data set. The performance of the classifier could likely be improved greatly by including more negative training data. This could be achieved through the addition of another data set containing descriptions of navy or merchant ships that were definitely not involved in the slave trade.
  - The logs are all in different languages, and are manually transcribed. Even after using fuzzy string matching, human error in transcription may result in similar values being classified differently. For the start and ending ports of a voyage, this problem could be resolved by using the latitude and longitude of the ports as opposed to the names of the ports.
  - The positive training data is only for ships traveling in the atlantic ocean, whereas the cliwoc data includes world-wide voyages. Analysis of the latitude and longitue of ship voyages could provide further insight.
  
