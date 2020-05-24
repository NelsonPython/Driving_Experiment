'''
Distance calculations
https://www.movable-type.co.uk/scripts/latlong.html
https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing

US Dept. of Energy Alternative Fuels Data Center - EV Stations
https://afdc.energy.gov/stations/#/analyze?country=US&fuel=ELEC
https://catalog.data.gov/dataset/electric-vehicle-charging-stations

Coding
https://www.dataquest.io/blog/settingwithcopywarning/

Maps
https://www.kaggle.com/asimislam/tutorial-arcgis-folium-choropleth-maps
Stamen Toner, OpenStreetMap, Stamen Terrain
'''     
import pandas as pd
import greatCircle as g
import folium
from   folium.plugins import MarkerCluster
import urllib.request

# GET TRIP GOAL FROM MOBI DATAMART
fp = urllib.request.urlopen("http://localhost/ai_getGPSCoord.php")
gpsbytes = fp.read()
goal = gpsbytes.decode("utf8").strip("\n")
fp.close()
trip = goal.split(",")
print("GET TRIP GOAL FROM MOBI DATA MART")
print("\nvehicle name: ", trip[0])
print("\ndeparture latitude: ", trip[1])
print("departure longitude: ", trip[2])
print("departure city: ", trip[3])
print("\narrival latitude: ", trip[4])
print("arrival longitude: ", trip[5])
print("arrival city: ", trip[6])
print("\nGOAL_ID for updating the number of stops: ", trip[7])

# set map type
mapType = "plan"                        # sim (simulation) or plan

# name the map
if mapType == "plan":
    routeMap = "maps/"+trip[0]+"Map.html"
else:
    routeMap = "maps/"+trip[0]+"Sim.html"

# get station data
stationData = "data/stationSeed.csv"

# get vehicle data
vehicleData = "data/KellyBlueBook.csv"

# GET STATION DATA 
pd.set_option('display.max_columns',23)
d = pd.read_csv(stationData)
df = d[["Station Name","Street Address","City","State","ZIP",
        "Latitude","Longitude",
        "Date Last Confirmed",
        "Groups With Access Code","Access Days Time",
        "Cards Accepted","Access Code","Access Detail Code",
        "EV Level1 EVSE Num","EV Level2 EVSE Num","EV DC Fast Count",
        "EV Network",
        "EV Pricing",
        "EV Connector Types"]]
minLat = df["Latitude"].min()
maxLat = df["Latitude"].max()


# GET VEHICLE DATA
v = pd.read_csv(vehicleData)


# COMPUTE DISTANCE
tripDistance = int(g.Haversine(float(trip[1]),float(trip[2]),float(trip[4]),float(trip[5])))
if float(trip[1]) - float(trip[4]) > 0:
    bearing = 160
else:
    bearing = -35

vehicleRange = v["VEHICLE_RANGE"].loc[v["VEHICLE"]==trip[0]].item()
vehicleRange80 = float(vehicleRange) * 0.80

# PRINT THE ROUTE
# Assumptions:
#       use 80% of the vehicle's range because driving conditions may require more or less fuel and fast charging stations report refueling to 80% of capacity
#       one additional fueling stop is calculated so drivers do not arrive at their destination low on fuel 

outputString = "<h2>ROUTE</h2>"
outputString += "<br>Vehicle: "+trip[0]
outputString += "<br>Starting location: "+trip[3]
outputString += "<br>Destination: "+trip[6]

outputString += "<br><br>Assumptions:  use 80% of a vehicle's range because many battery chargers report re-charging to 80% capacity<br><br>"
outputString += trip[0] + " has a range of " + str(vehicleRange) + " miles. The range used for route planning is 80% or "+ str(int(vehicleRange80)) + " miles"

EV_adapter = v["ADAPTER"].loc[v["VEHICLE"]==trip[0]].item()
EV_network = v["NETWORK"].loc[v["VEHICLE"]==trip[0]].item()
EV_charger = v["CHARGE_TYPE"].loc[v["VEHICLE"]==trip[0]].item()
if "J1772" in EV_adapter: 
        EV_adapter = "J1772"

outputString += "<br><br>Vehicle adapter: " + EV_adapter
outputString += "<br>Vehicle network: " + EV_network
outputString += "<br>Vehicle charger: " + EV_charger

outputString += "<br><br>Trip Distance " + str(tripDistance) + " miles"
numStops = round(tripDistance / vehicleRange80,0)
outputString += "<br>Number of refueling stops between " + trip[3] + " and " + trip[6] + ": " + str(int(numStops))

# UPDATE DATABASE WITH numStops
import mysql.connector

db = mysql.connector.connect(
        host = "localhost",
        user = "py",
        password = "admin1234",
        database = "roadtrip"
)

conn = db.cursor()

