<?php
// grab recaptcha library
require_once "recaptchalib.php";
include 'moqpconfig.php';

// your secret key
$secret = "Your_Key_Goes_Here";

// empty response
$response = null;
 
// check secret key
$reCaptcha = new ReCaptcha($secret);

// if submitted check response
if ($_POST["g-recaptcha-response"]) {
       $response = $reCaptcha->verifyResponse(
           $_SERVER["REMOTE_ADDR"],
           $_POST["g-recaptcha-response"]
       );
}
$postData = $uploadedFile = $statusMsg = '';
$msgClass = 'errordiv';

if(isset($_POST['submit'])){
  // Get the submitted form data
  $postData = $_POST;
  //echo "test - postData = $postData";
  $email = $_POST['email'];
  $name = $_POST['name'];
  $submittercall = $_POST['submittercall'];
  $callsign = $_POST['callsign'];
  $category = $_POST['category'];
  $location = $_POST['location'];
  $message = $_POST['message'];
  echo "<h2>MOQP Log Submission Summary</h2>";
  echo "Name: $name<br>Submitter's Call Sign:$submittercall<br>e-mail: $email<br>MOQP Call Sign: $callsign<br>  ";
  echo "Category: $category<br>Location: $location<br>Note/Message: $message<br>";

  // Check CAPTCHA response
  if ($response == null || !$response->success) {
         $statusMsg='Please check the Im not a robot box';
  }else{
    
    // Check whether submitted data is not empty
    if(!empty($email) && !empty($name) && 
       !empty($submittercall) && !empty($callsign) &&
       !empty($category) && !empty($location) &&
       !empty($_FILES["attachment"]["name"])){
        
        // Validate email
        if(filter_var($email, FILTER_VALIDATE_EMAIL) === false){
            $statusMsg = 'Please enter your valid email.';
        }else{
            $uploadStatus = 1;
            
            // Upload attachment file
            if(!empty($_FILES["attachment"]["name"])){
                
                // File path config
                $targetDir = "/tmp/";
                $fileName = basename($_FILES["attachment"]["name"]);
                $targetFilePath = $targetDir . $fileName;
                $fileType = pathinfo($targetFilePath,PATHINFO_EXTENSION);
                $fileType = strtolower($fileType);
                //echo $targetFilePath;
                
                // Allow certain file formats
                $allowTypes = array("log","txt","csv","xls","xlsx","pdf","cbr","cab");
                $txtTypes = array("log","txt","csv","cbr","cab");
                //echo "filetype = $fileType";
                if(in_array($fileType, $allowTypes)){
                    // Upload file to the server
                    if(move_uploaded_file($_FILES["attachment"]["tmp_name"], $targetFilePath)){
                        $uploadedFile = $targetFilePath;
                        $uploadStatus = 1;

                    }else{
                        $uploadStatus = 0;
                        $statusMsg = "Sorry, there was an error uploading your file.";
                    }
                }else{
                    $uploadStatus = 0;
                    $statusMsg = "Sorry, only files of type $allowTypes are allowed to be upload.";
                }
            }
            
            if($uploadStatus == 1){
                
                // Recipient
                $toEmail = 'moqsoparty@w0ma.org';

                // Sender
                //$from = 'n0so@w0ma.org';
                //$fromName = 'MOQP Web Log';
                $from = $email;
                $fromName = $name;
                
                // Subject
                $emailSubject = 'MOQP WEB '.strtoupper($callsign);
                
                // Message 
                $htmlContent = "<h2>MOQP Log Received via Web</h2>".
                    "<p>Name: $name, $submittercall<br>".
                    "e-mail: $email<br>MOQP Call Sign Used: $callsign<br>".
                    "Category: $category<br>Location: $location<br></p>".
                    "<p>Uploaded filename: $fileName</p>".
                    "<p>Note/Message: $message</p>".
                    "<p>This data received via the MOQP Web Form.</p>";
                    
                
                // Header for sender info
                $headers = "From: $fromName"." <".$from.">";

                if(!empty($uploadedFile) && file_exists($uploadedFile)){
                    
                    // Boundary 
                    $semi_rand = md5(time()); 
                    $mime_boundary = "==Multipart_Boundary_x{$semi_rand}x"; 
                    
                    // Headers for attachment 
                    $headers .= "\nMIME-Version: 1.0\n" . "Content-Type: multipart/mixed;\n" . " boundary=\"{$mime_boundary}\""; 
                    // Multipart boundary 
                    $message = "--{$mime_boundary}\n" . "Content-Type: text/html; charset=\"UTF-8\"\n" .
                    "Content-Transfer-Encoding: 7bit\n\n" . $htmlContent . "\n\n"; 
                    
                    // Preparing attachment
                    if(is_file($uploadedFile)){
                        $message .= "--{$mime_boundary}\n";
                        $fp =    @fopen($uploadedFile,"rb");
                        $data =  @fread($fp,filesize($uploadedFile));
                        @fclose($fp);
                        $data = chunk_split(base64_encode($data));
                        $newfilename = strtoupper($callsign.".".$fileType);
                        $message .= "Content-Type: application/octet-stream; name=\"".$newfilename."\"\n" . 
                        "Content-Description: ".$newfilename."\n" .
                        "Content-Disposition: attachment;\n" . " filename=\"".$newfilename."\"; size=".filesize($uploadedFile).";\n" . 
                        "Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
                    }
                    
                    //echo "<br>data= " .$data; 
                    //exec("python pytest.py $data",$my_output);
                    //var_dump($my_output);
                    //echo "php printing ... $my_output";
                    
                    $message .= "--{$mime_boundary}--";
                    $returnpath = "-f" . $email;
                    
                    // Send email
                    $mail = mail($toEmail, $emailSubject, $message, $headers, $returnpath);
                    
                    // Delete attachment file from the server
                    @unlink($uploadedFile);
                }else{
                     // Set content-type header for sending HTML email
                    $headers .= "\r\n". "MIME-Version: 1.0";
                    $headers .= "\r\n". "Content-type:text/html;charset=UTF-8";
                    
                    // Send email
                    $mail = mail($toEmail, $emailSubject, $htmlContent, $headers); 
                }
                // If mail sent
                if($mail){
                    echo '<h3>Your log has been submitted successfully.</h3>';
                    echo '<p>Please CLOSE this browser window when you are ready.</p>';
                    exit();
                    //$statusMsg = 'Your log has been submitted successfully !';
                    //$msgClass = 'succdiv';
                    
                    //$postData = '';
                }else{
                    $statusMsg = 'Your log submission failed, please try again.';
                }
            }
        }
    }else{
        $statusMsg = 'Please fill all the fields.';
    }
  }
}
?>


