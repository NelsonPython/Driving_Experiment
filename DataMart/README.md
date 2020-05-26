<h1>MOBI Data Mart</h1>

This is a simple MOBI Data Mart.  You may replace it with any popular data marketplace that sends messages in json, txt, or csv format.  Follow this <a href="https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-ubuntu-18-04">tutorial</a> to install Nginx, MySQL, and PHP on Ubuntu 18.04

<h2>Creating the Roadtrip database</h2>

Create your roadtrip database with four tables:

- KellyBlueBook - contains vehicle data

- Station - contains EV charging station data

- goal - contains the vehicle, trip origin, trip destination, and the number of fuel stops

- labDevices - contains the MAC address, IP address, and device name for each device

Open MySQL and create the roadtrip database

```
CREATE DATABASE roadtrip;
```

Create the KellyBlueBook table

```
CREATE TABLE KellyBlueBook (
v_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
vehicle varchar(40),
vehicle_range in(11),
charge_time_240v float(3,1),
adapter varchar(30),
network_name varchar(40),
charge_type varchar(10),
vehicle_website varchar(200));
```

Use the [load_KellyBlueBook.py](DB/load_KellyBlueBook.py) script to insert data

Create the Station table

```
CREATE TABLE Station (
s_ID                int(11)  NOT NULL PRIMARY KEY AUTO_INCREMENT,
station_name        varchar(80),
station_address     varchar(60),
station_city        varchar(30),
station_state       varchar(2),
zip                 varchar(5),
zip_plus4           varchar(4),
lat                 varchar(20),
lng                 varchar(20),
date_last_confirmed date,
access_groups       varchar(35),
access_days         varchar(250),
cards_accepted      varchar(30),
access_code         varchar(10),
access_detail_code  varchar(20),
ev_level_1_evse_num varchar(10),
ev_level_2_evse_num varchar(10),
ev_dc_fast_count    int(11),
ev_network          varchar(20),
ev_pricing          varchar(200),
ev_connector_types  varchar(30)); 
```
You can use the <a href="https://www.kaggle.com/nelsondata/map-ev-charging-stations-on-highway-i-5">Kaggle notebook</a> to create your own station.csv file or copy the station.csv file from the DB folder and run the [load_Stations.py](DB/load_Stations.py) script to insert data


Create the goal table
```
CREATE TABLE goal (
GOAL_ID  int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
VEHICLE	       varchar(20),
ORIGIN_LAT     varchar(10),
ORIGIN_LNG     varchar(10),
ORIGIN_NAME    varchar(40),
DEST_LAT       varchar(10),
DEST_LNG       varchar(10),
DEST_NAME      varchar(40),
NUM_FUEL_STOPS int(11));
```

Get the MAC address of each of your devices then create the labDevices table

```
CREATE TABLE labDevices (
lab_id  int(11)  NOT NULL PRIMARY KEY AUTO_INCREMENT,
ipaddr  varchar(15),
macaddr varchar(17),
device  varchar(30));
```

<h2>PHP scripts</h2>
Copy the php scripts and the ai.css file into the /var/www/html folder

<h4>ai_getIP.php</h4>

<h4>ai_addGPSCoord.php</h4>

<h4>ai_getGPSCoord.php</h4>

<h4>ai_showMap</h4>
