<?php 
session_start(); 
//$day=$_GET['day'];
//$day=strtolower($day);
$day=trim( strtolower($_SESSION['day']) );

switch ($day) {
    case "saturday":
        $_SESSION['saturday'] = $_SESSION['CNAME'];
        $_SESSION['idsaturday'] = $_SESSION['CID'];
        $_SESSION['cdsaturday'] = $_SESSION['CCODE'];
        $_SESSION['day'] = "Sunday";
        $returnurl = 'routeplanner.php';
        break;
    case "sunday":
        $_SESSION['sunday'] = $_SESSION['CNAME'];
        $_SESSION['idsunday'] = $_SESSION['CID'];
        $_SESSION['cdsunday'] = $_SESSION['CCODE'];
        $returnurl = 'confirm.php';
        break;
    default:
        print 'No case defined! Day = ' . $day;
        break;
}

$_SESSION['CID']=NULL;
$_SESSION['CCODE']=NULL;
$_SESSION['CNAME']=NULL;

header('location: '. $returnurl);
?>