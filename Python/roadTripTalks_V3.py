import mysql.connector
import os.path
import sys
import vlc
import json
import time
import argparse
import pandas as pd
from gtts import gTTS
from datetime import datetime
import socket
import getIP

ap = argparse.ArgumentParser()
ap.add_argument("-l","--language",required=True, help="Choose english, spanish, or chinese")
args = vars(ap.parse_args())

s = socket.socket()
host = getIP.getIP()
port = 8089
s.bind((host,port))
s.listen(5)

# SETUP DATABASE CONNECTION
db = mysql.connector.connect(
        host = "localhost",
        user = "py",
        password = "admin1234",
        database = "translations"
)
conn = db.cursor()

def formatTimeStamp(ts):
    TS = []
    mes = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','novembre','deciembre']
    yue = ['yi','er','san','si','wu','liu','qi','ba','jiu','shi','shi yi','shi er']

    # day
    d = str(int(ts.strftime("%d")))
    I = str(int(ts.strftime("%I")))
    M = str(int(ts.strftime("%M")))

    # lookup the month name translation
    monthNum = int(ts.strftime("%m"))
    m = mes[monthNum-1]
    y = yue[monthNum-1]

    # English
    TS.append(ts.strftime("%B") + " " + d + " " +  " at " + ts.strftime("%I %M %p"))

    # Spanish
    spanishTS = " el " + d + " de " + m
    if ts.strftime("%I") == 1:
        spanishTS = spanishTS + " a la " + I + " y " + M
    else:
        spanishTS = spanishTS + " a las " + I + " y " + M
    TS.append(spanishTS)

    # Chinese
    chineseTS = y + " yue " + d + " hao zai "
    chineseTS = chineseTS + I + " dian " + M + " fen"
    TS.append(chineseTS)

    return TS

# TRANSLATING
def lookupPhrase(tag):
    # translations MUST be returned in this order:  English, Spanish, Chinese
    tagList = []
    sql = "select LANGUAGE, PHRASE from lookup where tag = '"+tag
    sql = sql + "'"
    conn.execute(sql)
    res = conn.fetchall()
    for r in res:
        if r[0].upper() == "ENGLISH":
            t = (1, r[1])
            tagList.append(t)
        elif r[0].upper() == "SPANISH":
            t = (2, r[1])
            tagList.append(t)
        elif r[0].upper() == "CHINESE":
            t = (3, r[1])
            tagList.append(t)

    tagList.sort()
    return [t[1] for t in tagList]

def formatTextOnly(tag):
    ''' translate a message '''
    msgList = lookupPhrase(tag)
    return msgList

def formatText_Beg(tag,txt):
    ''' translate a message with special text at the beginning '''
    p1 = lookupPhrase(txt)
    p2 = lookupPhrase(tag)
    msgList = [p1[x] + " " + p2[x] for x in range(3)]
    return msgList

def formatText_Mid(msg1,msg2,txt):
    # version 1.0 format
    ''' translate a message with special text in the middle '''
    p1 = lookupPhrase(msg1)
    p2 = lookupPhrase(txt)
    p3 = lookupPhrase(msg2)
    msgList = [p1[x] + " " + p2[x] + " " + p3[x] for x in range(3)]
    return msgList

def formatData_End(tag,data):
    ''' translate a version 2.0 message with numeric data '''
    msgList=[]
    phrases = lookupPhrase(tag)

    for p in phrases:
        # if there is a ; in the phrase split it into two phrases
        if p.find(";") > -1:
            p = p.split(";")
            m = p[0] + " " +  str(data) + " " + p[1]
        else:
            m = p + str(data)
        msgList.append(m)
    return msgList


def formatData_With_Time(tag,duration,tripLeg,ts):
    ''' translate a message with timestamp and data and a counter'''
    msgList=[]
    phrases = lookupPhrase(tag)

    if duration == '0':
        duration = ' '

    c=0
    for p in phrases:
        # if there is a ; in the phrase split it into two phrases
        if p.find(";") > -1:
            p = p.split(";")
            m = ts[c] + " " + p[0] + " " + duration + " " + p[1]
        else:
            m = p + str(ts[c]) + " " + duration
        msgList.append(m)
        c+=1
    return msgList

