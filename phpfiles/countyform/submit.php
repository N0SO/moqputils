<?php
session_start();
include './moqpconfig.php';
include 'routeutils.php';

//Parse and fixup input parameters
$callsign = strtoupper( test_input($_SESSION['call']) );
$name = test_input($_SESSION['name'] );
$club = test_input($_SESSION['club'] );
$email = test_input($_SESSION['from'] );
$mode = test_input($_SESSION['mode'] );
$power = test_input($_SESSION['power'] );
$category = test_input($_SESSION['category'] );
$comments = test_input($_POST['message']);
$saturday = test_input($_SESSION['saturday']);
$sunday = test_input($_SESSION['sunday']);
$vhf = test_input($_SESSION['vhf']);

$myDate = gmdate('Y-m-d-G-i-s');

//
// Open database
//
//connection to the database
$dbhandle = mysqli_connect($hostname, $username, $password, $dbname)
  or die("Unable to connect to database!");
#echo "Connected to $hostname...<br>";
//$pdo = opendb('moqpconfig.php');

//Check to see if this operator already has a route entry
//If so, replace it with the new data.
$sql = "SELECT * FROM stations_registered WHERE callsign = '".$callsign."'";
$cresult = mysqli_query($dbhandle, $sql);
if ($cresult->num_rows > 0) {  
   // Delete the previous route data
   $row = $cresult->fetch_assoc();
   $staid = $row['ID'];
   $satrouteid = $row['SAT_ROUTE'];
   $sunrouteid = $row['SUN_ROUTE'];
   $deletemsg = "You had older county activation information already in the database. It was replaced with the data displayed above.";
   $sql = "DELETE FROM route_entries WHERE STATION_ID = '".$staid."'";
   if (! mysqli_query($dbhandle, $sql) ) {
         echo "Error: " . $sql . "<br>" . mysqli_error($dbhandle) ."<br>";
   }
   $sql = "DELETE FROM routes WHERE STATION_ID = '".$staid."'";
   if (! mysqli_query($dbhandle, $sql) ) {
         echo "Error: " . $sql . "<br>" . mysqli_error($dbhandle) ."<br>";
   }
   $sql = "DELETE FROM stations_registered WHERE ID = '".$staid."'";
   if (! mysqli_query($dbhandle, $sql) ) {
         echo "Error: " . $sql . "<br>" . mysqli_error($dbhandle) ."<br>";
   }
   
}
else {
   $deletemsg="If you need to update this information, just enter it again. The new information you enter will replace the old information.";
}
//Write op info to stations_registered table of DB
$sql = "INSERT INTO stations_registered (CALLSIGN, 
                                            NAME, 
                                            CLUB, 
                                            EMAIL, 
                                            MODE, 
                                            POWER,
                                            CATEGORY,
                                            VHF,
                                            COMMENTS,
                                            DATE )
        VALUES ('$callsign',
           	    '$name',
           	    '$club',
           	    '$email',
           	    '$mode',
           	    '$power',
           	    '$category',
           	    '$vhf',
           	    '$comments',
           	    '$myDate')";
//print $sql;
if (mysqli_query($dbhandle, $sql)) {
       //echo "New record created successfully";
} 
else {
       echo "Error: " . $sql . "<br>" . mysqli_error($dbhandle) ."<br>";
}
// Get the station ID from the stations_registered table.
// This should be the last record inserted above.
// The mysqli_insert_id() will fetch it for us.
$station_id=mysqli_insert_id($dbhandle);
$countyids = test_input($_SESSION['idsaturday']);  
if ($countyids != NULL) {
       // Enter Saturday route for this station
       $satroute = parse_route($dbhandle, $station_id, $countyids, $myDate, 'SAT');
}
$countyids = test_input($_SESSION['idsunday']);  
if ($countyids != NULL) {
       // Enter Sunday route for this station
       $sunroute = parse_route($dbhandle, $station_id, $countyids, $myDate, 'SUN');
}
// write $satroute and $sunroute to stations_registered table
$sql = "UPDATE stations_registered 
                   SET SAT_ROUTE ='$satroute', SUN_ROUTE = '$sunroute' 
                   WHERE ID='$station_id'";
if (mysqli_query($dbhandle, $sql)) {
       //echo "New route records created successfully";
} 
else {
       echo "Error: " . $sql . "<br>" . mysqli_error($dbhandle);
}
mysqli_close($dbhandle);

