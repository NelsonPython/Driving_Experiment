<h1>Data Mart</h1>

<b>The data mart is a simple web app the shows data from the driving experiment.</b>  You may replace it with any popular data marketplace that sends messages in json, txt, or csv format.  Follow this <a href="https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-ubuntu-18-04">tutorial</a> to install Nginx, MySQL, and PHP on Ubuntu 18.04.

<h2>Creating the Roadtrip database</h2>

Create your roadtrip database with four tables:

- BlueBook - contains vehicle data

- Station - contains EV charging station data

- goal - contains the vehicle, trip origin, trip destination, and the number of fuel stops

- labDevices - contains the MAC address, IP address, and device name for each device

Open MySQL and create the roadtrip database

```
CREATE DATABASE roadtrip;
```

Create the BlueBook table

```
CREATE TABLE BlueBook (
v_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
vehicle varchar(40),
vehicle_range in(11),
charge_time_240v float(3,1),
adapter varchar(30),
network_name varchar(40),
charge_type varchar(10),
vehicle_website varchar(200));
```

Use the [load_BlueBook.py](DB/load_BlueBook.py) script to insert data

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

Create the labDevices table

```
CREATE TABLE labDevices (
lab_id  int(11)  NOT NULL PRIMARY KEY AUTO_INCREMENT,
ipaddr  varchar(15),
macaddr varchar(17),
device  varchar(30));
```

Use the ip addr command to get the IP address and MAC address of your Public Radio, AstroPiQuake, and Bumblebee AV

```
ip addr
```
In this example, the ip address is 192.168.1.8 and the mac address is YO:UR:MA:C9:AD:DR

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether YO:UR:MA:C9:AD:DR brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 601665sec preferred_lft 601665sec
    inet6 fe80::ae56:b667:f535:22cd/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```


Insert your data into the labDevices table.  Do not change the device tags.  They are used by other programs.

```
insert into labDevices (ipaddr,macaddr,device) values ('192.168.1.x','YO:UR:MA:C9:AD:DR','radio')
insert into labDevices (ipaddr,macaddr,device) values ('192.168.1.x','YO:UR:MA:C9:AD:DR','AstroPiQuake')
insert into labDevices (ipaddr,macaddr,device) values ('192.168.1.x','YO:UR:MA:C9:AD:DR','bumblebeeav')
```

<h2>Creating a simple web app</h2>

[Programming PHP scripts ](php.md)

