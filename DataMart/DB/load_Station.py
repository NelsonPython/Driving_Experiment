import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
        host = "localhost",
        user = "USERNAME",
        password = "PASSWORD",
        database = "roadtrip"
)
conn = mydb.cursor()

d = pd.read_csv("data/stationSeed.csv")
df = d[["Station Name","Street Address","City","State","ZIP","Plus4", \
        "Latitude","Longitude", \
        "Date Last Confirmed", \
        "Groups With Access Code","Access Days Time", \
        "Cards Accepted","Access Code","Access Detail Code", \
        "EV Level1 EVSE Num","EV Level2 EVSE Num","EV DC Fast Count", \
        "EV Network", \
        "EV Pricing", \
        "EV Connector Types"]]

df = df.fillna(0)
print(df.info())

field_length = df["Station Name"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Station Name']
print("Station Name ", len(var))

field_length = df["Street Address"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Street Address']
print("Street Address ", len(var))

field_length = df["City"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'City']
print("City ", len(var))

field_length = df["State"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'State']
print("State ", len(var))

field_length = df["ZIP"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'ZIP']
print("Zip ", len(var))

'''
field_length = df["Plus4"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Plus4']
print("Plus4 ", len(var))

field_length = df["Latitude"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Latitude']
print("Latitude ", len(var))

field_length = df["Longitude"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Longitude']
print("Longitude ", len(var))
'''

field_length = df["Date Last Confirmed"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Date Last Confirmed']
print("Date Last Confirmed ", len(var))

field_length = df["Groups With Access Code"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Groups With Access Code']
print("Groups With Access Code ", len(var))

field_length = df["Access Days Time"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Access Days Time']
print("Access Days Time ", len(var))

field_length = df["Cards Accepted"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Cards Accepted']
print("Cards Accepted ", len(var))

field_length = df["Access Code"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Access Code']
print("Access Code ", len(var))

field_length = df["Access Detail Code"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'Access Detail Code']
print("Access Detail Code ", len(var))

'''
field_length = df["EV Level1 EVSE Num"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV Level 1 EVSE Num']
print("EV Level 1 EVSE Num ", len(var))

field_length = df["EV Level2 EVSE Num"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV Level 2 EVSE Num']
print("EV Level 2 EVSE Num ", len(var))

field_length = df["EV DC Fast Count"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV DC Fast Count']
print("EV DC Fast Count ", len(var))
'''

field_length = df["EV Network"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV Network']
print("EV Network ", len(var))

field_length = df["EV Pricing"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV Pricing']
print("EV Pricing ", len(var))

field_length = df["EV Connector Types"].astype('str').map(len)
var = df.loc[field_length.argmax(), 'EV Connector Types']
print("EV Connector Types ", len(var))



tup = []
val = []
for (idx, row) in df.iterrows():
    val.append(row["Station Name"])
    val.append(row["Street Address"])
    val.append(row["City"])
    val.append(row["State"])
    val.append(row["ZIP"])
    val.append(row["Plus4"])
    val.append(row["Latitude"])
    val.append(row["Longitude"])
    val.append(row["Date Last Confirmed"])
    val.append(row["Groups With Access Code"])
    val.append(row["Access Days Time"])
    val.append(row["Cards Accepted"])
    val.append(row["Access Code"])
    val.append(row["Access Detail Code"])
    val.append(row["EV Level1 EVSE Num"])
    val.append(row["EV Level2 EVSE Num"])
    val.append(row["EV DC Fast Count"])
    val.append(row["EV Network"])
    val.append(row["EV Pricing"])
    val.append(row["EV Connector Types"])
    strVal = ','.join('"'+str(v)+'"' for v in val)
    tup.append(strVal)
    val = []

for t in tup:
    sql = "INSERT INTO Station (station_name, station_address, station_city, station_state, zip, zip_plus4, \
lat, lng, date_last_confirmed, \
access_groups, access_days, cards_accepted, \
access_code, access_detail_code, ev_level_1_evse_num, \
ev_level_2_evse_num, ev_dc_fast_count, ev_network, ev_pricing, \
ev_connector_types) values (" + t
    sql = sql + ")"
    # print("\n", sql)

    try:
        conn.execute(sql)
        mydb.commit()
    except:
        print("\n",sql)

    #print(conn.rowcount, " record inserted")
