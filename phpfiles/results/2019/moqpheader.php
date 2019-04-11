<?php

function draw_moqpheader($imagepath, $htmlpath) {

   print "<table align='center' border='0' cellpadding='1' cellspacing='1'>";
   print '<tbody>';
   print '<tr>';
   print "<td><a href='http://w0ma.org/index.php/missouri-qso-party/18-moqp/moqp-history/moqp-2018-history/61-2018-planned-activations'>
             <img align='middle' alt='Map' src='".$imagepath."moqp_icon.png'>Active Counties (Map)</a></td>";
   print '<td><a href="activecountiestabular.php"><img align="middle" alt="MOQP Home" src="'.$imagepath.'moqp_icon.png"> Active Counties (tabular)</a></td>';
   print '</tr>';
   print '<tr>';
   print '<td><a href="http://w0ma.org/mo_qso_party/"><img align="middle" alt="MOQP Home" src="'.$imagepath.'moqp_icon.png"> Back to MOQP Home</a></td>';
   print '<td><a href="http://w0ma.org/"><img align="middle" alt="BEARS Home" src="'.$imagepath.'moqp_icon.png"> BEARS Home</a></td>';
   print '</tr>';
   print '</tbody>';
   print '</table>';
}
?>