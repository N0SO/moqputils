<?php
session_start();
//echo '<pre>';
//var_dump($_SESSION);
//echo '</pre>';
//header("location: routeplanner.php?day=Saturday");
?>
  <html>
  <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     <title>Confirmation Pae</title>
     <link rel="stylesheet" type="text/css" href="../default.css">
  </head>
  <body>
  <h2 align = "center">Is the information below correct?</h2>
  <form method="post" action="submit.php">
  <br>
  <fieldset>
  <legend><b>Operator/Group Information</b></legend>
  <p>Call: <input name="call" type="text" id="call" size="12" style="text-transform: uppercase" value="<?php echo $_SESSION['call']?>" /> 
  <p>Name: <input name="name" type="text" class="drop" id="name" size="20" value="<?php echo $_SESSION['name']?>" />
  <p>Club: <input name="club" type="text" class="drop" id="club" size="20" default = "Single Op" value="<?php echo $_SESSION['club']?>" /> For clubs or multi-op stations, enter club name or additional op callsigns.<br>
  <p>E-Mail: <input type="email" name="from" id="from" type="text" class="drop" value="<?php echo $_SESSION['from']?>" /><br>
  </fieldset>
  <fieldset>
  <legend><b>Planned Modes, Power and Category</b></legend>
  <p>Mode: <input name="mode" class="input" id="mode" value="<?php echo $_SESSION['mode']?>" readonly="readonly"/>
  <p>Power:  <input name="power" class="input" id="power" value="<?php echo $_SESSION['power']?>" readonly="readonly"/>
  <p>VHF/UHF Operation: <input type="radio" name="VHF"
                        <?php if ($_SESSION['vhf'] =="YES") echo "checked";?>
                        value="YES">yes
                        <input type="radio" name="VHF"
                        <?php if ($_SESSION['vhf'] =="NO") echo "checked";?>
                        value="NO">no<br>
 <p>Category: <input name="category" class="input" id="category" value="<?php echo $_SESSION['category']?>" readonly="readonly"/>
 </fieldset>
<fieldset>
    <legend><b><?php echo $day?> Saturday Counties List</b></legend>
    <textarea name="satcounties"  
          cols="40" rows="5" 
          readonly="readonly">
          <?php echo $_SESSION['saturday']; ?>
          </textarea>
</fieldset>
 <fieldset>
    <legend><b><?php echo $day?> Sunday Counties List</b></legend>
    <textarea name="suncounties"  
          cols="40" rows="5" 
          readonly="readonly">
          <?php echo $_SESSION['sunday']; ?>
          </textarea>
</fieldset>
<br>
  <p>Please enter any comments or extra information you want people to see along with your list of counties:</p>
  <textarea rows="10" cols="60" name="message"></textarea><br>
  <input type="submit" name="submit" value="Yes, ready to record submit">
  </form>
  <form method="post" action="index.php">
  <input type="submit" name="reset" value="No, I need to update">

  </body>
  </html>

