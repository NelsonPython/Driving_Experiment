#TODO: match up dates of temperature readings

import pandas as pd
import matplotlib.pyplot as plt

ev = pd.read_csv("sensorData/Enviro.csv")

plt.figure()
plt.title("Sky Color")
plt.xlabel("Minutes")
plt.ylabel("RGB")
plt.plot(ev["red"], "r", label= "red")
plt.plot(ev["green"], "g", label= "green")
plt.plot(ev["blue"], "b", label= "blue")
plt.legend()
plt.show()


plt.figure()
plt.title("Light")
plt.xlabel("Minutes")
plt.ylabel("Amount of light")
plt.plot(ev["lux"])
plt.legend()
plt.show()

