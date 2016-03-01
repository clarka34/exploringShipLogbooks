import os
import sys
import random
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
file_path ="C:\\Users\\Administrator\\data\\data\\CLIWOC15.csv"

def is_new_trip():
    trip_id = 1
    index = 0
    trip =[0]*len(position['Date'])
    trip[0]= trip_id
    while index < len(position['Date'])-1:
        index += 1
        if position.iat[index,8] - position.iat[index-1,8]<100 and position.iat[index,3] == position.iat[index-1,3] and position.iat[index,4] == position.iat[index-1,4]:
            trip[index] = trip_id
        else:
            trip_id += 1
            trip[index] = trip_id
    position.insert(9, "Trip", trip)
    return trip_id
if __name__ == "__main__":
    raw_data = if_data_ready(file_path)
    shipname = pd.value_counts(raw_data["ShipName"]).head(10).keys()
    i=0 #By changing this index, we can change the ship we want to research
    position = raw_data[raw_data["ShipName"]==shipname[i]][pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3","VoyageFrom","VoyageTo","Year","Month","Day","UTC"]]
    position = position.sort_values(by='UTC', ascending=True)
    position.insert(8, "Date", position['UTC'])
    position['Date'] = position['Date'] // 100
    position_list = list(zip(position["Lat3"],position["Lon3"]))
    trip_id = is_new_trip()
    #print(len(position['Date']))
    #position.to_csv("temp5.csv") 
    plt.figure(figsize=(40, 20))
    plt.xlim(-100,0)
    plt.ylim(0,50)
    colors = "rgbcmykw" ## 8 basic colors
    color = random.randint(0,7)
    for k in range(41,trip_id):  ## choose a trip_id
        color = (color+k) % 8  #choose a color number
        position_p = position[position["Trip"]==k]
        position_list = list(zip(position_p["Lat3"],position_p["Lon3"]))
        for i in position_list:
            plt.scatter(i[1], i[0],s=100,c=colors[color],alpha=0.8)
    ##This is the first step of separting the route
    plt.savefig('routes.png')
    plt.show()