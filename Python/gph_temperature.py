#TODO: match up dates of temperature readings

import pandas as pd
import matplotlib.pyplot as plt

sp = pd.read_csv("sensorData/AstroPiQuake.csv")
ev = pd.read_csv("sensorData/Enviro.csv")

plt.figure()
plt.title("Temperature")
plt.xlabel("Minutes running")
plt.ylabel("Degrees Celsius")
plt.plot(sp["temperature"], label="AstroPiQuake")
plt.plot(ev["temperature"], label="Enviro")
plt.legend()
plt.show()

