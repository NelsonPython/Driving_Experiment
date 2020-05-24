<?php
	$servername = "localhost";
	$username = "py";
	$password = "admin1234";
	$dbname = "roadtrip";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 
        $sql = "SELECT VEHICLE, ORIGIN_LAT, ORIGIN_LNG, ORIGIN_NAME, DEST_LAT, DEST_LNG, DEST_NAME, GOAL_ID,NUM_FUEL_STOPS from goal  order by GOAL_ID DESC LIMIT 1";
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
	    while($row = $result->fetch_assoc()) {
	        echo $row["VEHICLE"];
		echo "," .$row["ORIGIN_LAT"];
		echo "," .$row["ORIGIN_LNG"];
		echo "," .$row["ORIGIN_NAME"];
		echo "," .$row["DEST_LAT"];
		echo "," .$row["DEST_LNG"];
		echo "," .$row["DEST_NAME"];
		echo "," .$row["GOAL_ID"];
		echo "," .$row["NUM_FUEL_STOPS"];
	    }
	} else {
	    echo "None";
	}
	$conn->close();
?>

