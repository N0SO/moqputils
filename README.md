# moqputils
Collection of tools for processing Missouri QSO Party log files. 
The set has now grown from the single csv2cab utility to an entire
suite of utilities that was used to score the 2019 Missouri QSO 
Party. Expanded utilities include:
   csv2cab - The original CSV to CABRILLO utility.
   
   loadlogs - Load logfiles into a MySQL database. Log headers 
              are read and recorded in a table, then QSOs from
              the log are read into a QSOs table. This will 
              qllow additional utilities to do things like 
              validate QSOs and generate contest wide stats.
              
   qsocheck - Check all QSOs in the MySQL database QSO table
              for validity. Also checks for corrosponding QSO
              with the other station. The QOS will be marked
              VALID if all QSO checks pass, or the reason the
              qsochecker thinks i't invalid will be recoreded.
              Does the date/time match the
              defined contest period? Is the band valid?
              is the mode valid? Callsigns valid? signal
              report valid for mode?

   mqpcategory - Utilities to summarize and categorize a single 
                 log or set of logs.
              


This suite is python based, it will run on any platform that supports
python V3.x (currently using 3.6). 

csv2cab
The BEARS-STL provide a spreadsheet template useful for logging 
contacts during the Missouri QSO Party. The form may be downloaded
from our website: http://w0ma.org/index.php/missouri-qso-party.
This is the original utility that converts the Missouri QSO Party 
Excel logging form MOQP_log.xls to a Cabrillo file ready for submission.




To use this utility:
1. Download the spreadsheet form from the link above.
2. Fill out the info needed in the top part of the form. 
3. Enter your contacts, one per line, into the form lines that start with QSO:
4. After all contacts have been entered, SAVE the form as a .xls file (for your records)
5. SAVE the file a 2nd time as a .CSV file.
6. Enter: python csv2cab.py logfilename.csv  NOTE: the file name will be the file you saved in step #5.
7. The resulting file will be named logfilename.csv.log.
8. We recommend you rename (or copy) the file to end in .LOG only.
9. Submit the resulting file as described here: http://w0ma.org/index.php/information/submitting-your-log

V1.0.0 Initial release - 2018-04-13
