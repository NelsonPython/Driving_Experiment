import mysql.connector
import pandas as pd

# setup database connection and cursor
mydb = mysql.connector.connect(
	host = "localhost",
	user = "USERNAME",
	passwd = 'PASSWORD',
	database = 'roadtrip'
)
mycursor = mydb.cursor()

v = pd.read_csv("data/KellyBlueBook.csv")
v = v.fillna(0)
v["VEHICLE"] = v["VEHICLE"].astype('str')
v["VEHICLE_RANGE"] = v["VEHICLE_RANGE"].astype('str')
v["CHARGE_TIME_240V"] = v["CHARGE_TIME_240V"].astype('str')
v["ADAPTER"] = v["ADAPTER"].astype('str')
v["CHARGE_TYPE"] = v["CHARGE_TYPE"].astype('str')
v["NETWORK_NAME"] = v["NETWORK"].astype('str')
v["VEHICLE_WEBSITE"] = v["WEBSITE"].astype('str')

#val = v[["VEHICLE", "VEHICLE_RANGE", "CHARGE_TIME_240V", "ADAPTER", "CHARGE_TYPE", "NETWORK_NAME", "VEHICLE_WEBSITE"]].to_records(index=False)
#val = list(val)
#print(type(val))

sql = "INSERT INTO KellyBlueBook (vehicle, vehicle_range, charge_time_240v, adapter, charge_type, network_name, vehicle_website) \
values (%s, %s, %s, %s, %s, %s, %s)"

val = [('economy', '226', '11.5', 'CHAdeMO J1772', 'DC', 'Chargepoint', \
'https://www.nissanusa.com/vehicles/electric-cars/leaf/features/range-charging-battery.html'), \
('sports', '370', '1.5', 'J1772 with Tesla adapter', 'Level2 DC', 'Chargepoint EVConnect', 'https://www.tesla.com/models'), \
('semi', '250', '1.5', 'J1772', 'DC', 'Chargepoint', 'https://freightliner.com/e-mobility/'), \
('Nissan Leaf Plus', '226', '11.5', 'CHAdeMO J1772', 'DC', 'Chargepoint', \
'https://www.nissanusa.com/vehicles/electric-cars/leaf/features/range-charging-battery.html'), \
('Tesla Model S', '370', '1.5', 'J1772 with Tesla adapter', 'Level2 DC', 'Chargepoint EVConnect', \
'https://www.tesla.com/models'), \
('Freightliner eCascadia Semi', '250', '1.5', 'J1772', 'DC', 'Chargepoint', 'https://freightliner.com/e-mobility/'), \
('Audi e-tron', '204', '8.0', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Jaguar I-Pace', '234', '12.9', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Chevrolet Bolt EV', '238', '9.5', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Kia Niro EV', '239', '9.5', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Kia Soul EV', '243', '9.5', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Hyundai Kona Electric', '258', '9.5', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Tesla Model 3', '310', '11.0', 'unknown', 'unknown', 'unknown', 'unknown'), \
('Tesla Model X', '325', '10.0', 'unknown', 'unknown', 'unknown', 'unknown')]

mycursor.executemany(sql,val)
mydb.commit()
print(mycursor.rowcount, " record inserted")