sql = "UPDATE goal SET NUM_FUEL_STOPS = "+ str(int(numStops)) +"  WHERE GOAL_ID = "+ str(trip[7])
conn.execute(sql)
db.commit()

print("\n", conn.rowcount, " record inserted")

# DEPARTING...
lat = trip[1]
lng = trip[2]

departMsg = "Depart: " + trip[3]
outputString += "<br><br>" + departMsg
# Setup the lists needed for drawing the map
Location =  [departMsg]
Latitude  = [float(lat)]
Longitude = [float(lng)]

for numStop in range(int(numStops)):

    outputString += "<br><br>GPS COORDINATES: " + str(lat) +","+ str(lng)

    print("GPS DISTANCE: ", lat, lng, str(int(vehicleRange80)), bearing)

    lat2, lng2 = g.GPSplusDistance(float(lat),float(lng),int(vehicleRange80),bearing)

    # find fueling stations between +/- 1 of the latitude because we are driving north and south on I5 
    ev = df.loc[df["Latitude"].between(lat2-1, lat2+1, inclusive=False)].copy()
    ev = ev.fillna(0)
    # drop EV connector types that don't match the vehicle adapter
    ev.drop(ev.loc[~ev["EV Connector Types"].str.contains(EV_adapter)].index, inplace=True)
    # drop stations that are not public
    ev.drop(ev.loc[~ev["Access Code"].str.contains("public")].index, inplace=True)
    # drop stations that are not open 24 hours
    ev.drop(ev.loc[~ev["Access Days Time"].str.contains("24")].index, inplace=True)
    # sort by the station with the most fast chargers
    ev.sort_values(by=['EV DC Fast Count'], ascending=False, inplace=True)
    # TODO - find closest longitude?

    if ev.empty:
            # if the computed latitude is beyond the station list then the vehicle will arrive with fuel
            if lat2 > maxLat or lat2 < minLat:
                break
            else:
                outputString += "<br>There are no stations at the next GPS coordinates:"+ str(lat2)+","+str(lng2)
            break
    else:
            outputString += "<br>DRIVE TO: " + str(ev["Latitude"].head(1).item())+","+str(ev["Longitude"].head(1).item())
            outputString += "<br>STOP "+str(numStop+1)+" CHARGE BATTERY AT:<br>"

            cols = ["Station Name","Street Address","City","State","ZIP"]
            for col in cols:
                outputString += " "+ str(ev[col].head(1).item())

            cols = ["Access Code","Access Days Time","Cards Accepted","Groups With Access Code",
                    "EV Level1 EVSE Num","EV Level2 EVSE Num","EV Network","EV Connector Types","EV DC Fast Count",
                    "EV Pricing"]
            for col in cols:
                outputString += "<br><b>"+col+ ":</b>  "+ str(ev[col].head(1).item())

    lat = ev["Latitude"][0:1].item()
    lng = ev["Longitude"][0:1].item()

    # get data for the map
    stationData = "Refuel: " + ev["City"].head(1).item()+" "+ev["State"].head(1).item()+"<br>"+ev["Station Name"].head(1).item()+" Fast DC: "+ str(ev["EV DC Fast Count"].head(1).item())
    Location.append(stationData)
    Latitude.append(lat)
    Longitude.append(lng)

arriveMsg = "ARRIVE: "+ trip[6]
outputString += "<br><br>" + arriveMsg + "<br>"
Location.append(arriveMsg)
Latitude.append(float(trip[4]))
Longitude.append(float(trip[5]))


# MAP PLANNED ROUTE
sm = pd.DataFrame(columns = {'Location','Latitude','Longitude'})
sm.columns = ['Location','Latitude','Longitude']
sm['Location']  = Location
sm['Latitude']  = Latitude
sm['Longitude'] = Longitude

#  center map on mean of Latitude/Longitude
if mapType == 'sim':
    map_world = folium.Map(location=[sm.Latitude.mean(), sm.Longitude.mean()], tiles = 'Stamen Toner', zoom_start = 5)
    fillColor = 'yellow'
elif mapType == 'plan':
    map_world = folium.Map(location=[sm.Latitude.mean(), sm.Longitude.mean()], tiles = 'OpenStreetMap', zoom_start = 5)
    fillColor = 'green'
else:
    print("I don't know this map type")

#  add Locations to map
for lat, lng, label in zip(sm.Latitude, sm.Longitude, sm.Location):
    folium.CircleMarker(
        [lat, lng],
        radius=8,
        popup=label,
        fill=True,
        color='Blue',
        fill_color=fillColor,
        fill_opacity=0.6
        ).add_to(map_world)

#  save map to local machine, open in any browser
map_world.save(routeMap)

h = open(routeMap, "a")
print(outputString,file=h)
h.close()
print("Map and itinerary at: ", routeMap)
