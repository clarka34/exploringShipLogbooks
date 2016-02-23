"""
is_lat_unit_matters.py

By Wedward Wei

After I explore the data, I found some interesting detail. Like we have differnt types of "LongitudeUnits"
I am wondering if the latitude data could be presented in differnt ways, so we meed more steps before plot.
So I wrote this code to see if the worry is necessary.

"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
"""
If data is not ready, we need download the raw data and unzip the files in the same route
If data is ready, return the DataFrame
"""
def if_data_ready(filename):
    if os.path.exists(filename):
        print (filename+" already exist")
        return pd.read_csv(filename)
    else:
        print (filename+" does not exist, please check the file")
        sys.exit()
file_path = os.getcwd()+"\\data\\CLIWOC15.csv"
raw_data = if_data_ready(file_path)

# Show that we have differnt types of "LongitudeUnits"
print(pd.value_counts(raw_data["LongitudeUnits"])) 

raw_data_360_1 = raw_data[raw_data["LongitudeUnits"]=="360 degrees"]
raw_data_360_2 = raw_data[raw_data["LongitudeUnits"]=="360 GRADOS"]
raw_data_180_1 = raw_data[raw_data["LongitudeUnits"]=="180 degrees"]
raw_data_180_2 = raw_data[raw_data["LongitudeUnits"]=="180 GRADOS"]
position_1 = raw_data_360_1[pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3"]]
position_2 = raw_data_360_2[pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3"]]
position_3 = raw_data_180_1[pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3"]]
position_4 = raw_data_180_2[pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3"]]

#Output the 1st type of image

position_list = list(zip(position_1["Lat3"],position_1["Lon3"]))
plt.figure(figsize=(30, 15))
plt.xlim(-180,180)
plt.ylim(-70,60)
for i in position_list[:10000]: ##MAX=62324
    plt.scatter(i[1], i[0],s=15, alpha=.2)
plt.savefig('360_1.png')

#Output the 2nd type of image

plt.clf() #clear the cache
position_list = list(zip(position_2["Lat3"],position_2["Lon3"]))
plt.figure(figsize=(30, 15))
plt.xlim(-180,180)
plt.ylim(-70,60)
for i in position_list[:10000]: ##MAX=16450
    plt.scatter(i[1], i[0],s=8, alpha=.2)
plt.savefig('360_2.png')

#Output the 3rd type of image

plt.clf() #clear the cache
position_list = list(zip(position_3["Lat3"],position_3["Lon3"]))
plt.figure(figsize=(30, 15))
plt.xlim(-180,180)
plt.ylim(-70,60)
for i in position_list[:10000]: ##MAX=136133
    plt.scatter(i[1], i[0],s=8, alpha=.2)
plt.savefig('180_1.png')

#Output the 4nd type of image

plt.clf() #clear the cache
position_list = list(zip(position_4["Lat3"],position_4["Lon3"]))
plt.figure(figsize=(30, 15))
plt.xlim(-180,180)
plt.ylim(-70,60)
for i in position_list: ##MAX=1781
    plt.scatter(i[1], i[0],s=15, alpha=.2)
plt.savefig('180_2.png')

"""
After comparing the 4 images, we can reach the preliminary conclusion that,
the value in column "LongitudeUnits" does not affect the column "Lat3", so
we can use the data in Lat3" and "Lon3" directly.
"""