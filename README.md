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
3. You can see options for each utility by entering:<br/>
   ./utility-name --help. Example:<br/>
    python ./mqpcategory --help<br/>
    usage: mqpcategory [-h] [-v] [-c CALLSIGN] [-d DIGITAL] [-U VHF] [-i INPUTPATH]<br/>
    moqpcategory - Determine which Missouri QSO Party Award category a Cabrillo Format log file is in. Based on 2019 MOQP rules<br/>
    optional arguments:<br/>
             -h, --help            show this help message and exit<br/>
             -v, --version         show program's version number and exit<br/>
             -c CALLSIGN, --callsign CALLSIGN<br/>
              CALLSIGN in MOQP database to summarize. Entering allcalls = all calls in database<br/>
             -d DIGITAL, --digital DIGITAL<br/>
             Summarize digital QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in
             database<br/>
             -U VHF, --vhf VHF     Summarize VHF QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in
                                   database<br/>
             -i INPUTPATH, --inputpath INPUTPATH<br/>
              Specifies the path to the folder that contains the log files to summarize. <br/>     
  
         
SCORING THE QSO PARTY, STEP-BY-STEP.
1. Install the utilities as described above.
2. Setup a new MySQL database to hold your data. We recommend using phpMyAdmin
   and importing the sample database.
3. Open a terminal window in the moqputils folder.
4. Note where the raw CABRILLO format log files reside. Logs MUST BE in CABRILLO format.
5. You can pre-check each logfile for errors by running:<br/>
   python ./mqpcategory -i path-to-log-file<br/>
   This will check the logfile without loading it into the database and show you
   a report in CSV format, which you can load into a spreadsheet like MSExcel.<br/>
   example:<br/>
           python ./mqpcategory -i /home/data/moqploags/W0MA.LOG<br/>
       this will evaluate only the single log file W0MA.LOG. Entering the following 
       will perform the summary in ALL .LOG files in the folder:<br/>
           python ./mqpcategory -i /home/data/moqploags/<br/>
       the ending slash is important!
       
   Review this output for errors - you may want to consider rejecting
   logs that have excessive errors and ask the submitters to correct
   the errors, or edit the files yourself to correct minor defects.
       
   If you choose to edit the logs, it is recommended that you preserve the
   original log as submitted for history, and perform edits on a copy of
   the log in another folder.
   Things to look for include:
   - CABRILLO HEADER info. Especially the LOCATION: and all CATEGORY-XXXX: tags. 
             This information is what will determine which MOQP category the
             station fits into. Many operators edit the fields and change the data to non-
             standard values. For the QSO Party, all stations should make LOCATION: their 
             STATE, PROVINCE or DX. The mqpcategory utility will flag fields it recognizes 
             as incorrect or incomplete in most cases. It's worth a reply e-mail to the 
             submitter to get this info clarified or corrected. 
             
   - QSO: Exchanges need to be in the format:<br/>
                 QSO: frequency-in-KHz MODE DATE TIME MYCALL MYRST MYQTH URCALL URRST URQTH<br/>
             Example of W0MA PHONE QSO with N0H:<br/>
                 QSO: 3900 PH 2019-04-07 1451 W0MA 59 MO N0H 59 IRN<br/>
          
   - QSO DATE/TIMES - The utility will flag QSOs that are not withing the 
             contest period. If there are lots of them, you should question if the station 
             time was off. If it's off more than 30 minutes, many QSOs may be considered 
             invalid by the qsochecker.
             
   - QSO FREQUENCY in KHz - Many stations will entry the frequency in MHz (3.5, 4, 
             7, 14, 21, etc.) - CABRILLO format expects frequency in KHz (3500, 4000, 7000, etc.).
             
   - For MISSOURI stations, the MYQTH/URQTH in the exchange field should be a 3 character
             county name, NOT MO or MISSOURI!
             
   - SIGNAL REPORTS - must be the standard RST format, not db numbers from FT8 QSOs!
          
   - EXTRA DATA COLUMNS IN THE QSO: LINES - Some older logging programs include a
             a SEQUENCE or SERIAL NUMBER as part of the exchange. This is no longer required
             and they need to be removed before scoring. Some logging programs include 
             station fields for multi-transmitter stations. These may need to be removed 
             before scoring unless they are at the end of the line.
             
   - DUPES REMOVED - Most modern logging programs do this. If not, the QSOCHECKER will 
             flag the older of two QSOs that are DUPES as INVALID.
    
