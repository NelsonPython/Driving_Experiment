<?php
	$servername = "localhost";
	$username = "py";
	$password = "admin1234";
	$dbname = "roadtrip";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 

        $sql = "select ipaddr from labDevices where macaddr = '08:00:27:86:dd:45'";
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
	    while($row = $result->fetch_assoc()) {
	        echo $row["ipaddr"];
	    }
	} else {
	    echo "None";
	}
	$conn->close();
?>

