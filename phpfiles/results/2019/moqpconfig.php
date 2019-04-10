<?php
   // Global MOQP configurtion file. 
   // Put stuff that changes year to year here.
   // Connection info for the moqp database
   $username = "w0ma_moqp";
   $password = '$MOQPdata';
   $hostname = "localhost";
   $year='2019';
   $dbname = 'w0ma_moqp_'.$year;
   // File paths
   $LOGROOT = '/home/w0ma/mo_qso_party/results/'.$year.'/logs/';
   $LOGPATH = $LOGROOT.'submitted/';
   $LOGWAIT = $LOGROOT.'waiting/';
   $LOGREADY = $LOGROOT.'ready/';
   $LOGFURTHER = $LOGROOT.'humanreview/';

   $DATAPATH='results/'.$year;
   $UPLOAD_DIR='logs/submitted';
   // List of log processors e-mail addresses
   // parse-form.php will send an e-mail to each address when a logfile
   // has been successfully uploaded to W0MA.ORG
   // If this list is updated, the one in cgi-bin/robotconfig.py also needs to be updated.
   //$LOGPROCESSORS = 'n0so@w0ma.org, Randall.wing@gmail.com, ad0dx@yahoo.com';
   $LOGPROCESSORS = 'n0so@w0ma.org';
?>