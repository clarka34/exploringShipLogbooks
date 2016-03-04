import sys
import os
import pandas as pd
import numpy as np

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

def is_new_trip(position,trip_id):
    index = 0
    trip = [0]*len(position['Date'])
    trip [0] = trip_id
    while index < len(position['Date'])-1:
        index += 1
        if index ==len(position['Date'])-1:
            if position.iat[index,8] - position.iat[index-1,8]<100 and position.iat[index,3] == position.iat[index-1,3] and position.iat[index,4] == position.iat[index-1,4]:
                num_data = trip.count(trip_id)
                if trip.count(trip_id) < 5:
                    for i in range(index-1, index-num_data-1, -1):
                        trip[i]=0
                    continue
                else:
                    trip[index] = trip_id
                    trip_id += 1
                    continue        
        if position.iat[index,8] - position.iat[index-1,8]<100 and position.iat[index,3] == position.iat[index-1,3] and position.iat[index,4] == position.iat[index-1,4]:
            trip[index] = trip_id
        else:
            ##delete trips that is too short
            num_data = trip.count(trip_id)
            if trip.count(trip_id) < 5:
                for i in range(index-1, index-num_data-1, -1):
                    trip[i]=0  ## the data point would be marked 0
            else:
                trip_id += 1
                trip[index] = trip_id
    position.insert(9, "Trip", trip)
    return trip_id
def split_trip():
    #shipname = pd.value_counts(raw_data["ShipName"]).head(10).keys()
    shipname = list(pd.value_counts(raw_data["ShipName"]).keys()) #949 shipnames
    shipname = [x for x in shipname if 'SAN CARLOS' not in x]
    shipname = [x for x in shipname if 'LA SUERTE' not in x] 
    shipname = [x for x in shipname if 'LABORDE' not in x]
    shipname = [x for x in shipname if 'CONOCIDO-26' not in x]
    shipname = [x for x in shipname if 'NaSa DEL ROSARIO,STMA TRINIDAD' not in x]
    shipname = [x for x in shipname if 'Vrouwe Margaretha Maria' not in x]
    shipname = [x for x in shipname if 'EL MARLLORQUÍN' not in x] 
    shipname = [x for x in shipname if 'LA ORBE' not in x]
    shipname = [x for x in shipname if 'LA JUNO' not in x]
    shipname = [x for x in shipname if 'DESCONOCIDO-01' not in x]
    shipname = [x for x in shipname if 'DESCONOCIDO-08' not in x]
    shipname = [x for x in shipname if 'DESCONOCIDO-21' not in x]
    shipname = [x for x in shipname if 'DESCONOCIDO-11' not in x]   #Some ships could cause error and need to be removed manually
    position_all = []
    trip_id = 1
    for ship in shipname:
        position = raw_data[raw_data["ShipName"]==ship][pd.notnull(raw_data["Lat3"])][pd.notnull(raw_data["Lon3"])][["Lat3","Lon3","VoyageFrom","VoyageTo","Year","Month","Day","UTC","Nationality","WarsAndFights"]]
        position = position.sort_values(by='UTC', ascending=True)
        position.insert(8, "Date", position['UTC'])
        position['Date'] = position['Date'] // 100
        #print(ship, end=" ")   ##For testing which ship got errer message
        trip_id = is_new_trip(position,trip_id)
        position_each_ship = list(zip([ship]*len(position["Lat3"]),position["Nationality"],position["VoyageFrom"],position["VoyageTo"],position["Year"],position["Date"],position["Lat3"],position["Lon3"],position["WarsAndFights"],position["Trip"]))
        position_all += position_each_ship
    return position_all
if __name__ == "__main__":
    file_path ="C:\\Users\\Administrator\\data\\data\\CLIWOC15.csv"
    raw_data = if_data_ready(file_path)
    df = pd.DataFrame(split_trip(), columns=['ShipName',"Nationality","VoyageFrom","VoyageTo","Year","Date",'Latitude', 'Longtitude', "ifWarsAndFights",'Trip'])
    df.to_excel('Trip_Data.xlsx',index=False)


            