6. Once Step #5 is completed and the logfile edited accordingly, it is recommended that the 
       edited log be moved to a different folder, and that the original be preserved for history.
       
7. Load the logfiles into the database:<br/>
           python ./loadlogs -i /home/data/moqplogs/ready-to-load/W0MA.LOG  <br/>
       This will load a single logfile into the database. Entering:<br/>
           python ./loadlogs -i /home/data/moqplogs/ready-to-load/<br/>
       will attempt to load ALL logfiles in the folder /home/data/moqplogs/ready-to-load/<br/>
       
       NOTE: The loadlogs utility needs updating to allow for REPLACING logs in the database.
             currently, the utility will simply make a new db entry for the log if you load it a
             2nd time. This would show up as a station appearing multiple times (with many DUPElicate
             QSOS) in the contest reports later on, and these will need to be removed manually. You
             may use phpMyAdmin to remove duplicate logs, but it's a bit painfull. A utility to help
             manage this probably should be on the TODO list.
       
8. Getting the raw log files in prepped to initiallly load is probably the most time consuming task. 
       It can (and probably should) be done as the logs trickle in at the end of the contest. That way 
       when the contest log submission closes, you are ready to score! Don't forget to save/archive the
       raw logs, just in case!
       
       After all logs and QSOs are loaded into the database, it might be a good idea to perform an export/
       backup of the database. Again, the phoMyAdmin tool can help with this. Save the exported file 
       somewhere, just in case.
       
9. Once all logs are loaded into the database, start running the QSO checker:<br/>
             python ./qsocheck -c W0MA<br/>
       runs the QSO check for all QSOs submitted by W0MA. A report will be printed showing progress,
       and a list of VALID qsos will be displayed, followd by a list of INVALID qsos.
       
       This needs to be done for all station callsigns. If you enter: python qsocheck -c allcalls
       The qsochecker will run for every callsign in the database, updating status for valid/invalid 
       QSOs.
       
       If you have stations with an excessive number of invalid QSOs, it would be wise to investigate 
       why, correct any issues, then run qsocheck again. It's always best to make the final run of qskcheck
       with -c allcalls. 
       
       Once this step is complete, you are now ready to start "scoring".
       
10. The database contains three summary tables:
    - SUMMARY - Holds a summary list of QSOs by mode, multiplier count (mults) W0MA Bonus, K0GQ Bonus,
                     CABFILE Bonus, total score, MOQPCATEGORY, DIGITAL, VHF and ROOKIE flags. 
                     
      - Running python ./mqpcategory -c CALLSIGN<br/>
        adds or updates info for the station CALLSIGN.
                     
      - Running python ./mqpcategory -c allcalls<br/>
        adds or updates this table for all stations
                     found in the database.
                  
      - Note that running ./mqpcategory -d CALLSIGN or allcalls <br/>
        produces a summary report of
                     DIGITAL qsos only, usefull for scoring the DIGITAL award. No updates to the SUMMARY
                     table.

      - Note that running ./mqpcategory -U CALLSIGN or allcalls <br/>
        produces a summary report of
                     VFH (and up) qsos only, usefull for scoring the VHF awards. No updates to the SUMMARY
                     table.
                     
      - Note that running ./mqpcategory -C or --county CALLSIGN or allcalls <br/>
        produces a summary 
                     report of MISSOURI COUNTIES worked, usefull for scoring the MOST COUNTIES WORKED awards. 
                     
    - SHOWME - Holds a summary list of all 1x1 stations worked by CALLSIGN for the SHOWME Award.
    - MISSOURI - Holds a summary list of all 1x1 stations worked by CALLSIGN for the MISSOURI Award.
                     
      - Running python ./mqpcertificates -c CALLSIGN or allcalls <br/>
        adds a station to, or updates
                     stations status in these two tables.
      - Note that entering: python ./mqpcertificates -i path-to-logfile<br/>
                     will run the utility on a log file or directory of logfiles.
                     