//echo '<pre>';
//var_dump($_SESSION);
//echo '</pre>';
$contact = "[Information]---------------------------------\n";
$contact .= "Name: ". $name." \r\n";
$contact .= 'Email: '. $email." \r\n";
$contact .= 'Callsign: '.$callsign." \r\n";
$contact .= 'Club: '.$club." \r\n";
$contact .= "[Address]---------------------------------\n";
$contact .= "IP: ".getenv("REMOTE_ADDR")." (".gethostbyaddr(getenv("REMOTE_ADDR")).") \r\n";
$contact .= "[Activation Info]---------------------------------\r\n";
$contact .= 'Modes: '.$mode." \r\n ";
$contact .= 'Power: '.$power." \r\n ";
$contact .= 'Category: '.$category." \n ";
$contact .= 'Saturday County / Routes: '.$saturday." \r\n ";
$contact .= 'VHF/UHF: '.$vhf." \r\n";
$contact .= 'Sunday County / Routes: '.$sunday."  \r\n ";
$contact .= "[Message / Comments]---------------------------------\r\n";
$contact .= 'Message / Comments: '.$comments." \r\n ";
// Save data in activations folder
//$myDate = gmdate('Y-m-d-G-i-s');
//$myFile = "activations/".$callsign."-$myDate.txt";
//#$fh = fopen($myFile, 'w');
//#echo fwrite($fh,$contact);
//#fclose($fh);
$contact .= "This information has also been saved on w0ma.org in the ".$dbname."  database. \r\n";
$contact .= "To access go to http://w0ma.org/mo_qso_party/results/".$year."/activecountiestabular.php \r\n";
$contact .= "and click on ".$callsign." in one of the active counties shown. \r\n";

// send mail
//$route_recipients = "n0so@w0ma.org"; // for debug
$route_recipients = "n0so@w0ma.org,Randall.wing@gmail.com"; // for debug
mail(
      $route_recipients,
      "[New MOQP County Activation Registration] by $callsign",
      $contact,
      "FROM: $email\n\r");
?>

<html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <title>Your Activation Has Been Submitted</title>
   <link rel="stylesheet" type="text/css" href="../default.css">
</head>
<body>

<h3 align = "center">Thank you for activating the county or counties you plan to operate in.</h3>
<hr>
<p>Here is a summary of the information you submitted:<br>

<?php
echo "Call = ". $callsign ."<br>";
echo "Name = ". $name ."<br>";
echo "Club = ". $club ."<br>";
echo "E-Mail = ". $email ."<br>";
echo "Mode = ". $mode ."<br>";
echo "Power = ". $power ."<br>";
echo "Category = ". $category ."<br>";
echo "VHF/UHF Active? $vhf<br>";
echo "Saturday Counties / Routes = ". $saturday ."<br>";
echo "Sunday Counties / Routes = ". $sunday ."<br>";
echo "Message / Comments = ". $comments ."<br>";
#echo "Contact e-mail data: $contact<br>";

echo "<p>$deletemsg</p>";
?> 
<hr>
<p>Should you find that you are unable to honor your commitment in time, please drop a note to:<br>
          	<a href="http://w0ma.org/index.php/information/planned-activations/send-us-your-plans-by-e-mail" target="_BLANK">Missouri QSO Party Activation Cordinator.</a> and lets us know.<br>
<p>Best regards and good luck!<br>
<p align='center'><a href="http://w0ma.org/mo_qso_party/">Return to the MOQP Home Page</a></p>
</body>
</html>

<?php
function parse_route($db, $stationID, $countyIDs, $theDate, $theDay) {
   $idlist = explode(",",$countyIDs);
   $idcount = count($idlist);
   if ( $idcount > 0) {
      // create entry in route table for this route
      $sql = "INSERT INTO routes (STATION_ID,
                                    EVENT_DAY,
                                    DATE)
              VALUES ('$stationID',
           	        '$theDay',
           	        '$theDate')";
      //print "$sql <br>";
      if (mysqli_query($db, $sql)) {
          $routeid=mysqli_insert_id($db);
          //print "Return from mysqli_insert_id() = $routeid<br>";
          //query for the ID of the route just created
          //$sql = "SELECT * FROM routes WHERE STATION_ID = '".$stationID."'";
          //$cresult = mysqli_query($db, $sql); 
          //$row = $cresult->fetch_assoc();
          //$routeid = $row["ID"];  
          //echo "New $theDay route record created successfully";
          for($i = 0, $c = count($idlist); $i < $c; $i++) {
             // Add county waypoint for this route
             //print "Saving $theDay county $idlist[$i]...<br>";
             $sql = "INSERT INTO route_entries (ROUTE_ID,
                                                  STATION_ID,
                                                  ROUTE_SEQ,
                                                  COUNTY_ID,
                                                  DATE)
                      VALUES (   '$routeid',
                                 '$stationID',
           	                 '$i',
           	                 '$idlist[$i]',
           	                 '$theDate')";
             if (! mysqli_query($db, $sql)) {
                echo "Error: " . $sql . "<br>" . mysqli_error($db) ."<br>";
             }
          }  
      } 
      else {
          echo "Error: " . $sql . mysqli_error($db) ."<BR>";
      }

   }
   else {
      print "No county IDs found. countyIDs = $countyIDs<br>";
   }
   return $routeid;
}

        