<h1>Bumblebee AV</h1>
Go to your home directory and make a folder called /bumblebeeav.  Copy socketSports.py, motors.py, and listener.py.  Run socketSports.py and listener.py in different PuTTY sessions.

```
python3 socketSports.py -i 192.168.1.x
```

-ip must be the ip address of Public Radio


<h2>socketSports</h2>

'''
Purpose:  drive the demo

Inputs:
- modules to drive robot:  motors.py

Outputs:
- vehicle driving from one refueling stop to the next
- messages sent to host

'''
import sys
import RPi.GPIO as GPIO
import time
import datetime
import socket
import argparse
import urllib.request
from time import sleep
import motors

ap = argparse.ArgumentParser()
ap.add_argument("-ip","--ipaddr", required=True,
    help = ("Start webserver virtualBox, get webserver IP address, python3 socketSports.py -ip 192.168.1.x "))
args = vars(ap.parse_args())

#get the URL for Public Radio
getURL = "http://"+args['ipaddr']+"/ai_getIP.php"
fp = urllib.request.urlopen(getURL)
host = fp.read()
host = host.decode("utf8").strip("\n")
fp.close()
port = 8089
print("host: ", host,":",port)

#for this beginner tutorial, the listener and socketSports are not multi-threaded
#messages from the listener are stored in a text file called quake.txt
with open("quake.txt","w") as fo:
    fo.write("")

#calibrate motors and driving time
stopMtrTime = 0.1
forwardTime = 0.05
totDriveTime = 90

#set mode and turn off warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setup line followers
driverLine = 21
passengerLine = 26
GPIO.setup(driverLine,GPIO.IN)
GPIO.setup(passengerLine,GPIO.IN)

#setup motors
motors.setupGPIO(27,24,5)
motors.setupGPIO(22,6,17)
motors.setupGPIO(16,23,12)
motors.setupGPIO(18,13,25)

def reportStatus(host,port,task,timestamp,duration,tripLeg):
    msg = "device_name,Yellow,task,"+task+",timestamp,"+timestamp+",duration,"+str(duration)+",tripLeg,"+str(tripLeg)
    print("\n", task, " ", timestamp, " duration: ", duration, " trip leg: ",  tripLeg)

    s = socket.socket()
    try:
        s.connect((host,port))
        print(s.recv(1025))
        s.send((msg.encode('utf-8')))
        s.close()
    except Exception as e:
        print("I lost my connection to", host)
        pass

#get the number of fuel stops from the MOBI data mart
getFuelStops = "http://"+args['ipaddr']+"/ai_getGPSCoord.php"
fp = urllib.request.urlopen(getFuelStops)
gpsBytes = fp.read()
goal = gpsBytes.decode("utf8").strip("\n")
fp.close()
goal = goal.split(",")

#compute number of planned fuel stops
numFuelStops = int(goal[8])
i = round(totDriveTime/numFuelStops)
fuelTimes = [i + (x*i) for x in range(numFuelStops)]

#BEGIN TRIP
departTime = time.time()
statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
reportStatus(host,port,"yellow_depart", statusTime,'0',0)
print("Started driving at %s and will drive for %d" % (statusTime,totDriveTime))
motors.stop(5,17,12,25)
time.sleep(2)

tripLeg=1
quitFlag=False
try:
    while True:
      if quitFlag is True:
          break

      for t in range(totDriveTime):

            # drive and try not to get lost
            if motors.IsFollowingLine(driverLine, passengerLine):
                motors.goForward(0.05)
                motors.stop(5,17,12,25)
            else:
                if motors.SeekLine(driverLine, passengerLine)==False:
                    motors.stop(5,17,12,25)
                    statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                    reportStatus(host,port,'yellow_lost',statusTime,'0',tripLeg)
                    quitFlag=True
                    break

            # refuel
            if t in fuelTimes:

                # is there an earthquake?
                with open("quake.txt") as f:
                    line = f.read().strip("\n")
                if line == 'stop':
                    print("EARTHQUAKE ALERT - DROP, COVER, HOLD ON")
                    statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                    reportStatus(host,port,'quake',statusTime,"EARTHQUAKE. DROP, COVER, HOLD ON",tripLeg)
                    quitFlag=True
                    break

                # compute the driving time from departure to the first fuel stop
                stopTime = time.time()
                delta1 = stopTime - departTime

                motors.stop(5,17,12,25)

                afterPayTime = time.time()
                delta2 = afterPayTime - stopTime
                #statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                #reportStatus(host,port,'yellow_refuel', statusTime, str(round(delta2,2)),tripLeg)

                sched = round(delta1+delta2+delta2,0)
                if sched < 1: sched = 1
                statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                reportStatus(host,port,'yellow_scheduleFuel',statusTime, str(int(sched)),tripLeg)
                departTime = time.time()

                # simulate refueling and wait for radio host
                time.sleep(4)
                statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                reportStatus(host,port,"yellow_depart", statusTime,'0',0)

                tripLeg+=1

      if quitFlag is True:
          pass
      else:
          statusTime = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
          reportStatus(host,port,'yellow_arrive', statusTime,'0',tripLeg)
          quitFlag=True

