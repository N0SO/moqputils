<?php 
session_start(); 
$_SESSION['CNAME']=NULL;
$_SESSION['CID']=NULL;
$_SESSION['CCODE']=NULL;

header('location: routeplanner.php');
?>