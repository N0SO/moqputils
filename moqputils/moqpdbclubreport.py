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
"""

from moqpdbcatreport import *
from moqpdbconfig import *


VERSION = '0.0.1' 
"""
COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\tCLUB\t' + \
                'CW QSO\tPH QSO\tRY QSO\tQSO COUNT\tVHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\t' +\
                'DIGITAL\tVHF\tROOKIE\n'
"""
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
        thisclub=None
        #print(club)
        loglist = db.read_pquery(\
              "SELECT ID, CALLSIGN, OPERATORS, LOCATION "+\
              " FROM LOGHEADER WHERE CLUB=%s", [club])
        if (loglist):
            #print('\nClub: %s, log count = %d, data=%s'%(club, len(loglist),loglist))
            thisclub = dict()
            clubLogs = []
            thisScore = 0
            for station in loglist:
                thisStation = dict()
                score = db.read_pquery(\
                      "SELECT SCORE FROM SUMMARY WHERE LOGID=%s",
                      [station['ID']])
                thisScore += score[0]['SCORE']
                thisStation['CLUB']=club
                thisStation['SCORE']=score[0]['SCORE']   
                thisStation['CALL'] = station['CALLSIGN']
                thisStation['OPS'] = station['OPERATORS']
                thisStation['LOCATION'] = station['LOCATION']
                clubLogs.append(thisStation)
                #print(thisStation)
        thisclub['CLUB']=club
        thisclub['COUNT']=len(clubLogs)
        thisclub['SCORE']=thisScore
        thisclub['LOGS']=clubLogs
        return thisclub         

    def processAll(self, mydb):
        retlist = None
        clublist = mydb.read_query("SELECT DISTINCT CLUB FROM "+\
                                                     "LOGHEADER")
        #loglist = mydb.fetchLogList()
        #print(loglist)
        #print(len(loglist), loglist)
        if (clublist):
            retlist = []
            Headers = True
            for nextclub in clublist:
                if (nextclub['CLUB'] != ''):
                    thisclub=self.processOne(mydb, 
                               nextclub['CLUB'])
                    retlist.append(thisclub)
        else:
            print('No logs.')
        return retlist

    def printClubs(self, clubs):
        HEADERLINE = 'CLUB NAME\tSTATION CALL\tOPERATOR(S)\t'+\
                     'LOCATION\tSCORE'
        print(HEADERLINE)
        for club in clubs:
            if (club['COUNT'] >=3):
                print('%s Total:\t\t\t\t%d'%(club['CLUB'], 
                                            club['SCORE']))
            for station in club['LOGS']:
               stationcsv = self.exportcsvdata(station)
               print(stationcsv)



    def appMain(self, callsign):
       csvdata = ['No Data.']
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       clublist = self.processAll(mydb)
       if (clublist):
           self.printClubs(clublist)