def formatTemp(temp=0, humidity=0):
    '''translate temperature and humidity (optional) '''
    farenheit = int((temp*9/5)+32)
    humidity = int(humidity)
    temp = int(temp)
    p1 = lookupPhrase('tmp1')
    p2 = lookupPhrase('tmp2')

    if humidity > 0:
        p3 = lookupPhrase('hum')
    else:
        p3 = ['','','']
        humidity = ''

    # use degrees Farenheit or degrees Celsius depending on the language
    msgList=[]
    msg = p1[0] + " " + str(farenheit) + " " + p2[0] + " " + str(humidity) + " " + p3[0]
    msgList.append(msg)
    for x in range(1,3):
        m = p1[x] + " " + str(temp) + " " + p2[x] + " " + str(humidity) + " " + p3[x]
        msgList.append(m)
    return msgList


# RECORDING DATA
def print2File(deviceName, sensorData):
    ''' print sensor data to file '''

    if os.path.isfile("sensorData/"+deviceName+".csv"):
        # if the file exists, write the data
        pass
    else:
        # if the file doesn't exist, write the headers
        fo = open("sensorData/"+deviceName+".csv","w")
        d=''
        for k in sorted (sensorData.keys()):
            # create a comma separated string with the key 
            d = d + k + ","
        # remove the last comma and add the end of line character
        fo.write(d[:-1]+"\n")
        fo.close()

    fo = open("sensorData/"+deviceName+".csv","a")
    d=''
    for k  in sorted (sensorData.keys()):
        # create a comma separated string with the data
        d = d + sensorData[k] + ","
    # remove the last comma and add the end of line character
    fo.write(d[:-1]+"\n")
    fo.close()


# SAYING MESSAGES
def sayMsg(deviceName,msg,lang,duration):

    try:
        tts = gTTS(text=msg, lang=lang)
        tts.save("sensorData/msg.mp3")
    except Exception as e:
        print("Exception ", e)
        pass

    try:
        p = vlc.MediaPlayer("sensorData/msg.mp3")
        p.play()
        time.sleep(duration)
    except Exception as e:
        print("VLC Exception ", e)
        pass

def broadcast(deviceName, msgList, duration):
    if args["language"] == "english":
        print("\n",deviceName, ": ", msgList[0])
        sayMsg(deviceName,msgList[0], 'en', duration)

    if args["language"] == "spanish":
        print("\n",deviceName, ": ", msgList[1])
        sayMsg(deviceName,msgList[1], 'es-es', duration + 1)

    if args["language"] == "chinese":
        print("\n",deviceName, ": ", msgList[2])
        sayMsg(deviceName, msgList[2], 'zh-cn', duration + 2)


print(datetime.now())
print(host, port)

msgList = formatTextOnly('hello')
broadcast("Radio", msgList, 3)
msgList=[]

while True:

    try:
        c, addr = s.accept()
        varAddress = repr(addr[1])
        #print("\nconnection received from " + varAddress)
        c.send(b'server message')
        msg = c.recv(1026).decode('utf-8')
        i = iter(msg.split(","))
        data = dict(zip(i,i))
        #print("\n{}:\n{}".format(varAddress,data))

        if len(data) > 0:
            print2File(data["device_name"],data)

            if data["device_name"] == "AstroPiQuake":
                msgList = formatTemp(float(data['temperature']), float(data['humidity']))


            elif data["device_name"] == "Enviro":
                msgList = formatTemp(float(data['temperature']))


            elif data["device_name"] == "AirMacClean":
                if float(data["CO2"]) < 5000.0:
                    msgList = formatData_End('co2', data["CO2"])
                else:
                    msgList = formatTextOnly("badAir")


            elif data["device_name"] == "Yellow":

                print("\n",data["task"])

                if data["task"] == "quake":
                    msgList = formatTextOnly(data["task"])

                else:

                    msgList = formatData_With_Time(data['task'], data['duration'], data['tripLeg'],
                    formatTimeStamp(datetime.strptime(data['timestamp'], '%Y/%m/%d %H:%M:%S')))

                    if data['task'] == 'yellow_depart':
                        os.system('python3 send_2_AstroPiQuake.py -m drive')

                    #if data['task'] == 'yellow_refuel':
                    #    os.system('python3 send_2_AstroPiQuake.py -m charging')

                    if data['task'] == 'yellow_arrive':
                        os.system('python3 send_2_AstroPiQuake.py -m arrive')

                    if data['task'] == 'yellow_scheduleFuel':
                        os.system('python3 send_2_AstroPiQuake.py -m charging')

            elif data["device_name"] == "PiCamera":
                msgList = ['What radicals are in this Chinese character?',' ',data["hanzi"][:-1]]


            broadcast(data["device_name"], msgList, 5)
            msgList=[]

    except KeyboardInterrupt:
        print("I'm stopping now")
        sys.exit()
