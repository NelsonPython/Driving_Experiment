<h1>Creating a simple MOBI Data Mart web app</h1>

<img src="images/MobiDataMart_v2.png">

Copy ai.css, ai_addGPSCoord.php, ai_getGPSCoord.php, ai_getIP.php, ai_showMap into your /var/www/html folder



<h3>ai_addGPSCoord.php</h3>
When you choose a route, ai_addGPSCoord.php saves the GPS coordinates in the goal table

<img src="images/An-4.png">



<h3>ai_getGPSCoord.php</h3>
When ai_showMap.php plans the route, it uses ai_getGPSCoord.php to get the GPS coordinates for the current trip


<h3>ai_getIP.php</h3>
Each device gets the IP address


<h3>ai_showMap</h3>
This script plans the route and shows the scheduled charging stops

<img src="images/Sac-SanDiego-itinerary.png">


