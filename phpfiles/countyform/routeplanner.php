<?php 
session_start(); 
$day=$_SESSION['day'];
?>

<html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <title>Report Your County Activation Plans for the Missouri QSO Party</title>
   <link rel="stylesheet" type="text/css" href="../default.css">
</head>
<body>
  <h3 align = "center">Counties and Routes You Plan to Activate on <?php echo $day?></h3>
  <p>Click on the counties you plan to activate. They will be added to the text box at the
     bottom of this page. Hovering your mouse over the county name on the map should show 
     the full name with most web browsers. Click on the SAVE button next to the county list 
     text box when you are done and ready to move to the next step. </p>
  <hr>
  <p allign="center" style="text-align: center;">

  <?php drawMOCountiesMap("./moqpconfig.php"); ?>

<hr>
<p>
<form method="post" action="./togglerouteday.php" >
<fieldset>
    <legend><b><?php echo $day?> Counties List</b></legend>
    <textarea name="counties"  
          cols="40" rows="5" 
          readonly="readonly">
          <?php echo $_SESSION['CNAME']; ?>
          </textarea>
    <input type="submit" name="submit" value="Save <?php echo $day?> List"> 
</fieldset>
</form>
<form method="post" action="./resetroute.php" >
   <input type="submit" name="submit" value="Clear the List"> </p>
</form>
<p align="center"> The SAVE button saves the current list and moves to the next step.
</p>
</body>

</html>

<?php
function drawMOCountiesMap($configfile){
     include $configfile;
     
     //Display map image
     print '<img alt="Active Modes" src="routplanmap.png" usemap="#mocounties"  ismap="ismap" />';
     
     //connection to the database
     $pdo = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
     //echo "Connected to $hostname...<br>";
     
     //Build query
     $sql = 'SELECT * FROM mocounties';
     $q = $pdo->query($sql);
     $q->setFetchMode(PDO::FETCH_ASSOC);
     
     // Start building the map links
     print '<map name="mocounties">';

     //execute the SQL query
     //($r = $q->fetch());

     // Loop through the county entries and create county links
     while ($crow = $q->fetch()) {
        $county_ID=$crow['ID'];
        $county_name=$crow['name'];
        $county_code=$crow['code'];
        //$coords="405,67,22";
        $coords=$crow['coords'];
        print '<area shape="circle" coords="'.$coords.'" href="./getcounty.php?county='.$county_code.'" title="'.$county_name.', '.$county_code.'">';
     
     }
     print '</map>';
}

?>