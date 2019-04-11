<?php
   // Global MOQP configurtion file.
   // Put stuff that changes year to year here.
   // Connection info for the moqp database
   //Fill in your database host, userID, name and password
   $username = "         ";
   $password = '         ';
   $hostname = "localhost";
   $year='2019';
   $dbname = 'basname'.$year;
   // File paths
   $LOGROOT = './results/'.$year.'/logs/';
   $LOGPATH = $LOGROOT.'submitted/';
   $LOGWAIT = $LOGROOT.'waiting/';
   $LOGREADY = $LOGROOT.'ready/';
   $LOGFURTHER = $LOGROOT.'humanreview/';

   $DATAPATH='results/'.$year;
   $UPLOAD_DIR='logs/submitted';
   // List of log processors e-mail addresses separated by commas.
   // If this list is updated, the one in cgi-bin/robotconfig.py also needs to be updated.
   $LOGPROCESSORS = 'youremail@host.com';
?>