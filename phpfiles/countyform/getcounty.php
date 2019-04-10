<?php
session_start();
require_once 'routeutils.php';
require_once 'moqpconfig.php';
//include '../common/moqpheader.php';
// The value of the variable name is found
$wpcounty= $_GET['county'];
//echo "<h1>Adding county $wpcounty</h1>";

//connection to the database
$pdo = opendb('moqpconfig.php');

//Build query
$sql = "SELECT * FROM mocounties WHERE code = '".$wpcounty."'";
$q = $pdo->query($sql);
$q->setFetchMode(PDO::FETCH_ASSOC);

//execute the SQL query and return county data for $wpcounty
//$cresult = mysql_query("SELECT * FROM mocounties WHERE code = '".$wpcounty."'")
//   or die("No return for $wpcounty query.");

//$crow = mysql_fetch_array($cresult)
//   or die("No row data for $wpcounty");
//print "ID = ".$crow['ID']."<BR>";
//print "NAME = ".$crow['name']."<BR>";
//print "CODE = ".$crow['code']."<BR>";
$crow = $q->fetch();
$ID=$crow['ID'];
$name = $crow['name'];
$code = $crow['code'];
//mysql_close($dbhandle);

if( $_SESSION['CID'] == NULL ) {
      $_SESSION['CID'] = $ID;
      $_SESSION['CNAME']= $name;
      $_SESSION['CCODE']= $code;
}
else {
      $_SESSION['CID'] .=  ','.$ID;
      $_SESSION['CNAME'] .= ','.$name; 
      $_SESSION['CCODE'] .= ','.$code; 
}
//print $ID.$name.$code.'<br>';
//print $_SESSION['ID'].$_SESSION['CNAME'].$_SESSION['CCODE'];
//echo '<pre>';
//var_dump($_SESSION);
//echo '</pre>';
//print "<html>";
//print "<head>";
//print "<title>$name County Selected </title>";
//print "</head>";
//print "<body>";

//print '<p align="center">';
//print "<form method='post' action='routeplanner.php'>";
//print "Adding ID: $ID, County: $name, County Code: $code<br>";
//print '<input type="submit" name="CID" value="Add" />';
//print "</form></p>";

//print "</body>";
//print "</html>";


header("location: routeplanner.php?day=Saturday");
?>