<?php

function test_input($data)
{
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  #$data = mysql_real_escape_string($data);
  $data = str_replace("'","\'",$data);
  #$data = str_replace('"',' ',$data);

  return $data;
}

function opendb($configfile)
{
     include  $configfile;
     //echo $hostname.'...'.$username.'...'.$password.'...'.$dbname;
     
     //connection to the database
     try {
     $pdo = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
     return $pdo;
    } catch (PDOException $e) {
         die("Could not xxx connect to the database $dbname :" . $e->getMessage());
    }

}
?>
