<h1>MOBI Data Mart</h1>

This is a simple MOBI Data Mart.  You may replace it with any popular data marketplace that sends messages in json, txt, or csv format.

<h2>MySQL database</h2>

Create your roadtrip database with four tables:

- KellyBlueBook - contains vehicle data

- Station - contains EV charging station data

- goal - contains the vehicle, trip origin, trip destination, and the number of fuel stops

- labDevices - contains the MAC address, IP address, and device name for each device

Open MySQL and create the roadtrip database

```
CREATE DATABASE
```

Create the KellyBlueBook table
```
CREATE TABLE KellyBlueBook >>>
```

Use the [load_KellyBlueBook.py](DB/load_KellyBlueBook.py) script to insert data

<h4>Station Table</h4>

Create the Station table

```
CREATE TABLE >>>
```
Copy the station.csv file and run the [load_Stations.py](DB/load_Stations.py) script to insert data


<h4>Goal Table</h4>

Create the goal table
```
CREATE TABLE
```

<h4>labDevices</h4>
Get the MAC address of each of your devices then create the labDevices table
```
CREATE TABLE
```

<h2>NGINX webserver</h2>

Follow this <a href="https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04">tutorial</a> to install and configure your NGINX webserver

<h2>Security</h2>


<h2>PHP scripts</h2>
Copy the php scripts and the ai.css file into the /var/www/html folder

<h4>ai_getIP.php</h4>

<h4>ai_addGPSCoord.php</h4>

<h4>ai_getGPSCoord.php</h4>

<h4>ai_showMap</h4>
