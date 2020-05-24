#TODO: match up dates of temperature readings

import pandas as pd
import matplotlib.pyplot as plt

aq = pd.read_csv("sensorData/AirMacClean.csv")

plt.figure()
plt.title("Carbon Dioxide Levels < 5000 are within OSHA safety limits")
plt.xlabel("Minutes running")
plt.ylim(0,5000)
plt.ylabel("PPM")
plt.plot(aq["CO2"])
plt.show()

plt.figure()
plt.title("TVOC")
plt.xlabel("Minutes running")
plt.ylabel("PPB")
plt.plot(aq["TVOC"])
plt.show()

