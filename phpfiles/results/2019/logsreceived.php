<html>
<?php
   include "moqpconfig.php";
   include '/home/w0ma/mo_qso_party/countyform/routeutils.php';

?>
<head>
	<title><?php echo $year;?> MOQP Logs Received</title>
</head>
<body bgcolor="#E6E6FA">
<h1 style="text-align: center;"><?php echo $year;?>  Missouri QSO Party Logs Received</h1>
<hr />
<!--
<table border="0" cellpadding="1" cellspacing="1" style="width: 500px;" summary="Test" align="center">
      <tbody>
      <tr>
        <td>
         <form action="" method="get">
          <fieldset>
            <legend>Search for a Call</legend>
            Call: <input type="text" name="call">&nbsp; (leave blank to see all)&nbsp;&nbsp;&nbsp;
            <input type="submit"><br>Sort by:
            <input type="radio" name="sort_type" value="No Sort" checked>No Sort
            <input type="radio" name="sort_type" value="Call Sign" checked>By Callsign
            <input type="radio" name="sort_type" value="Date">By Date
          </fieldset>
         </form>
        </td>
      </tr>   
      </tbody>
 </table>
-->
<table border="0" cellpadding="1" cellspacing="1"  summary="Test" align="center">
      <tbody>
<!--
      <tr>
         <td valign="top" bgcolor="#99CCFF"><b>STATION CALL</b></td>
         <td valign="top" bgcolor="#99CCFF"><b>DATE RECEIVED</b></td>
     </tr>
-->
<tr>
<td>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
<td>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
<td>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
<td>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
<td>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
</tr>
<Caption>Logs received from the following stations:</caption>
<?php
   //include "../moqpconfig.php";
   
   // Get call to search for from form
   if (isset($_GET["call"])) {
      $srch_call = $_GET["call"];
      $sort_type = $_GET["sort_type"];
      if ($srch_call == '')
         $srch_call = "%";
   }
   else {
      $srch_call = '%';
      $sort_type = 'Call Sign';
   }
#   if ( (strlen($srch_call) > 1) and (strlen($srch_call) %2 == 1) ) {
#      // If string length is odd, pad the 1st char with a space
#      $srch_call = ' '.$srch_call;
#   }
      
   // Get sorting options
   if ($sort_type == "No Sort")
      $order_by = "ID";
   elseif ($sort_type == "Call Sign")
      $order_by = "STA_CALL";
   elseif ($sort_type == "Date")
      $order_by = "DATE_REC";
      
   //connection to the database
   $db_handle = opendb('moqpconfig.php');

   if ($db_handle) {

      try {
         $sql = "SELECT DISTINCT STA_CALL FROM logs_received WHERE RTRIM(LTRIM(STA_CALL)) LIKE RTRIM(LTRIM('$srch_call')) ORDER BY $order_by";
         $result = $db_handle->query($sql);
         $result->setFetchMode(PDO::FETCH_ASSOC);
         $rowcount = 0;
         while ( $db_field = $result->fetch() ) {
            If ($rowcount == 0) print "<tr>";
               print "<td valign='top'><b>".$db_field['STA_CALL'] . "</b></td>";
               #print "<td valign='top'><a href='./$DATAPATH/$UPLOAD_DIR/".$db_field['FILENAME'] . "'>".$db_field['FILENAME'] . "</a></td>";
               #print "<td valign='top'>".$db_field['FILENAME'] . "</td>";
               #print "<td valign='top'>".$db_field['DATE_REC'] . "</td>";
               $rowcount = $rowcount + 1;
               If ($rowcount == 5) {
                  print "</tr>";
                  $rowcount = 0;
               }
         }
         print "</tbody><br></table>";
         $SQL2 = "SELECT COUNT(DISTINCT(STA_CALL)) FROM logs_received";
         $result2 = $db_handle->query($SQL2);
         //$result2->setFetchMode(PDO::FETCH_ASSOC);
         $count = $result2->fetch();
         $SQL3 ="select max(DATE_REC) from logs_received";
         $result3 = $db_handle->query($SQL3);
         $latest = $result3->fetch();
         #print "<hr>";
         #print "<p align = 'center'>Search for call sign: ". strtoupper($srch_call).", sorted by: $sort_type</p>";
         #print "<p align = 'center'>".$count[0]." unique log files received as of ".gmdate('Y/m/d G:i:s')." UTC</p>";
         print "<p align = 'center'>".$count[0]." unique log files received as of ".$latest[0]." UTC</p>";
         #print "<p align = 'center'>".$SQL."</p>";
         //mysql_close($db_handle);

      } catch (PDOException $e) {
         die("Error getting last update date: " . $e->getMessage());
         
      }

   }
   else {
      print "Database NOT Found ";
      //mysql_close($db_handle);
   }
?>

<hr>
<!--
<p>
Here are a few log submission tips:
</p>
<ol>
<li>Cabrillo file format is preferred.</li>
<li>Name your logfile with your callsign. Example: W0MA.LOG or W0MA.TXT or W0MA.xls (if using our excel template).
<li>Leave the '/x' designators out of the file name and e-mail title (W0MA.LOG instead of W0MA/M.LOG for a filename, W0MA instead of W0MA/M as an e-mail title). The '/' symbol cannot be used in a file name.
<li>When submitting by e-mail, make the subject of the e-mail your callsign and nothing else, or the robot may reject your e-mail as SPAM.
<li>Check back after submitting. In 15 minutes your log should appear in the list above. If it doesn't appear, try resubmitting it after rechecking the file name and e-mail title as listed above.
</ol>
<p>
Thanks again to all of you for making the MOQP fun this year!
</p>

-->
<p>
If your call sign does not appear in the list above withing 15-20 minutes of submission, please take a look at the <i>Log Submission Tips</i> on our 
<i> MOQP Log Submission </i> page via the link below.
</p>
<hr/>
<table border="0" cellpadding="1" cellspacing="1" style="width: 500px;" align = 'center'>
	<tbody>
		<tr>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php">W&Oslash;MA Home</a></td>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php/missouri-qso-party">MOQP Home</a></td>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php/9-moqp/26-submitting-your-log-for-the-missouri-qso-party">MOQP Log Submission</a></td>
		</tr>
	</tbody>
</table>


</body>
</html>
