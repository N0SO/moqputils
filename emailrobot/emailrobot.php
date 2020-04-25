<?php
include 'moqpconfig.php';
$raw = exec('cd /home/w0ma/email-robot; rm -f database.txt; python emailrobot.py >>robotlog.txt 2>&1');
#$raw = exec('cd ./cgi-bin; rm -f filesread.txt; python emailrobot.py >filesread.txt');
#$raw = file_get_contents('./cgi-bin/database.txt', true);
#$lines = explode('\n', $raw);
$lines = preg_split('/\r\n|\n|\r/', trim(file_get_contents('/home/w0ma/email-robot/database.txt')));
#echo $lines;
$count = 0;
foreach ($lines as $result) {
	#echo $count++."Result = ".$result."<br>";
	$resulta = explode(',', $result);
	if ( strlen($resulta[1]) >= 3 ) {
	   //
	   // Code to write to database goes here
	   //
	   try {
	      $conn = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
	      // set the PDO error mode to exception
	      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	      $sql = "INSERT INTO logs_received (STA_CALL,
	      					 OP_NAME,
	      					 EMAIL,
	                                         RECEIVED_BY,
	                                         FILENAME,
	                                         DATE_REC,
	                                         EMAILSUBJ)	
	      
	            VALUES ('$resulta[4]',
	                    '$resulta[6]',
	                    '$resulta[2]',
	                    '$resulta[1]',
	                    '$resulta[12]',
	                    '$resulta[0]',
	                    '$resulta[3]')";
	      // use exec() because no results are returned
	      $conn->exec($sql);
	      //echo "New record created successfully";
	   }
	   catch(PDOException $e) {
	      echo $sql . "<br>" . $e->getMessage();
	   }
	
	   $conn = null;  
	} 
}
?>