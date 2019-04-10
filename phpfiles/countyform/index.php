<?php
//Start a new session and display form if user has not clicked submit
include 'moqpconfig.php';
session_start();
include 'routeutils.php';
if (!isset($_POST["submit"]))
  {
  ?>
  <html>
  <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     <title>Activate Your County for the Missouri QSO Party</title>
     <link rel="stylesheet" type="text/css" href="../default.css">
  </head>
  <body>

  <h2 align = "center">Tell Us Which Missouri Counties You Will Activate for the Missouri QSO Party</h2>
  <p>
  Please use this series of forms to let us know which Missouri county or counties you plan 
  to activate for the <?php echo $year;?> Missouri QSO Party. 
  </p>
  <p>
  First, we need some operator information about you or your group and what your operating plans are. 
  Please fill in the information requested below. When you are ready, please click the button marked 
  Pick Saturday Counties.
  <p>
  Alternately, this information may be sent via e-mail (not this form) to 
  <a href="http://w0ma.org/index.php/information/planned-activations/send-us-your-plans-by-e-mail" target="_BLANK">
  Missouri QSO Party County Activation Cordinator.</a>
  <p>
  The information entered here (or sent by e-mail) will be used to update the 
  <a href="http://w0ma.org/index.php/moqp-history/2019/2018-county-activations/view-2019-activation-plans"  
              target="_BLANK">List of known <?php echo $year;?> County Activations</a> pages. <br>
  </p>
  <form method="post" action="<?php echo $_SERVER["PHP_SELF"];?>">
  <br>
  <fieldset>
  <legend><b>Operator/Group Information</b></legend>
  <p>Call: <input name="call" type="text" id="call" size="12" style="text-transform: uppercase"> 
  <p>Name: <input name="name" type="text" class="drop" id="name" size="20">
  <p>Club: <input name="club" type="text" class="drop" id="club" size="20" default = "Single Op"> For clubs or multi-op stations, enter club name or additional op callsigns.<br>
  <p>E-Mail: <input type="email" name="from" id="from" type="text" class="drop"><br>
  </fieldset>
  <fieldset>
  <legend><b>Planned Modes, Power and Category</b></legend>
  <p>Mode: <select name="mode" class="input" id="mode">
           <option value="0">Mode - Select One</option>
           <option value="CW">- HF - CW </option>
           <option value="PHONE">- HF - PHONE</option>
           <option value="DIGITAL">- HF - DIGITAL</option>
           <option value="MIXED">- HF SSB, CW, DIGITAL (MIXED)</option>
        </select>
  <p>Power:  <select name="power" class="input" id="power">
             <option value="0" selected="selected">Power - Select One</option>
             <option value="QRP">- QRP (5 watts or less)</option>
             <option value="LOW">- LOW (150 watts or less, not QRP )</option>
             <option value="HIGH">- HIGH (greater than 150 watts)</option>
          </select><br>
  <p>VHF/UHF Operation: <input type="radio" name="VHF"
                        <?php if (isset($VHF) && $VHF=="yes") echo "checked";?>
                        value="YES">yes
                        <input type="radio" name="VHF"
                        <?php if (isset($VHF) && $VHF=="no") echo "checked";?>
                        value="NO">no<br>
 <p>Category: <select name="category" class="input" id="category">
               <option value="0" selected="selected">Category - Select One</option><br>
               <option value="FIXED SINGLE OP">- Fixed Single Operator</option>
               <option value="FIXED MULTI OP">- Fixed Multi-Op</option>
               <option value="MOBILE SINGLE OP">- Mobile Single-Op</option>
               <option value="MOBILE MULTI OP">- Mobile Multi-Op</option>
               <option value="MOBILE UNLIMITED">- Mobile Unlimited</option>
               <option value="EXPEDITION">- Expedition</option>
            </select><br>
  </fieldset>
  <br>
<!--
  <p>Message/Comments: <textarea rows="10" cols="60" name="message"></textarea><br>
-->
  <input type="submit" name="submit" value="Pick Saturday Counties">
  </form>
  </body>
  </html>
  <?php
  }
else
  // the user has submitted the form
  {
  // define variables and set to empty values
  #$call = $name = $club = $mode = $power = $category = $saturday = $sunday = $message = $errormessage = "";
  // Check if the "from" input field is filled out
  if (isset($_POST["from"]))
    {
       //print "Post was set!";
       // Fetch data from the form
       $call = test_input($_POST["call"]);
       $name = test_input($_POST["name"]);
       $club = test_input($_POST["club"]);
       $from = test_input($_POST["from"]);
       $mode = test_input($_POST["mode"]);
       $power = test_input($_POST["power"]);
       $category = test_input($_POST["category"]);
       $VHF = $_POST['VHF'];
       $saturday = test_input($_POST["saturday"]);
       $sunday = test_input($_POST["sunday"]);
       $message = test_input($_POST["message"]);
       // message lines should not exceed 70 characters (PHP rule), so wrap it
       //$saturday = wordwrap($saturday, 70);
       //$sunday = wordwrap($sunday, 70);
       $message = wordwrap($message, 70);
       // Check form data for errors
       if ($call == "") 
           $errormessage = "Please enter your callsign in the call field";
       elseif ($name == "")
           $errormessage = "Please enter your name in the name field";
       //elseif ($club == "")
           //$errormessage = "Please enter your club name, additional callsigns if you are a group or N/A if an individual in the club field";
       elseif ($from == "")
           $errormessage = "Please enter your e-mail address in the e-mail field";
       elseif ($mode == "0")
           $errormessage = "Please select your planned mode of operation in the mode field";
       elseif ($power == "0")
           $errormessage = "Please select your planned power level in the power field";
       elseif ($category == "0")
           $errormessage = "Please select your planned operating category in the category field";
       //elseif ($saturday == "")
       //    $errormessage = "Please enter the Missouri counties you plan to activate on Saturday";
       //elseif ($sunday == "")
       //    $errormessage = "Please enter the Missouri counties you plan to activate on Sunday";
       //elseif ($message == "")
       //    $errormessage = "Please enter the Missouri counties you plan to activate in the message field";
       if ($errormessage == "") {
          // Put all this stuff into session variables and pass on the the next routine
	  $_SESSION['call']= $call;
          $_SESSION['name']=$name;
          $_SESSION['club']=$club;
          $_SESSION['from']=$from;
          $_SESSION['mode']=$mode;
          $_SESSION['power']=$power;
          $_SESSION['vhf']=$VHF;
          $_SESSION['category']=$category;
          $_SESSION['saturday'] = "";
          $_SESSION['sunday']="";
          $_SESSION['message']=$message;
          $_SESSION['day']='Saturday';
          header("location: routeplanner.php?day=Saturday");

       }
       else 
       { 
          echo "<p><b>Error:</b> ". $errormessage . "<br>";
          echo "<p>Please use your browser back button to correct, then click the send button again.<br>";
          unset($_POST["submit"]);
       }
       //echo '<pre>';
       //var_dump($_SESSION);
       //echo '</pre>';
    }
  }
?>