<!-- Display submission status -->
<?php if(!empty($statusMsg)){ ?>
         <p class="statusMsg <?php echo !empty($msgClass)?$msgClass:''; ?>"><?php echo $statusMsg; ?></p>
    <?php } ?>

<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
  <title><?php echo $year;?> Missouri QSO Party Log Submission Form</title>
  <script src='https://www.google.com/recaptcha/api.js'></script>
</head>
<body bgcolor="#E6E6FA">
<h3 align='center'><?php echo $year;?> Missouri QSO Party Log Submission Form</h3>
<p style="text-align: center;"><?php echo "from database $dbname";?></p>
<hr>

<!-- Display contact form -->
<form method="post" action="" enctype="multipart/form-data">
  <fieldset>
    <br>
    <legend>Missouri QSO Party Log File Upload</legend>
    <div class="form-group">
        <label>Submitter's Name: </label>
           <input type="text" name="name" class="form-control" value="<?php echo !empty($postData['name'])?$postData['name']:''; ?>" placeholder="NAME" required="">
        </label>
    </div>
    <br>
    <div class="form-group">
        <label>Submitter's e-mail Address: 
        <input type="email" name="email" class="form-control" value="<?php echo !empty($postData['email'])?$postData['email']:''; ?>" placeholder="EMAIL ADDRESS" required="">
        </label>
    </div>
    <br>
    <div class="form-group">
      <label>Submitter's Call Sign: 
        <input type="text" name="submittercall" class="form-control" value="<?php echo !empty($postData['submittercall'])?$postData['submittercall']:''; ?>" placeholder="YOUR CALL SIGN" required="" style="text-transform:uppercase">
      </label>
    </div>
    <br>
    <div class="form-group">
      <label>Call Sign Used During MOQP: 
        <input type="text" name="callsign" class="form-control" value="<?php echo !empty($postData['callsign'])?$postData['callsign']:''; ?>" placeholder="MOQP CALL SIGN" required="" style="text-transform:uppercase">
      </label>
    </div>
    <br>

   <?php
   // Create connection and read LOCATION, CONTESTCATEGORIES tables
   $conn = new mysqli($hostname, $username, $password, $dbname);
   // Check connection
   if ($conn->connect_error) {
     die("Connection failed: " . $conn->connect_error);
   }

   $sql = "SELECT * FROM CONTESTCATEGORIES";
   $sql2 = "SELECT * FROM LOCATIONS";
   $result = $conn->query($sql);
   $resultL = $conn->query($sql2);
   if (($result->num_rows > 0) and ($resultL->num_rows >0)) {
     // Build option select lists
     echo "<div class='form-group'>";
     echo "<label>Select your Location for the MOQP<br>(US State, Canada Province or DX): </label>";
     echo "<select id='location' name='location' class='form-control'>";
     if (!empty($postData['location']))
        echo "<option value=".$postData['location'].">".$postData['location']."</option>";
     else
        echo "<option></option>";
     while($row = $resultL->fetch_assoc()) {
       echo "<option value='" . $row["ABREV"]. "'>". $row["ABREV"]. " - " .$row["NAME"]. " - ". $row["COMMENT"]. "</option>";
     }
     echo "</select><br>";
     echo "</div>";
     echo "<br>";
     echo '<div class="form-group">';
     echo "Select your MOQP category: ";
     echo "<select id='category' name='category' class='form-control'>";
     //echo "<option value='Select Category'>Category</option>";
     if (!empty($postData['category'])) {
         echo "<option>".$postData['category']."</option>";
     }
     else {
         echo "<option></option>";
     }
     while($row = $result->fetch_assoc()) {
       echo "<p><option value='" . $row["NAME"]. "'>". $row["NAME"]. " - ". $row["DESCRIPTION"]. "</option>";
     }
     echo "</select>";
     echo "</div>";
   } else {
     echo "0 results";
   }
   $conn->close();
   ?>

   <div class="form-group">
      <br><label>Enter Optional Message or Notes: 
        <textarea name="message" class="form-control" placeholder="Write your optional message here" ><?php echo !empty($postData['message'])?$postData['message']:''; ?></textarea>
      </label>
    </div>
    <br>
    <div class="form-group">
      <label>Browse For Log File: 
        <input type="file" name="attachment" class="form-control" required="this is a required field">
      </label>
    </div>
    <div class="submit">
        <input type="submit" name="submit" class="btn" value="SUBMIT">
    </div>
    <br>
  </fieldset>
    <div class="g-recaptcha" data-sitekey="6LeRFlUUAAAAAInDgk2fFgi_LqaToqoT3HfCdqfs">
    </div>

</form>

<hr/>
<table border="0" cellpadding="1" cellspacing="1" style="width: 500px;" align = "center">
	<tbody>
		<tr>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php">W&Oslash;MA Home</a></td>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php/missouri-qso-party">MOQP Home</a></td>
			<td style="text-align: center;"><a href="http://w0ma.org/index.php/9-moqp/26-submitting-your-log-for-the-missouri-qso-party">MOQP Log Submission</a></td>
		</tr>
	</tbody>
</table>
<script src='https://www.google.com/recaptcha/api.js'></script>
</body>
</html>

<?php
function readLog($targetFilePath, $fileType, $txtTypes) {
   if(in_array($fileType, $txtTypes)){
     //echo "reading file $targetFilePath<br>";
     $fdat=readfile($targetFilePath);
     //echo $fdat;
  }
  //echo "FileType = $fileType<br>";
  //echo "txtTypes= ";
  //var_dump($txtTypes);
  return $fdat;
} ?>  


