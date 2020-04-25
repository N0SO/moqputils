<?php
     include 'moqpheader.php';
     include 'moqpconfig.php';
     include '../../countyform/routeutils.php';
     //connection to the database
     $pdo = opendb('moqpconfig.php');

     //Build query & fetch last DB update time stamp
     try {
         $sql = "SELECT MAX(DATE) FROM stations_registered";
         $q = $pdo->query($sql);
         //$q->setFetchMode(PDO::FETCH_ASSOC);
         $drow = $q->fetch();
         $update_date = $drow[0];
     } catch (PDOException $e) {
         die("Error getting last update date: " . $e->getMessage());
         
     }
?>

<html>
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<title>Tabular List of Known County Activations for <?php echo $year;?></title>
        <link rel="stylesheet" type="text/css" href="../default.css">
</head>
<body>

<h1 align="center">Tabular List of Known Missouri County Activations for <?php echo $year;?></h1>
<!--                          
<?
draw_moqpheader('../../img/','./');
?>

<p align="center"><a href="http://cwfun.org/funspots/moqp/">Missouri QSO Party Special Event Spotter Page</a> </p>
-->                             

<p align="center"><i>Updated: <?php echo $update_date; ?> UTC</i></p>
<p align="center"><B>NOTE: </B>Clicking on a callsign in the list below will display all<br> 
                               known information about that stations operating plans.</p>
<!--
<p align="center">             This page is a work in progress. Want to help us test it? <br>
                               Enter your planned activation information 
                               <a href="../../countyform/" target = "blank">HERE</a>
                               and it will <br>
                               automatically show up on this page. Hopefully you will not have any<br>
                               troubles. But if you do, 
                               <a href="mailto: n0so@w0ma.org">e-mail us</a> the details.
                               We can correct the<br> information directly in the database if necessary.</p>
-->                             
<hr />

<center>
<table border="1" cellpadding="0">
   <tbody>
      <tr>
         <td valign="top" bgcolor="#99CCFF"><b>Missouri County</b></td>
         <td valign="top" bgcolor="#99CCFF"><b>Modes</b></td>
         <td valign="top" bgcolor="#99CCFF"><b>Callsign</b></td>
     </tr>
 
     <?php

     //execute the SQL query and return county
     $sql = "SELECT * FROM mocounties";
     $c = $pdo->query($sql);
     $c->setFetchMode(PDO::FETCH_ASSOC);

     //Loop through the county table 
     while ($crow = $c->fetch()) {
        $county_ID=$crow['ID'];
        $county_name=$crow['name'];
        $county_code=$crow['code'];
        print "<td valign='top' bgcolor='#99CCFF'><b>$county_name ($county_code)</td>";
        $sql = "SELECT DISTINCT STATION_ID FROM route_entries WHERE COUNTY_ID = $county_ID";
        $s = $pdo->query($sql);
        $s->setFetchMode(PDO::FETCH_ASSOC);

        $modes = "";
        $calls = "";  
        // Loop through all route_entries selected and fetch the MODE and CALL  
        // from the station_registered table the station station_ID represents 
        while ($rrow = $s->fetch()) {
           // Select the station for this county
           $station = $rrow['STATION_ID'];
           $sresult = $sql = "SELECT * FROM stations_registered where ID = $station";
           $i = $pdo->query($sql);
           $i->setFetchMode(PDO::FETCH_ASSOC);
           $srow = $i->fetch();
           $modes .= $srow['MODE']."<BR>";
           $calls .= "<a href='getstationinfo.php?call=".
                     $station."' TARGET='_blank'>".$srow['CALLSIGN']."</a>"."<BR>";
        }
        if ($modes)
           print "<td>$modes</td>";
        else
           print "<td>&nbsp;</td>";
        
        if ($calls)
           print "<td>$calls</td>";
        else
           print "<td>&nbsp;</td>";
           
        print "<tr>";
     }
     ?>
   </tbody>
</table>
</center>
</body>
</html>