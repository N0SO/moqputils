#!/usr/bin/env python3
"""
moqpdbclubreport - Fetches a list of logs that have something
                   other than NULL in the Cabrillo Header field
                   CLUB. The log SUMMARY table entries for the
                   corrosponding logs is fetched and displayed
                   in the same format as MOQPDBCatReport, with
                   the CLUB field added. The result is output
                   in .csv format for further refinement in a
                   spreadsheet program such as Excel or
                   libreoffice.

                   Inherits from MOQPDBCatReport

                   Based on 2019 MOQP Rules.
                  
Update History:
* Fri Jan 31 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Sun May 31 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 -Added CLUBS and CLUB_MEMBERS DB Tables
- and reworked code to let SQL do the sorting work.
* Sat Dec 10 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Updates to use new devmodpath code.
"""

from moqputils.moqpdbcatreport import *
from moqputils.configs.moqpdbconfig import *


VERSION = '0.1.0' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tCLUB\tSCORE\n'

class MOQPDBClubReport(MOQPDBCatReport):
           
    def exportcsvdata(self, log):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
       """
       csvdata = None

       if (log):
       
           csvdata = ''
           csvdata += ('%s\t'%(log['CLUB']))
           csvdata += ('%s\t'%(log['CALL']))
           csvdata += ('%s\t'%(log['OPS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['SCORE']))         

       else:
          csvdata = ('No log data in database for .'%callsign)
       return csvdata

    def processOne(self, db, club):
        loglist = db.read_pquery(\
              "SELECT LOGHEADER.ID, SUMMARY.SCORE "+\
              "FROM LOGHEADER INNER JOIN SUMMARY ON "+\
              "LOGHEADER.ID=SUMMARY.LOGID WHERE CLUB=%s "+\
              "ORDER BY SUMMARY.SCORE", [club])

        logcount = len(loglist)
        if (logcount >= 3):
            #print('\nClub: %s, log count = %d, data=%s'%(club, len(loglist),loglist))
            thisScore = 0
            for station in loglist:
                thisScore += station['SCORE'] # Sum club member scores
            # Create club entry
            clubid = db.write_pquery(\
               'INSERT INTO CLUBS '+\
               '(NAME, LOGCOUNT, SCORE) '+\
               'VALUES (%s, %s, %s)',
               [club, logcount, thisScore])
            # Create club member entries
            for station in loglist:
                memberid = db.write_pquery(\
                   'INSERT INTO CLUB_MEMBERS '+\
                   '(CLUBID, LOGID) '+\
                   'VALUES(%s, %s)',
                   [clubid, station['ID']])

    def processAll(self, mydb):
        dquery ='DROP TABLE IF EXISTS CLUB_MEMBERS, CLUBS;'
        query1 = 'CREATE TABLE CLUBS ('+\
          'CLUBID int NOT NULL AUTO_INCREMENT, '+\
          'NAME varchar(255) NOT NULL, '+\
          'LOGCOUNT int NULL, '+\
          'SCORE int NULL, '+\
          'PRIMARY KEY (CLUBID));'
        query2 = 'CREATE TABLE CLUB_MEMBERS ('+\
          'ID int NOT NULL AUTO_INCREMENT, '+\
          'CLUBID int NULL, '+\
          'LOGID int NULL, '+\
          'PRIMARY KEY (ID));'

        clublist = mydb.read_query("SELECT DISTINCT CLUB FROM "+\
                                   "LOGHEADER ORDER BY CLUB")
        if (clublist):
            result = mydb.read_query("SHOW TABLES LIKE 'CLUBS'")
            if (len(result) > 0):
                mydb.write_query(dquery) # Delete old club tables
            mydb.write_query(query1) #and create new, empty tables
            mydb.write_query(query2)
            retlist = []
            Headers = True
            for nextclub in clublist:
                if (nextclub['CLUB'] != ''):
                    self.processOne(mydb, 
                               nextclub['CLUB'])
        else:
            print('No logs.')

    
    def printClubsDB(self, db):
        queryL = 'SELECT * FROM CLUBS WHERE 1 ORDER BY SCORE DESC'
        query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.LOCATION, LOGHEADER.OPERATORS, '+\
                'CLUB_MEMBERS.* '+\
                'FROM CLUB_MEMBERS INNER JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=CLUB_MEMBERS.LOGID '
        clubList = db.read_query(queryL)
        printText = []
        print('CLUB\tCALL\tOPERATORS\tLOCATION\t'+\
              'OP SCORE\tLOG COUNT\tSCORE')
        for club in clubList:
            #print(club)
            stationList = db.read_query(\
               'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
               'LOGHEADER.LOCATION, LOGHEADER.OPERATORS, '+\
               'CLUB_MEMBERS.*, SUMMARY.SCORE '+\
               'FROM CLUB_MEMBERS INNER JOIN LOGHEADER ON '+\
               'LOGHEADER.ID=CLUB_MEMBERS.LOGID '+\
               'INNER JOIN SUMMARY ON SUMMARY.LOGID=LOGHEADER.ID'+\
               ' WHERE '+\
               'CLUB_MEMBERS.CLUBID='+('%s'%(club['CLUBID']))+\
               ' ORDER BY SCORE DESC')
            #print(stationList)
            print('%s\t\t\t\t\t%s\t%s'%(club['NAME'], 
                                    club['LOGCOUNT'],
                                    club['SCORE']))
            for station in stationList:
                print('\t%s\t%s\t%s\t%s'%\
                                 (station['CALLSIGN'],
                                  station['OPERATORS'],
                                  station['LOCATION'],
                                  station['SCORE']))
                    
    def appMain(self, callsign):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       result = mydb.read_query("SHOW TABLES LIKE 'CLUBS'")
       if (len(result) == 0):
           callsign = 'club-update'
       if (callsign == 'club-update'):
           print(\
            'Updating club database before generating report...')
           self.processAll(mydb)
       self.printClubsDB(mydb)

