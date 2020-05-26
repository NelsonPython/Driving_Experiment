<?php
	$servername = "localhost";
	$username = "USERNAME";
	$password = "PASSWORD";
	$dbname = "roadtrip";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 

        #Enter the MAC address of the computer running the MOBI Data Mart
        $sql = "select ipaddr from labDevices where macaddr = 'YO:UR:MA:C9:AD:DR'";
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

