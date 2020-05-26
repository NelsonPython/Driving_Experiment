<h1>MOBI Data Mart</h1>

This is a simple MOBI Data Mart.  You may replace it with any popular data marketplace that sends messages in json, txt, or csv format.

<h2>MySQL database</h2>

Create your roadtrip database with four tables:

- KellyBlueBook - contains vehicle data

- Station - contains EV charging station data

- goal - contains the vehicle, trip origin, trip destination, and the number of fuel stops

- labDevices - contains the MAC address, IP address, and device name for each device

<h4>KellyBlueBook Table</h4>
Use the load_KellyBlueBook.py script to create the KellyBlueBook table

<h4>Station Table</h4>
Use the station.csv file along with the load_Stations.py script to create the station table

<h4>Goal Table</h4>


<h4>labDevices</h4>


<h2>NGINX webserver</h2>


<h2>Security</h2>


<h2>PHP scripts</h2>
Copy the php scripts and the ai.css file into the /var/www/html folder

<h4>ai_getIP.php</h4>

<h4>ai_addGPSCoord.php</h4>

<h4>ai_getGPSCoord.php</h4>

<h4>ai_showMap</h4>
