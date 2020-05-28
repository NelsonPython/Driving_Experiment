<h1>Configuring AstroPiQuake to Drive I-5</h1>



<b>AstroPiQuake rides onboard Bumblebee AV broadcasting messages and gathering environment data</b>

If you have not built your own AstroPiQuake, follow these [instructions](https://github.com/NelsonPython/AstroPiQuake).  Set up the Drive I-5 experiment by making a folder in your home directory called /quake.  Copy sensorTosocket.py and emoji.py into the quake folder.  Run each script is a separate PuTTY session.

```
python3 sensorTosocket.py -ip 192.168.1.x
```

-ip must be the ip address of Public Radio


<h2>sensorTosocket.py</h2>
This script gets sensor readings and sends them to the Public Radio announcer.  It also draws emojis in different colors depending on the temperature and humidity readings.

```
#!/usr/bin/python

'''
Purpose: send sensor data to Public Radio

Notes:
- this script assumes there is no DNS server so devices connect directly to the ip address of the website
- this script communicates through raw sockets
'''

import argparse
import socket
import time
import datetime
import urllib.request
from sense_hat import SenseHat

ap = argparse.ArgumentParser()
ap.add_argument("-ip","--ipaddr", required=True, help = ("get IP address of the website"))
args = vars(ap.parse_args())

def smiley(faceColor, sense):
        E = [0,0,0]
        I = faceColor;
        i_pixels = [
                E,E,I,I,I,I,E,E,
                E,I,I,I,I,I,I,E,
                I,I,E,I,I,E,I,I,
                I,I,I,I,I,I,I,I,
                I,I,E,I,I,E,I,I,
                I,I,I,E,E,I,I,I,
                E,I,I,I,I,I,I,E,
                E,E,I,I,I,I,E,E,
        ];
        sense.set_pixels(i_pixels)

def humidity(A,I,Q,sense):
        # palm tree design
        
        R=[0,50,0]
        S=[0,100,0]
        T=[105,53,15]
        U=[122,82,25]
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,R,R,Q,Q,
                Q,Q,S,S,R,R,R,Q,
                I,S,S,S,R,R,R,I,
                I,S,S,I,U,I,R,I,
                I,S,I,I,T,I,I,I,
                A,A,A,A,U,A,A,A,
                A,A,A,A,T,A,A,A,
        ];
        sense.set_pixels(i_pixels)

def getSensorData(sense):
        sensors = {}
        sensors["pressure"] = str(sense.get_pressure())
        sensors["temperature"] = str(sense.get_temperature())
        sensors["humidity"] = str(sense.get_humidity())

        o = sense.get_orientation()
        sensors["pitch"] = str(o["pitch"])
        sensors["roll"] = str(o["roll"])
        sensors["yaw"] = str(o["yaw"])

        a = sense.get_accelerometer_raw()
        sensors["x"] = str(a["x"])
        sensors["y"] = str(a["y"])
        sensors["z"] = str(a["z"])

        t = datetime.datetime.now()
        sensors["timestamp"] = str(t.strftime('%Y%m%d %H:%M'))
        sensors["lng"] = '-118.323411'
        sensors["lat"] = '33.893916'
        sensors["device_name"] = "AstroPiQuake"
        return sensors

def reportWeather(weatherColor,A,I,Q,sense):
        humidity(A,I,Q, sense)
        time.sleep(3)
        smiley(weatherColor, sense)
        time.sleep(3)

def main():
        s = socket.socket()

        # get the URL for the multi-lingual announcer at Public Radio
        
        getURL = "http://"+args['ipaddr']+"/getIP.php"
        fp = urllib.request.urlopen(getURL)
        host = fp.read()
        host = host.decode("utf8").strip("\n")
        fp.close()

        # connect to Public Radio to send the status report
        port = 8089
        print(host, port)
        s.connect((host,port))
        print(s.recv(1025))
        sense = SenseHat()
        sense.clear()
        dictSensors = getSensorData(sense)
        payload = ",".join(("{},{}".format(*dictSensor) for dictSensor in dictSensors.items()))
        s.send((payload.encode('utf-8')))

        # set the rotation so that Smiley is not upside down
        sense.set_rotation(180)
        
        # change the color of the palm tree depending on the humidity
        if float(dictSensors["humidity"]) < 60:
                Q = [75,38,0]
                I = [35,0,0]
                A = [75,0,0]
        else:
                Q = [0,38,75]
                I = [0,0,50]
                A = [0,0,75]

        red     = (75, 0, 0)
        yellow  = (75,50,0)
        blue    = (0,50,75)
        
        # change the smiley face depending on the temperature
        if float(dictSensors["temperature"]) -5 < 10:
                reportWeather(blue,A,I,I,sense)
        elif float(dictSensors["temperature"])-5 < 35:
                reportWeather(yellow,A,I,I,sense)
        else:
                reportWeather(red,A,I,I,sense)

if __name__ == '__main__':
        main()
```

<h2>emoji.py</h2>
This script listens for messages from Public Radio and draws emojis on the LEDs

```
python3 emoji.py
```

```
#!/usr/bin/python
'''
Purpose: receive data and display emoji on the LEDs
'''
import sys
import socket
import time
import datetime
from sense_hat import SenseHat

def panel(Q, sense,msg):
        # set all the pixels to the same color
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
        ];
        sense.set_pixels(i_pixels)
        sense.show_message(msg, text_colour=[100,100,100],back_colour=Q)

def smiley(faceColor, sense):
        I = faceColor;
        Q = [0,0,0];
        i_pixels = [
                Q,Q,I,I,I,I,Q,Q,
                Q,I,I,I,I,I,I,Q,
                I,I,Q,I,I,Q,I,I,
                I,I,I,I,I,I,I,I,
                I,I,Q,I,I,Q,I,I,
                I,I,I,Q,Q,I,I,I,
                Q,I,I,I,I,I,I,Q,
                Q,Q,I,I,I,I,Q,Q,
        ];
        sense.set_pixels(i_pixels)

def fear(faceColor,W,sense):
        # animated smiley face

        I = faceColor;
        Q = [0,0,0];
        up_pixels = [
                Q,Q,I,I,I,I,Q,Q,
                Q,I,W,I,I,W,I,Q,
                I,W,Q,W,I,Q,W,I,
                I,I,W,I,I,W,I,I,
                I,I,I,I,I,I,I,I,
                I,I,I,Q,Q,I,I,I,
                Q,I,I,I,I,I,I,Q,
                Q,Q,I,I,I,I,Q,Q,
        ];
        down_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,I,I,I,I,Q,Q,
                Q,I,I,I,I,I,I,Q,
                I,I,I,I,I,I,I,I,
                I,W,W,I,I,W,W,I,
                I,I,I,I,I,I,I,I,
                Q,I,I,I,I,I,I,Q,
                Q,Q,I,I,I,I,Q,Q,
        ];
        sense.set_pixels(up_pixels)
        time.sleep(1)
        sense.set_pixels(down_pixels)
        time.sleep(1)
        sense.set_pixels(up_pixels)
        time.sleep(1)
        sense.set_pixels(down_pixels)
        time.sleep(1)
        sense.set_pixels(up_pixels)
        time.sleep(1)

def halfCharged(sense):
        # half charged battery

        B = [150,100,0];
        I = [100,100,100];
        A = [60,60,60];
        Q = [45,0,0];
        Z = [0,0,0];
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                I,I,I,I,I,I,I,Q,
                Z,Z,A,A,A,A,A,A,
                A,A,A,A,A,A,A,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q
        ];
        sense.set_pixels(i_pixels)
        time.sleep(2)
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                I,I,I,I,I,I,I,Q,
                Z,Z,A,A,A,A,A,A,
                A,A,A,A,A,A,A,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q
        ];
        sense.set_pixels(i_pixels)
        time.sleep(2)
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                I,I,I,I,I,I,I,Q,
                Z,Z,Z,Z,A,A,A,A,
                A,A,A,A,A,A,A,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q
        ];
        sense.set_pixels(i_pixels)

def charging(sense):
        # animation showing battery charging

        B = [150,100,0];
        I = [100,100,100];
        A = [60,60,60];
        Q = [45,0,0];
        Z = [0,0,0];
        i_pixels = [
                Q,Q,Q,Q,Q,Q,B,Q,
                Q,Q,Q,Q,Q,B,Q,Q,
                I,I,I,I,B,I,I,Q,
                Z,Z,Z,B,A,A,A,A,
                A,A,A,A,B,A,A,Q,
                Q,Q,Q,B,Q,Q,Q,Q,
                Q,Q,B,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q
        ];
        sense.set_pixels(i_pixels)


def charged(sense):
        I = [100,100,100];
        A = [60,60,60];
        Q = [45,0,0];
        i_pixels = [
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                I,I,I,I,I,I,I,Q,
                A,A,A,A,A,A,A,A,
                A,A,A,A,A,A,A,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q,
                Q,Q,Q,Q,Q,Q,Q,Q
        ];
        sense.set_pixels(i_pixels)

def getIP():
        # this device is self-aware.  It can get its own ip address in order to bind a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
                s.connect(('192.168.1.14', 1))
                IP = s.getsockname()[0]
        except:
                IP = '127.0.0.1'
        finally:
                s.close()
        return IP

s = socket.socket()
host = getIP()
port = 8088
print(host, port)
s.bind((host,port))
s.listen(5)

sense = SenseHat()

# set the rotation so that the emojis are not upside down
sense.set_rotation(180)

# configure the colors
red     = (75, 0, 0)
yellow  = (75,50,0)
blue    = (0,0,75)
white   = (100,100,100)
orange  = (70,25,0)
green  = (0,100,0)

# get messages 
while True:
    try:
        c, addr = s.accept()
        varAddress = repr(addr[1])
        c.send(b'server message')
        msg = c.recv(1026).decode('utf-8')

    except Exception as e:
        print("Something happened")
        sys.exit()

    except KeyboardInterrupt:
        sys.exit()

    sense.clear()

    if msg == 'charging':
        charging(sense)

    elif msg == 'charged':
        charged(sense)

    elif msg == 'drive':
        charged(sense)
        time.sleep(2)
        halfCharged(sense)

    elif msg == 'arrive':
        smiley(yellow,sense)

    elif msg == 'quake':
        fear(yellow,white,sense)
        panel(orange,sense,'Drop, Cover, Hold on')

    else:
        panel(blue,sense,'')

    time.sleep(3)
```

