# moqputils
Collection of tools for processing Missouri QSO Party log files. This will replace the csv2cab repository.

csv2cab
Convert the Missouri QSO Party Excel logging form MOQP_log.xls 
to a Cabrillo file ready for submission.

The BEARS-STL provide a spreadsheet template useful for logging 
contacts during the Missouri QSO Party. The form may be downloaded
from our website: http://w0ma.org/index.php/missouri-qso-party.

This utility is python based, it will run on any platform that supports
python V2.7

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
