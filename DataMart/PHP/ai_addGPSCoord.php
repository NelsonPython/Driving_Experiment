<!DOCTYPE HTML>
<html>
<head>
	<title>MOBI Data Market</title>
	<link rel="stylesheet" href="ai.css">
</head>
<?php
	$servername = "localhost";
	$username = "USERNAME";
	$password = "PASSWORD";
	$dbname = "roadtrip";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 
?>

<div class="w3-row">
<div class="w3-half w3-container">

	<a  href="http://localhost/index.php">Home</a>

	<h3>Road Trip</h3>
	<p><span class="error">* Required</span></p>

	<form method="post" action="ai_showMap.php"">

                        <br>Vehicle <select name="vehicle">
                                <option value="vehicle" selected></option>
                                <option value="economy">EV economy car</option>
                                <option value="sports">EV sports sedan</option>
                                <option value="semi">EV semi-truck</option>
                                </select>

                        <br><br>Starting location <select name="origin">
                                <option value="0,0,origin" selected></option>
                                <option value="48.9962,-122.7309,Blaine">Blaine</option>
                                <option value="34.0524,-118.2618,Los Angeles">Los Angeles</option>
                                <option value="38.5781,-121.4834,Sacramento">Sacramento</option>
                                <option value="32.5461,-117.0307,San Diego">San Diego</option>
                                </select>

                        <br><br>Destination <select name="dest">
                                <option value="0,0,dest" selected></option>
                                <option value="48.9962,-122.7309,Blaine">Blaine</option>
                                <option value="34.0524,-118.2618,Los Angeles">Los Angeles</option>
                                <option value="38.5781,-121.4834,Sacramento">Sacramento</option>
                                <option value="32.5461,-117.0307,San Diego">San Diego</option>
                                </select>

		  <br><br>
		  <input type="submit" name="submit" value="Go">
	</form>
	</table>
</div>
</div>
</body>
</html>

