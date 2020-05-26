<h1>Public Radio</h1>

Public Radio broadcasts messages in three languages:  English, Spanish, and Chinese.  During a demo, this allows humans to understand conversations between devices.  In the real world, autonomous vehicles may not speak aloud when communicating with each other because sending and receiving messages is faster and more accurate.  Public Radio uses the translations database.  Open MySQL and create the translations database

```
CREATE DATABASE translations;
```

Create the lookup table

```
CREATE TABLE lookup (
lookup_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
tag varchar(20),
language varchar(20),
phrase varchar(100));
```

<h3>Running Public Radio</h3>
Go to your home directory and make a folder called /PublicRadio.  Copy roadTripTalks.py, send_2_yellow_wheels.py, send_2_AstroPiQuake.py, and quake.sh


<h3>Creating charts and graphs</h3>
Go to your /PublicRadio folder and copy ??? graphs
