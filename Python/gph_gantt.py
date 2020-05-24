'''
Purpose:  publish a Gantt chart showing when devices report data

TODO:  revise code to handle devices running for more than one day
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)

qk = pd.read_csv('sensorData/AstroPiQuake.csv')
ev = pd.read_csv('sensorData/Enviro.csv')
co = pd.read_csv('sensorData/AirMacClean.csv')

def datetimeDelta(duration):
    ''' 1 days 02:36:00  TODO:  add code for 10 days or more  '''
    # day
    d = int(duration[:1]) * 1440 

    # h:m:s
    duration = duration[7:]
    duration = duration.split(":")
    h = int(duration[0]) * 60
    m = int(duration[1])
    s = int(duration[2][:2]) // 60
    return d + h + m + s

def prepareData(df):
    # convert timestamp to datetime format
    # using timestamp as the index, resample the data at every 10 minutes, 10T
    # fill missing data with zeros
    # make a new column with the index

    nulltest = [1.0] *  df.shape[0]
    df["NULLTEST"] = nulltest

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    q10 = df.resample("10T", on='timestamp').mean()
    q10 = q10.fillna(0)
    q10["RPT"] = q10.index
    return q10

def findMissingReports(q10):
    # find the date time ranges where there is missing data 
    return q10[["RPT"]].loc[q10["NULLTEST"] == 0].values

def calcReportingChunks(beg, end, missing):
    # find the chunks of time when the device was not reporting
    # assuming the device operates less than a day TODO:  add code for longer operation
    chunks = [beg]
    t = missing[0][0]
    chunks.append(t)

    for m in missing:
        m = pd.to_datetime(m)
        delta = m[0] - t
        minutes = delta.seconds % 3600 // 60
        if minutes > 10:
             chunks.append(t)
             chunks.append(m[0])
        t = m[0]

    chunks.append(missing[-1][0])
    chunks.append(end)
    return chunks

def calcSpan(chunks, beg):
    # compute the duration
    begPoints = []
    span = []
    for k in range(0, len(chunks), 2):
        begPoints.append(datetimeDelta(str(chunks[k] - beg)))
        span.append(datetimeDelta(str(chunks[k+1] - chunks[k])))
    return list(zip(begPoints, span))

# PREPARE PLOT DATA
qk_10 = prepareData(qk)
ev_10 = prepareData(ev)
co_10 = prepareData(co)

qkMissing = findMissingReports(qk_10)
evMissing = findMissingReports(ev_10)
coMissing = findMissingReports(co_10)

# get the beginning and ending dates and times
qk_beg = pd.to_datetime(qk["timestamp"][0])
ev_beg = pd.to_datetime(ev["timestamp"][0])
co_beg = pd.to_datetime(co["timestamp"][0])
qk_end = pd.to_datetime(qk["timestamp"][len(qk)-1])
ev_end = pd.to_datetime(ev["timestamp"][len(ev)-1])
co_end = pd.to_datetime(co["timestamp"][len(co)-1])

# COMPUTE ACTUALS
if len(qkMissing) > 0:
	qk_chunks = calcReportingChunks(qk_beg, qk_end, qkMissing)
	qk_plotPoints = calcSpan(qk_chunks, qk_beg)
else:
	qk_plotPoints = [(qk_beg, datetimeDelta(qk_end-qk_beg))]

if len(evMissing) > 0:
	ev_chunks = calcReportingChunks(ev_beg, ev_end, evMissing)
	ev_plotPoints = calcSpan(ev_chunks, ev_beg)
else:
	ev_plotPoints = [(ev_beg, datetimeDelta(ev_end-ev_beg))]

if len(coMissing) > 0:
	co_chunks = calcReportingChunks(co_beg, co_end, coMissing)
	co_plotPoints = calcSpan(co_chunks, co_beg)
else:
	co_plotPoints = [(co_beg, datetimeDelta(co_end-co_beg))]

#print(qk_plotPoints)
#print(ev_plotPoints)
#print(co_plotPoints)

# COMPUTE SCHEDULED
qk_expected = [(qk_plotPoints[0][0], qk_plotPoints[-1][0] + qk_plotPoints[-1][1])]
ev_expected = [(ev_plotPoints[0][0], ev_plotPoints[-1][0] + ev_plotPoints[-1][1])]
co_expected = [(co_plotPoints[0][0], co_plotPoints[-1][0] + co_plotPoints[-1][1])]

# PLOT
fig, gnt = plt.subplots()
gnt.set_title('PROJECT PLAN:  Schedule vs Actual')
gnt.set_ylim(0,30)
xLabel = "Minutes running from " + qk_beg.strftime("%m/%d/%Y") + " to " + qk_end.strftime("%m/%d/%Y")
gnt.set_xlabel(xLabel)
gnt.set_yticklabels([' ','AstroPiQuake',' ','Enviro', ' ', 'Air MacClean'])
gnt.grid(True)

gnt.broken_barh(qk_expected, (0,4), facecolors=('tab:blue'))
gnt.broken_barh(qk_plotPoints, (5,4))

gnt.broken_barh(qk_expected, (10,4), facecolors=('tab:cyan'))
gnt.broken_barh(ev_plotPoints, (15,4), facecolors=('tab:cyan'))

gnt.broken_barh(qk_expected, (20,4), facecolors=('tab:orange'))
gnt.broken_barh(co_plotPoints, (25,4), facecolors=('tab:orange'))
plt.show()