except KeyboardInterrupt:
        GPIO.cleanup()

GPIO.cleanup()

```

<h2>motors.py</h2>

```
It is easier to troubleshoot the motors if you color code the wires that connect them to the motor controller 
Describing your configuration inside the script doesn't affect driving performance and it is convenient

Motor 1:  yellow ground wire front driverside
Enable = 5
Postive = 24
Negative = 27

Motor 2: green ground wire rear driverside
Enable = 17
Postive = 6
Negative = 22

Motor 3: orange ground wire front passenger
Enable = 12
Positive = 23
Negative = 16

Motor 4: blue ground wire rear passenger
Enable = 25
Positive = 13
Negative = 18
'''

import RPi.GPIO as GPIO
import time
from time import sleep

def setupGPIO(gnd,vcc,enable):
        GPIO.setup(gnd,GPIO.OUT)
        GPIO.setup(vcc,GPIO.OUT)
        GPIO.setup(enable,GPIO.OUT)

def forward(gnd,vcc,enable):
        GPIO.output(gnd,GPIO.HIGH)
        GPIO.output(vcc,GPIO.LOW)
        GPIO.output(enable,GPIO.HIGH)

def backward(gnd,vcc,enable):
        GPIO.output(gnd,GPIO.LOW)
        GPIO.output(vcc,GPIO.HIGH)
        GPIO.output(enable,GPIO.HIGH)

def stop(e1, e2, e3, e4):
        ''' set enable to low to stop '''
        GPIO.output(e1,GPIO.LOW)
        GPIO.output(e2,GPIO.LOW)
        GPIO.output(e3,GPIO.LOW)
        GPIO.output(e4,GPIO.LOW)
        sleep(0.05)

def goForward(forwardTime):
        forward(27,24,5)        # motor 1
        forward(22,6,17)        # motor 2
        forward(23,16,12)       # motor 3
        forward(18,13,25)       # motor 4
        sleep(forwardTime)

def IsFollowingLine(driverLine,passengerLine):
        ''' check the color reported by the black (0) and white (1) sensor
        '''
        # if both line followers are seeing white
        if GPIO.input(driverLine) == 1 and GPIO.input(passengerLine) == 1:
                return True
        else:
                return False

def SeekLine(driverLine,passengerLine):
    turnTime = 0.005
    numTries = 1
    maxTries = 200

    startTime = time.time()
    while numTries <= maxTries:
        # if driver is seeing black and passenger is seeing white, turn left
        if (GPIO.input(driverLine) == 1) and (GPIO.input(passengerLine) == 0):
            #print("seeking left", numTries)
            forward(27,24,5)         # motor 1
            forward(22,6,17)         # motor 2
            backward(23,16,12)       # motor 3
            backward(18,13,25)       # motor 4

        elif (GPIO.input(driverLine) == 0) and (GPIO.input(passengerLine) == 1):
            #print("seeking right ", numTries)
            backward(27,24,5)       # motor 1
            backward(22,6,17)       # motor 2
            forward(23,16,12)       # motor 3
            forward(18,13,25)       # motor 4
        sleep(turnTime)

        goForward(0.0005)

        if IsFollowingLine(driverLine,passengerLine):
                return True

        stopTime = time.time()
        numTries+=1
        if numTries > maxTries:
                print("I started seeking at: ", startTime, " and stopped at: ", stopTime)
                print("I looked for: ", stopTime-startTime, " seconds")
                return False

if __name__ == '__main__':
        print("motors.py")
```
<h2>listener.py</h2>
This script listens for messages from Public Radio and writes the message to a text file.

```
#!/usr/bin/python
'''
Purpose: receive messages
'''
import sys
import socket
import time
import datetime

def getIP():
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
port = 8087
print(host, port)
s.bind((host,port))
s.listen(5)

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

    if msg == 'quake':
        t = datetime.datetime.now()
        print("Earthquake alert received at: ", t.strftime('%Y%m%d %H:%M'))
        with open("quake.txt","w") as fo:
            fo.write("stop")
```
