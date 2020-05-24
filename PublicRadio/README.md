<h1>Public Radio</h1>

Public Radio reports messages from AI Lab devices in three languages:  English, Spanish, and Chinese.  It has a limited vocabulary with messages stored in the Translations table of the roadtrip database.

Create two MySQL databases:

- Roadtrip

- Translations

<h4>Configure roadtrip</h4>

Create four tables:

- KellyBlueBook - contains vehicle data

- Station - contains EV charging station data

- goal - contains the vehicle, trip origin, trip destination, and the number of fuel stops

- labDevices - contains the MAC address, IP address, and device name for each device

<h4>Configure Translations</h4>

Create the lookup table that uses a tag to find the proper phrase for each language

<h2>Configure the scripts</h2>
Go to your home directory and make a folder called /PublicRadio.  Copy roadTripTalks.py, send_2_yellow_wheels.py, send_2_AstroPiQuake.py, and quake.sh

<h2>Configure graphs</h2>
Go to your /PublicRadio folder and copy ??? graphs
