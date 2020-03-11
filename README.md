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
              
SCORING THE QSO PARTY, STEP-BY-STEP.
    1. Install the utilities as described above.
    2. Setup a new MySQL database to hold your data. We recommend using phpMyAdmin
       and importing the sample database.
    3. Open a terminal window in the moqputils folder.
    4. Note where the raw CABRILLO format log files reside. They MUST BE in CABRILLO format.
    5. You can pre-check each logfile for errors by running:
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
       the errors, or edit the files yourself to correct minor defects.
       
       If you choose to edit the logs, it is recommended that you preserve the
       original log as submitted for history, and perform edits on a copy of
       the log in another folder.
       Things to look for include:
          A. CABRILLO HEADER info. Especially the LOCATION: and all CATEGORY-XXXX: tags. 
             This information is what will determine which MOQP category the
             station fits into. Many operators edit the fields and change the data to non-
             standard values. For the QSO Party, all stations should make LOCATION: their 
             STATE, PROVINCE or DX. The mqpcategory utility will flag fields it recognizes 
             as incorrect or incomplete in most cases. It's worth a reply e-mail to the 
             submitter to get this info clarified or corrected. 
             
          B. QSO: Exchanges need to be in the format:
                 QSO: frequency-in-KHz MODE DATE TIME MYCALL MYRST MYQTH URCALL URRST URQTH
             Example of W0MA PHONE QSO with N0H:
                 QSO: 3900 PH 2019-04-07 1451 W0MA 59 MO N0H 59 IRN
          
          C. QSO DATE/TIME Stamps - The utility will flag QSOs that are not withing the 
             contest period. If there are lots of them, you should question if the station 
             time was off. If it's off more than 30 minutes, many QSOs may be considered 
             invalid by the qskchecker.
             
          D. QSO FREQUENCY in KHz - Many stations will entry the frequency in MHz (3.5, 4, 
             7, 14, 21, etc.) - CABRILLO format expects frequency in KHz (3500, 4000, 7000, etc.).
             
          E. For MISSOURI stations, the MYQTH/URQTH in the exchange field should be a 3 character
             county name, NOT MO or MISSOURI!
             
          F. SIGNAL REPORTS - must be the standard RST format, not db numbers from FT8 QSOs!
          
          G. EXTRA DATA COLUMNS IN THE QSO: LINES - Some older logging programs include a
             a SEQUENCE or SERIAL NUMBER as part of the exchange. This is no longer required
             and they need to be removed before scoring. Some logging programs include 
             station fields for multi-transmitter stations. These may need to be removed 
             before scoring unless they are at the end of the line.
             
          H. DUPES REMOVED - Most modern logging programs do this. If not, the QSOCHECKER will 
             flag the older of two QSOs that are DUPES as INVALID.
    
    6. Once Step #5 is completed and the logfile edited accordingly, it is recommended that the 
       edited log be moved to a different folder, and that the original be preserved for history.
       
    7. Load the logfiles into the database:
           python ./loadlogs -i /home/data/moqplogs/ready-to-load/W0MA.LOG  
       This will load a single logfile into the database. Entering:
           python ./loadlogs -i /home/data/moqplogs/ready-to-load/
       will attempt to load ALL logfiles in the folder /home/data/moqplogs/ready-to-load/
       
       NOTE: The loadlogs utility needs updating to allow for REPLACING logs in the database.
             currently, the utility will simply make a new db entry for the log if you load it a
             2nd time. This would show up as a station appearing multiple times (with many DUPElicate
             QSOS) in the contest reports later on, and these will need to be removed manually. You
             may use phpMyAdmin to remove duplicate logs, but it's a bit painfull. A utility to help
             manage this probably should be on the TODO list.
       
    8. Run the QSO checker:
    
             
 ----- More to follow -----

V1.0.0 Initial release - 2018-04-13
