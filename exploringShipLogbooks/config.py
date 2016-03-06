# configuration for logbook data analysis

# desired data columns for processing (will drop all other columns)
desired_columns = ['VoyageFrom', 'VoyageTo', 'ShipName', 'ShipType', 'Company',
                   'Nationality', 'WarsAndFights', 'Year']

# columns containing logbook text (to search for mentions of slaves)
text_columns = ['CargoMemo', 'LifeOnBoardMemo', 'OtherRem', 'EncRem']

# slave synonyms to search logs for
slave_words = ['slave',  'slaves', 'slaaf', 'slaven', 'meisjesslaaf', 'manslaaf',
               'manslaven', 'slavenjong','jongensslaaf', 'meidslaaf', 'servant',
               'slavenmeid', 'vrouwslaaf', 'vrouwslaven', 'slavenhandel', 'slaaf',
               'esclavo', 'esclavos', 'esclave', 'esclaves']
