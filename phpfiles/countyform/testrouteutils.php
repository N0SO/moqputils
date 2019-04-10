<?php
// the message
$msg = "First line of text\n";
$msg .= "Second line of text\n";
$msg .= "Third line of text\n";

// use wordwrap() if lines are longer than 70 characters
$msg = wordwrap($msg,70);

// send email
mail(
      "mheitmann@n0so.net",
      "My subject Two",
      $msg,
      "FROM: mikeheit@aol.com\n\r");

echo test_input("This is a test of ''''' single ''''quotes.")."<br>";
echo test_input('This is a test of """"" double """""" quotes.')."<br>";
#echo test_input("This is a test of ''''' single ''''quotes.")."<br>";
#echo test_input("This is a test of ''''' single ''''quotes.")."<br>";




function test_input($data)
{
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  #$data = mysql_real_escape_string($data);
  $data = str_replace("'","\'",$data);
  $data = str_replace('"',' ',$data);

  return $data;
}
?>