11. Step 10 was mostly descriptive, so here is an expample for after the database is loaded with all log files
       and the qsocheck has been run:
       
    - SCORE, SUMMARIZE AND STORE in SUMMARY Table and MOQP SCORES BY CATEGORY Report:<br/>
             python mqpcategory -c allcalls (optionally add >filename.csv to this line to capture report).
             This updates the SUMMARY table, and also produces a nice report in .CSV format that may be pulled
             into MSExcel for sorting, printing, reporting. You need to run this first to create / update the
             SUMMARY table. Some of the later reports rely on it.
             
    - MOQP SCORES BY CATEGORY Report:<br/>
             python mqpreports -c allcalls (optionally add >filename.csv to this line to capture report).
             Same report as mqpcategory -c but without updating the SUMMARY table. This one just reads and
             formats data from the table. As a TODO, it should also sort my MOQPCATEGORY and SCORE.
             
             This step will generate a BIG report. For the moment, the various category lists need to be
             generated manually from this report by pulling the report filename.csv into MSExcel and 
             splitting out by MOQP CATEGORY. Probably the most time consuming task (aside from getting the
             raw log files in shape to initiallly load).
             
    - MOQP SHOWME and MISSOURI Awards:<br/>
             python mqocertificates -c allcalls (optionally add >filename.csv to this line to capture report).
             This updates the SHOWME and MISSOURI tables, and produces a nice report in .CSV format that may 
             be pulled into MSExcel for sorting, printing, reporting. As a TODO, these should also get added 
             to mqpreports to only report the data without updating the tables.
             
    - MOQP DIGITAL ONLY Awards:<br/>
             python mqpcategory -d allcalls (optionally add >filename.csv to this line to capture report).
             This produces a report of the DIGITAL QSOs from the summary tabel, and also produces a nice report 
             in .CSV format that may be pulled into MSExcel for sorting, printing, reporting. No updates to the
             table, so you need to run with the -c option first. As a TODO, these should also get added 
             to mqpreports utility.
             
    - MOQP VHF ONLY Awards:<br/>
             python mqpcategory -U allcalls (optionally add >filename.csv to this line to capture report).
             This produces a report of the VHF and up only QSOs from the summary tabel, and also produces a nice 
             report in .CSV format that may be pulled into MSExcel for sorting, printing, reporting. No updates 
             to the table, so you need to run with the -c option first. As a TODO, these should also get added 
             to mqpreports utility.
             
   - MOQP CLUB Awards:<br/>
             python mqpreports -c club (optionally add >filename.csv to this line to capture report).
             This produces a summary report of the stations with something in the CLUB: tag of the logfile header.
             The list will be sorted by LOCATION, CLUB and SCORE. Also produces a nice report in .CSV format that 
             may be pulled into MSExcel for sorting, printing, reporting. At the moment, the user needs to 
             consolidate and summarize the clubs using the spreadsheet to determine winners.

   - MOQP MOST COUNTIES Award:<br/>
             python mqpcategory -C or --county allcalls (optionally add >filename.csv to this line to capture report).
             Generates a list of all stations showing the Missouri Counties worked.
             
  -  MOQP ROOKIE Award:<br/>
             Use the report generated by mqpreports -c allcalls >filename.txt.
             Load filename.txt into MSExcel (or equivalent) and sort on the ROOKIE field to generate the list of
             rookie entries with score. Eligibility for teh ROOKIE award must be done manually, and may take 
             communication with the operator to determine age, level of experience, etc.
       
 
V1.0.0 Initial release - 2018-04-13
