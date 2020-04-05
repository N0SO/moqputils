# moqputils
Collection of tools for processing Missouri QSO Party log files. 
The set has now grown from the single csv2cab utility to an entire
suite of utilities that was used to score the 2019 Missouri QSO 
Party. Expanded utilities include:
1. csv2cab- The original CSV to CABRILLO utility. 
   - The BEARS-STL provide a spreadsheet template useful for logging 
     contacts during the Missouri QSO Party. The form may be 
     downloaded from our website: http://w0ma.org/index.php/missouri-qso-party.
     It is also in this repository. This is the original utility that 
     converts that Missouri QSO Party Excel logging form MOQP_log.xls 
     to a Cabrillo file ready for submission.
   
2. loadlogs - Load logfiles into a MySQL database. 
   - The Log header is read and recorded a table logheaders, then
     QSOs from the log are read into a QSOs table. 
     This will allow the additional utilities to do 
     things like validate QSOs and generate contest 
     wide stats.
              
3. qsocheck - Check all QSOs in the MySQL database QSO table
              for validity. 
   - Also checks for a corrosponding QSO with the other station. 
     The QOS will be marked VALID if all QSO checks pass, or the 
     reason the qsochecker thinks it is invalid will be recoreded.
     Does the date/time match the defined contest period? 
     Is the band valid?
     Is the mode valid? 
     Callsigns valid? 
     Signal report valid for mode?

4. mqpcategory - Utilities to summarize and categorize logs.
   - A single log or set of logs using data from the database,
    or directly from the logfiles. Database SUMMARY
    table, bonus points and summary stats for the
    station are updated if run on the database.
                 
5. mqpcertificates - Utilities to score SHOWME / MISSOURI awards. 
   - Build the database SHOWME and MISSOURI award tables. Al list
     of those who qulaify for special certificates SPELL SHOW ME and 
     MISSOURI. Database SHOWME and MISSOURI tables are updated.

6. mqpreports - Utilities to generate CSV reports.
   - For review, processing, publishing.  These only use data
     from the database summary tables.
              
7. mqplabels - Utilities to create CSV files for labels and awards.
   - Reports that will contain PLACEMENT, AWARD NAME, STATION, 
     OPERATORS, NAME, ADDRESS, EMAIL, etc. These may be used in a 
     spreadsheet to create First and Second Place award, SHOWME,
     MISSOURI certificates and mailing/ shipping lables.

This suite is python based, it will run on any platform that supports
python V3.x (currently using 3.6) and MySQL. It requires the python3
MySQL and requests libraries packages. These are probably already
installed in most Linux distrobutions. They should be available for
Windows 10 and MacOS. You can also install VirtualBox and run Linux
under Windows 10 or MacOS. The suite was developed on a Fedora Linux
system, version 30. But we have also had success running it under 
Windows 10 (with a Linux based MySQO database on the same LAN).

It's first application was scoring the 2019 Missouri QSO Party.

See the INSTALLATION and USAGE Guide in the shared/docs folder
for information regarding setup and use of the utilities.

       
 
V1.0.0 Initial release - 2018-04-13
