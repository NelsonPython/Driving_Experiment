'''
kou, ri, mu, charging, charged, drive,  arrive, fear
'''
import socket
import argparse
import mysql.connector

ap = argparse.ArgumentParser()
ap.add_argument("-m","--msg", required=True, \
	help="kou, ri, mu, charging, charged, drive, arrive, fear")
args = vars(ap.parse_args())

# get the IP address for AstroPiQuake LED
db = mysql.connector.connect(
        host = "localhost",
        user = "py",
        password = "admin1234",
        database = "roadtrip"
)
conn = db.cursor()
conn.execute("SELECT ipAddr from labDevices where macAddr = 'b8:27:eb:e1:a2:5b'")
res = conn.fetchall()
for r in res:
	host = r[0]

s = socket.socket()
port = 8088
print(host, port)
s.connect((host,port))
print(s.recv(1025))
s.send(args["msg"].encode('utf-8'))
print(args["msg"], " sent to LED")
s.close()
