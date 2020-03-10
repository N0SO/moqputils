# moqputils
Collection of tools for processing Missouri QSO Party log files. 
The set has now grown from the single csv2cab utility to an entire
suite of utilities that was used to score the 2019 Missouri QSO 
Party. Expanded utilities include:

   csv2cab - The original CSV to CABRILLO utility. The BEARS-STL
             provide a spreadsheet template useful for logging 
             contacts during the Missouri QSO Party. The form 
             may be downloaded from our website: 
             http://w0ma.org/index.php/missouri-qso-party.
             It is also in this repository.
             This is the original utility that converts that
             Missouri QSO Party Excel logging form MOQP_log.xls 
             to a Cabrillo file ready for submission.
   
   loadlogs - Load logfiles into a MySQL database. Log headers 
              are read and recorded a table logheaders, then
              QSOs from the log are read into a QSOs table. 
              This will allow the additional utilities to do 
              things like validate QSOs and generate contest 
              wide stats.
              
   qsocheck - Check all QSOs in the MySQL database QSO table
              for validity. Also checks for a corrosponding QSO
              with the other station. The QOS will be marked
              VALID if all QSO checks pass, or the reason the
              qsochecker thinks it is invalid will be recoreded.
              Does the date/time match the defined contest period? 
              Is the band valid?
              is the mode valid? 
              Callsigns valid? 
              Signal report valid for mode?

   mqpcategory - Utilities to summarize and categorize a single 
                 log or set of logs using data from the database,
                 or directly from the logfiles. Database SUMMARY
                 table, bonus points and summary stats for the
                 station are updated if run on the database.
                 
   mqpcertificates - Utilities to score and summarize the list 
                     of those who qulaify for special certificates
                     such as SPELL SHOW ME and MISSURI. Database
                     SHOWME and MISSOURI tables are updated.

   mqpreports - Utilities to generate CSV reports for review, 
                processing, publishing.  These only use data
                from the database summary tables.
              
   mqplabels - Utilities to create CSV files that will contain
               PLACEMENT, AWARD NAME, STATION, OPERATORS, NAME,
               ADDRESS, EMAIL, etc. These may be used in a 
               spreadsheet to create First and Second Place 
               award, SHOWME, MISSOURI certificates and mailing/
               shipping lables.

This suite is python based, it will run on any platform that supports
python V3.x (currently using 3.6) and MySQL. It requires the python3
MySQL and requests libraries packages. These are probably already
installed in most Linux distrobutions. They should be available for
Windows 10 and MacOS. You can also install VirtualBox and run Linux
under Windows 10 or MacOS. The suite was developed on a Fedora Linux
system, version 30. But we have also had success running it under 
Windows 10 (with a Linux based MySQO database on the same LAN).

It's first application was scoring the 2019 Missouri QSO Party.

INSTALLATION:
    1. Install python3 and mySQL.
    2. Install (or verify) the python3 MySQL and REQUESTS 
       libraries are installed.
    3. Setup the mySQL database. The phpMyAdmin utility can be
       very usefule for this. There is a blank database in this
       repository that may be imported. We should write a script
       to set this up - That is on the TODO list.
       For now, set it up manually.
    4. Copy the entire source directory moqputils somewhere.
       You will run from this directory. Again, we should develop
       the python setup/install packages for the utilities, but we
       are not there yet. That is also on the TODO list.
USAGE:
    1. Some of the utilities have a GUI, but most do not. Even the
       GUIs that are available are not fully developed, so stick with
       the command line functions for now.
    2. Use the cd command to swithc into the moqputils directory in 
       a command window. You can run all of the utilities from there.
    3. You can see options for each utility by entering:
       ./utility-name --help. Example:
       python ./mqpcategory --help
       usage: mqpcategory [-h] [-v] [-c CALLSIGN] [-d DIGITAL] [-U VHF] [-i INPUTPATH]
       moqpcategory - Determine which Missouri QSO Party Award category a Cabrillo Format log file is in. Based on 2019 MOQP
       Rules
       optional arguments:
             -h, --help            show this help message and exit
             -v, --version         show program's version number and exit
             -c CALLSIGN, --callsign CALLSIGN
              CALLSIGN in MOQP database to summarize. Entering allcalls = all calls in database
             -d DIGITAL, --digital DIGITAL
             Summarize digital QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in
             database
             -U VHF, --vhf VHF     Summarize VHF QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in
                                   database
             -i INPUTPATH, --inputpath INPUTPATH
              Specifies the path to the folder that contains the log files to summarize.      
              
Scoring the QSO Party, step by step.
    1. Install the utilities as described above.
    2. Setup a new MySQL database to hold your data. We recommend using phpMyAdmin
       and importing the sample database.
    3. Open a terminal window in the moqputils folder.
    4. Note where the raw CABRILLO format log files reside. They MUST BE in CABRILLO format.
    5. You can pre-check logfiles for errors by running:
           python ./mqpcategory -i path-to-log-file
       This will check the logfile without loading it into the database and show you
       a report in CSV format, which you can load into a spreadsheet like MSExcel.
       example:
           python ./mqpcategory -i /home/data/moqploags/W0MA.LOG
       this will evaluate only the single log file.
           python ./mqpcategory -i /home/data/moqploags/W0MA.LOG
       entering the following will perform the summary in ALL .LOG files
       in the folder:
           python ./mqpcategory -i /home/data/moqploags/
       the ending slash is important!
       
       Review this output for errors - you may want to consider rejecting
       logs that have excessive errors and ask the submitters to correct
       the errors.
       
 ----- More to follow -----

V1.0.0 Initial release - 2018-04-13
