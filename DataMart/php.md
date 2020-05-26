<h1>Creating a simple MOBI Data Mart web app</h1>

Copy these php scripts and the ai.css file into your /var/www/html folder:

ai_addGPSCoord.php

ai_getGPSCoord.php

ai_getIP.php

ai_showMap

<img src="images/MobiDataMart_v2.png">


<h4>ai_addGPSCoord.php</h4>

<img src="images/An-4.png">

When you choose a route, ai_addGPSCoord.php saves the GPS coordinates in the goal table

<h4>ai_getGPSCoord.php</h4>

When ai_showMap.php plans the route, it uses ai_getGPSCoord.php to get the GPS coordinates for the current trip

<h4>ai_getIP.php</h4>

Each device gets the IP address

<h4>ai_showMap</h4>

This script plans the route and shows the scheduled charging stops

<img src="images/Sac-SanDiego-itinerary.png">


