<?php
include 'moqpconfig.php';
include 'moqpheader.php';
include '../../countyform/routeutils.php';
// The value of the variable name is found
$wpcall= $_GET['call'];

//connection to the database
#$dbhandle = mysql_connect($hostname, $username, $password)
#  or die("Unable to connect to MySQL");
#echo "Connected to $hostname...<br>";
$pdo = opendb('moqpconfig.php');

//select a database to work with
#$selected = mysql_select_db($dbname, $dbhandle)
#  or die("Could not select $dbname");
#echo "Connected to $dbname...<BR>";

//execute the SQL query and return stations_registered data for $wpcall
try {
     $sql = "SELECT * FROM stations_registered WHERE ID = $wpcall";
     $q = $pdo->query($sql);
     $q->setFetchMode(PDO::FETCH_ASSOC);
     $crow = $q->fetch();
} catch (PDOException $e) {
     die("Error getting row data for station ID $wpcalllast: " . $e->getMessage());
}

// Display Data
print "<html><head><title>Data for Registered Station".
       $crow['CALL'].
       "</title></head><body>";
print "<h1>Operating Details for station ". $crow['CALLSIGN']."</h1>";
//print "<p>TABLE ID = ".$crow['ID']."<br>";
print "CALL = ".$crow['CALLSIGN']."<BR>";
print "NAME = ".$crow['NAME']."<BR>";
print "CLUB = ".$crow['CLUB']."<BR>";
print "MODE = ".$crow['MODE']."<BR>";
print "POWER = ".$crow['POWER']."<BR>";
print "CATEGORY = ".$crow['CATEGORY']."<BR>";
print "<hr><h3>OPERATOR COMMENTS:</h3>";
print $crow['COMMENTS']."<BR>";
//print "<hr><h3>SATURDAY COUNTY ACTIVATIONS REGISTERED:</h3>";
//print $crow['SAT_ROUTE']."<BR>";
//print "<hr><h3>SUNDAY COUNTY ACTIVATIONS REGISTERED:</h3>";
//print $crow['SUN_ROUTE']."<BR>";
print "</p>";
//
// Get Saturday route if it exists
try {
     $sql = "SELECT * FROM route_entries WHERE ROUTE_ID = ".$crow['SAT_ROUTE'];
     $sat = $pdo->query($sql);
     //$sat->setFetchMode(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
     die("Error getting row data for Saturday ROUTE_ID = ".$crow['SAT_ROUTE'].": " . $e->getMessage());
}

$sat_counties = '';
while ($sarow = $sat->fetch()) {
   $sql = "SELECT * FROM mocounties WHERE ID=".$sarow['COUNTY_ID'];
   $ctresult = $pdo->query($sql);
   $ctresult->setFetchMode(PDO::FETCH_ASSOC);
   $ctrow = $ctresult->fetch();
   $sat_counties .= $ctrow['code'].", ";
}

//
// Get Sunday route if it exists
try {
     $sql = "SELECT * FROM route_entries WHERE ROUTE_ID = ".$crow['SUN_ROUTE'];
     $sun = $pdo->query($sql);
     $sun->setFetchMode(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
     die("Error getting row data for Sunday ROUTE_ID = ".$crow['SUN_ROUTE'].": " . $e->getMessage());
}

$sun_counties = '';
while ($surow = $sun->fetch()) {
   $sql = "SELECT * FROM mocounties WHERE ID=".$surow['COUNTY_ID'];
   $ctresult = $pdo->query($sql);
   $ctresult->setFetchMode(PDO::FETCH_ASSOC);
   $ctrow = $ctresult->fetch();
   $sun_counties .= $ctrow['code'].", ";
}

print "<hr><h3>SATURDAY COUNTY ACTIVATIONS REGISTERED:</h3>";
print "<p>".$sat_counties."</p>";
print "<hr><h3>SUNDAY COUNTY ACTIVATIONS REGISTERED:</h3>";
print "<p>".$sun_counties."</p>";
//mysql_close($dbhandle);

// Close html form
print "</body></html>";

?>