<h1>Configure Enviro</h1>

If you have not built your own Enviro, follow these [instructions](https://github.com/NelsonPython/Enviro).  Then, copy sensorEsocket.py to your home folder.

```
python3 sensorEsocket -ip 192.168.1.x
```

-ip must be the ip address of the VirtualBox running Public Radio

<h2>sensorEsocket.py</h2>

```
from envirophat import light, motion, weather,leds

import time
import datetime
import argparse
import urllib.request
import socket

ap = argparse.ArgumentParser()
ap.add_argument("-ip","--ipaddr", required=True,
    help = ("Start the host, get the host IP address, then type python3 senseToSocket.py -ip 192.168.1.x"))
args = vars(ap.parse_args())

s = socket.socket()

getURL = "http://"+args['ipaddr']+"/getIP.php"
fp = urllib.request.urlopen(getURL)
host = fp.read()
host = host.decode("utf8").strip("\n")
fp.close()

port = 8089
print(host, port)
s.connect((host,port))
print(s.recv(1025))

enviro = {}
try:
        enviro["lux"] = light.light()
        leds.on()
        rgb = str(light.rgb())[1:-1].replace(' ','').split(",")
        enviro["red"] = rgb[0]
        enviro["green"] = rgb[1]
        enviro["blue"] = rgb[2]

        leds.off()

        print(enviro["lux"])
        print(enviro["red"])
        print(enviro["green"])
        print(enviro["blue"])


        acc = str(motion.accelerometer())[1:-1].replace(' ','')
        acc = acc.split(",")

        enviro["x"] = acc[0]
        enviro["y"] = acc[1]
        enviro["z"] = acc[2]

        enviro["heading"] = motion.heading()
        enviro["temperature"] = weather.temperature()
        enviro["pressure"] = weather.pressure()
        enviro["timestamp"] = datetime.datetime.now()

        enviro["lng"] = '-118.323411'
        enviro["lat"] = '33.893916'
        enviro["device_name"] = "Enviro"

        payload = ",".join(("{},{}".format(*e) for e in enviro.items()))
        print(payload)
        s.send((payload.encode('utf-8')))

except Exception as e:
        print(e)

leds.off()
```
