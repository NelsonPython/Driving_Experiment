<!DOCTYPE HTML>
<html>
<head>
	<title>MOBI Data Mart</title>
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

	<a  href="http://localhost/index.php">Home</a>

	<h3>Route</h3>
	<?php
                //echo $_POST["vehicle"];
                //echo $_POST["origin"];
                //echo $_POST["dest"];

		$getVehicle = "";
		$getOrigin = "";
		$getDest = "";
		$getVehicleErr = "";
		$getOriginErr = "";
		$getDestErr = "";

		if ($_SERVER["REQUEST_METHOD"] == "POST") {
		  if (empty($_POST["vehicle"])) {
		    $getVehicleErr = "Vehicle required";
		  } else {
		    $getVehicle = validate_input($_POST["vehicle"]);
		    if (!preg_match("/^[a-zA-Z ]*$/",$getVehicle)) {
		      $getVehicleErr = "Only letters and white space allowed"; 
		    }
		  }

		  if (empty($_POST["origin"])) {
		    $getOriginErr = "Starting location required";
		  } else {
		    $getOrigin = validate_input($_POST["origin"]);
		    if (!preg_match("/^[a-zA-Z0-9-. ]*$/",$getOrigin)) {
		      $getOriginErr = "Valid GPS coordinate"; 
		    $getOrigin = explode (",", $getOrigin);

		    }
		  }

		  if (empty($_POST["dest"])) {
		    $getDestErr = "Destination required";
		  } else {
		    $getDest = validate_input($_POST["dest"]);
		    if (!preg_match("/^[a-zA-Z0-9-. ]*$/",$getDest)) {
		      $getDestErr = "Valid GPS coordinate"; 
		    $getDest = explode (",", $getDest);

		    }
		  }
		}

		function validate_input($data) {
		  $data = trim($data);
		  $data = stripslashes($data);
		  $data = htmlspecialchars($data);
		  return $data;
		}

		if (isset($getVehicle) && $getVehicle !== '') {

			echo "Vehicle: ".$getVehicle;
			echo "<br>Starting location: ".$getOrigin[2];
			echo "<br>Destination: ".$getDest[2];
			echo "<br><br>";
			echo '<table class="w3-table">';
                        //echo '<a  href=http://localhost/maps/'.$getVehicle.'Map.html>Route map and charging schedule</a>';

			$sql = "INSERT INTO goal (VEHICLE, ORIGIN_LAT, ORIGIN_LNG, ORIGIN_NAME, DEST_LAT, DEST_LNG, DEST_NAME) 
				VALUES ('" .$getVehicle. "','" .$getOrigin[0]. "','" .$getOrigin[1]. "','" .$getOrigin[2]. "','".$getDest[0]. "','" .$getDest[1]. "','" .$getDest[2]. "')";
	                //echo $sql. "<br>";
			if ($conn->query($sql) == TRUE) {
				$last_ID = $conn->insert_id;
			} else {
				echo "I did not understand the goal".$sql."<br>".$conn->error;
			};


                $minLat = 32.665584;
                $maxLat = 48.791487;

                $cmd = '/usr/bin/python3.6 ai_haversine.py -ot '.$getOrigin[0].' -ol '.$getOrigin[1].' -dt '.$getDest[0].' -dl '.$getDest[1].'  2>&1';
                $output = exec($cmd, $out, $status);
                //echo "<br>".$cmd;
                //echo "<br>".$status;
                //echo "<br>".$out[0];
                //echo "<br>".$out[1];
                $tripDistance = intval($out[0]);
                $bearing = intval($out[1]);

                $sql = "select vehicle, vehicle_range, charge_time_240v, adapter,
                        network_name, charge_type from KellyBlueBook where vehicle = '$getVehicle'";
                $res = $conn->query($sql);

                if ($res->num_rows > 0) {
                    while($r = $res->fetch_assoc()) {
                        $vehicleRange = $r["vehicle_range"];
                        $EV_adapter = $r["adapter"];
                        $EV_charger = $r["charge_type"];
                        $EV_network = $r["network_name"];
                    }
                } else {
                    echo "None";
                }
                $vehicleRange80 = floatval($vehicleRange) * 0.80;
                echo "Assumptions:  use 80% of a vehicle's range because many battery chargers report charging to 80% of capacity<br><br>";
                echo $getVehicle." has a driving range of : ".$vehicleRange." miles.  The range used for route planning is 80% or ".$vehicleRange80." miles<br>";

                if (strpos("J1772", $EV_adapter) !== false) {
                        $EV_adapter = 'J1772';
                }

                echo "<br>Vehicle adapter: ".$EV_adapter;
                echo "<br>Vehicle network: ".$EV_network;
                echo "<br>Vehicle charger: ".$EV_charger;

                echo "<br><br>Trip Distance ".$tripDistance." miles";

                $numStops = round($tripDistance / $vehicleRange80);
		if ($numStops == 0) {
	                $numStops = 1;
		}

                echo "<br>Number of refueling stops between ".$getOrigin[2]." and ".$getDest[2].": ".$numStops;

                $sql = "UPDATE goal SET NUM_FUEL_STOPS = ".$numStops." where GOAL_ID = ".intval($last_ID);
                $conn->query($sql);

		$lat = $getOrigin[0];
		$lng = $getOrigin[1];
                echo "<br><br>Depart: ".$getOrigin[2];
                for ($x = 1; $x <= $numStops; $x++) {

                        echo "<br><br>GPS COORDINATES: ".$lat." ".$lng;
                        $cmd2 = "/usr/bin/python3.6 ai_greatCircle.py -t ".floatval($lat)." -l ".floatval($lng)." -v ".intval($vehicleRange80)." -b ".intval($bearing)." 2>&1";
                        $output2 = exec($cmd2, $out2, $status2);
                        $lat2 = $out2[0];
                        $lng2 = $out2[1];
                        $out2 = [];

                        $lowLat = floatval($lat2) - 1;
                        $highLat = floatval($lat2) + 1;

                        $sql = "SELECT lat, lng, station_name, station_address, station_city, station_state, zip,
                                access_code, access_days, cards_accepted, ev_network, ev_pricing,
                                ev_connector_types, ev_dc_fast_count
                                from Station where lat > $lowLat and lat < $highLat and
                                ev_connector_types like '%$EV_adapter%'
                                and access_code like '%public%' and access_days like '%24%'
				order by ev_dc_fast_count DESC LIMIT 1";
                        //echo "<br>".$sql;
                        $res2 = $conn->query($sql);
                        if ($res2->num_rows > 0) {
                            while($e = $res2->fetch_assoc()) {
                                    $chargeLat = $e["lat"];
                                    $chargeLng = $e["lng"];
                                    $stationLocation = $e["station_name"]." ".$e["station_address"]." ".$e["station_city"].", ".$e["station_state"]." ".$e["zip"];
                                    $accessCode = $e["access_code"];
                                    $accessDays = $e["access_days"];
                                    $cardsAccepted = $e["cards_accepted"];
                                    $ev_network = $e["ev_network"];
                                    $ev_pricing = $e["ev_pricing"];
                                    $ev_connector_types = $e["ev_connector_types"];
                                    $ev_dc_fast_count = $e["ev_dc_fast_count"];
                                }
                        } else {
                                if ($lat2 > $maxLat || $lat2 < $minLat) {
                                        break;
                                } else {
                                        echo "<br>There are no stations at the next GPS coordinates: ".$lat2." ".$lng2;
                                        break;
                                }

                        }
                        echo "<br>DRIVE TO: ".$chargeLat. " ".$chargeLng;
                        echo "<br>".$numStop." CHARGE BATTERY AT:";
                        echo "<br>".$stationLocation;
                        echo "<br>Access code: ".$accessCode;
                        echo "<br>Access days: ".$accessDays;
                        echo "<br>Cards accepted: ".$cards_accepted;
                        echo "<br>Network: ".$ev_network;
                        echo "<br>Connector types: ".$ev_connector_types;
                        echo "<br>Number of high-speed chargers: ".$ev_dc_fast_count;
                        echo "<br>Price: ".$ev_pricing;

                $lat = $chargeLat;
                $lng = $chargeLng;

                };
                echo "<br><br>ARRIVE: ".$getDest[2];
                $conn->close();
                }
	?>
	</table>
</body>
</html>

