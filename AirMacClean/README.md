<h1>Configure Air MacClean</h1>
Make a folder in you home directory called /AirQuality and copy airMacClean.py, getIP.py, and textStatus.py.  


```
python3 airMacClean.py -ip 192.168.1.x -n 10 -t n
```

-ip must be the ip address of Public Radio

-n is the number of air quality samples

-t do you want to text the IP address of this device using IFTTT?  y or n


<h2>airMacClean.py</h2>

```
import time
import datetime
import board
import busio
import adafruit_ccs811
from statistics import mean
import argparse
import urllib.request
import getIP
import textStatus
import socket

ap = argparse.ArgumentParser()
ap.add_argument("-ip","--ipaddr", required=True,
    help = ("Start the host, get the host IP address, then type python3 senseToSocket.py -i 999.999.999.999 replacing 9s with the host ip address"))
ap.add_argument("-n","--numSamples", required=True,
    help = ("this sensor must warm up in order to accurately test air quality.  enter the number of samples to be used to compute an average of sensor readings"))
ap.add_argument("-t","--textDeviceIP", required=True,
    help = ("do you want to text the IP address of this device?  y or n"))
args = vars(ap.parse_args())

# sys args
host = args["ipaddr"]
numSamples = int(args["numSamples"])

print(host, numSamples)

# get the IP address of Public Radio
s = socket.socket()
getURL = "http://"+args['ipaddr']+"/getIP.php"
fp = urllib.request.urlopen(getURL)
host = fp.read()
host = host.decode("utf8").strip("\n")
fp.close()

# connect to Public Radio so you can send sensor readings
port = 8089
print("Host: ", host,":",port)
s.connect((host,port))
print(s.recv(1025))

# text the IP address of device
if args["textDeviceIP"] == "y":
    acIP = getIP.getIP()
    print("AirMacClean: ",acIP)
    textStatus.textStatus(acIP)

# setup air quality sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

co2 = []
tvoc = []

for k in range(numSamples):
    try:
      if not ccs811.data_ready:
          pass
      else:
          if ccs811.eco2 > 0:
              co2.append(ccs811.eco2)
              tvoc.append(ccs811.tvoc)
              print("C02 %1.0f PPM" % ccs811.eco2, end=" ")
              print("TVOC %1.0f PPB" % ccs811.tvoc)
          else:
              print("eco2==0")

    except KeyboardInterrupt:
        fo.close()
        sys.exit()
    time.sleep(3)

# get the average of the sensor readings
avgCO2 = mean(co2)
avgTVOC = mean(tvoc)
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
msg=str(round(avgCO2,0))+","+str(round(avgTVOC,0))+","+str(timestamp)
print(msg)

if args["textDeviceIP"] == "y":
    textStatus.textStatus(msg)

data= "device_name,AirMacClean,"
data = data + "CO2," + str(round(avgCO2,0))
data = data + ",TVOC," + str(round(avgTVOC,0))
data = data + ",timestamp," + timestamp
s.send((data.encode('utf-8')))
```

<h2>getIP.py</h2>

```
def getIP():
        '''
        PURPOSE:
        get the IP address of a Raspberry Pi
        attempt to connect to a known IP address

        IMPORTS:
        import socket
        '''
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
                s.connect(('192.168.1.9',1))
                IP = s.getsockname()[0]
        except:
                IP = '127.0.0.1'
        finally:
                s.close()

        return IP

if __name__=="__main__":
        getIP()
```

<h2>textStatus.py</h2>
In order to text using IFTTT, go to IFTTT.  Set up your account and copy your key into the script below.

```
import requests

def textStatus(msg):
        '''
        PURPOSE:  Text using IFTTT.com
                  you need your own API KEY
        '''
        try:
                r = requests.post(url="https://maker.ifttt.com/trigger/IP/with/key/YOUR KEY HERE", data={"value1": msg})
                print("Text status ", r.status_code, r.reason)
        except:
                print("Text status ", r.status_code, r.reason)

if __name__=="__main__":
        msg=''
        textStatus(msg)
```
