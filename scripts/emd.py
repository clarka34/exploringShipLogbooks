import os
import sys
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from emd import emd

"""
To use emd function, we need to install pyemd package on your machine first. (Windows machine may not supported)

https://github.com/garydoranjr/pyemd

"""
def if_data_ready(filename):
    if os.path.exists(filename):
        print (filename+" already exist")
        return pd.read_excel(filename)
    else:
        print (filename+" does not exist, please check the file")
        sys.exit()
      
def get_trip_data(trip_id,data):
    trip_data = data[data["Trip"]==trip_id].loc[:,("Lat3","Lon3")]
    trip_p = []
    for i in range(len(trip_data["Lat3"])):
        trip_p.append([trip_data.iat[i,0],trip_data.iat[i,1]])
    return trip_p
def trip_plot(trip_id,data):
    plt.figure(figsize=(20, 10))
    plt.xlim(-100,0)
    plt.ylim(0,50)
    colors = "rgbcmykw" ## 8 basic colors
    color = random.randint(0,7)
    color = (color + trip_id) % 8  #choose a color number
    position_list= get_trip_data(trip_id,data)
    for i in position_list:
        plt.scatter(i[1], i[0],s=40,c=colors[color],alpha=0.8)
    ##This is the first step of separting the route
    #plt.savefig('routes.png')
    plt.show()
  
if __name__ == "__main__":
    processed_data = if_data_ready("trip_data.xlsx") # Change the filename if necessary
    #trip_plot(1,processed_data)
    #trip_plot(2,processed_data)
    print emd(get_trip_data(1,processed_data),get_trip_data(2,processed_data))
    print emd(get_trip_data(1,processed_data),get_trip_data(3,processed_data))