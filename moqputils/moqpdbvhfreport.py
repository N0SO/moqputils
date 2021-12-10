#!/usr/bin/env python3
"""
moqpdbvhfreport - Same features as moqpcategory, except read
                  all data from an SQL database VHF Summary
                  table.

                  Prerequisits:
                   1. All logs loaded into database with
                      mqplogcheck -l
                   2. QSO Validation completed on all logs
                      with qsocheck -c allcalls
                   3. mqpcategory completed:
                      mqpcategory -c allcalls
                      mqpcategory -U (or  --vhf)

                  These steps create the summary tables
                  SUMMARY and VHF required by this code.

                  Added for the 2020 MOQP.

Update History:
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Thu Dec 09 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Refactored for efficiency.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *


VERSION = '0.1.0'

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\tSCORE\t'+\
     'QSOs\tCW QSOs\tPH QSOs\tRY QSOs\tMULTS\t'+\
     'CABFILE BONUS\tW0MA BONUS\tK0GQ BONUS'


class MOQPDBVhfReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsvsumdata(self, log):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
       """
       csvdata= None

       if (log):
           csvdata = ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%d\t'%(log['QSOS']))
           csvdata += ('%s\t'%(log['MULTS']))
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += ('%s\t'%(log['W0MABONUS']))
           csvdata += ('%s\t'%(log['K0GQBONUS']))
           csvdata += ('%s'%(log['CABBONUS']))

       return csvdata

    def fetchVHFSummary(self, mydb, call='allcalls'):
        sumdata = None
        query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.LOCATION, LOGHEADER.CABBONUS, '+\
                'LOGHEADER.OPERATORS, VHF.* '+\
                'FROM VHF INNER JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=VHF.LOGID '
        if (call != 'allcalls'):
            query += 'WHERE CALLSIGN=\'%s\' '%(call)
        else:
            query += 'ORDER BY LOGHEADER.LOCATION, VHF.SCORE DESC'
        sumdata = mydb.read_query(query)
        return sumdata
    def ProcessData(self, call):
       ReportList = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       data = self.fetchVHFSummary(mydb, call)
       if (data):
           ReportList = []
           for ent in data:
               ReportList.append(self.exportcsvsumdata(ent))
       return ReportList
    """
    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       csvList = self.ProcessData(callsign)
       if (csvList):
           print(COLUMNHEADERS)
           for line in csvList:
               print(line)
    """
    def showData(self, log):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
       """
       csvdata= None

       if (log):
           csvdata = ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += ('%d\t'%(log['QSOS']))
           csvdata += ('%d\t'%(log['CWQSO']))
           csvdata += ('%d\t'%(log['PHQSO']))
           csvdata += ('%d\t'%(log['RYQSO']))
           csvdata += ('%s\t'%(log['MULTS']))
           csvdata += ('%s\t'%(log['CABBONUS']))
           csvdata += ('%s\t'%(log['W0MABONUS']))
           csvdata += ('%s'%(log['K0GQBONUS']))
       return csvdata



    def appMain(self, callsign):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.OPERATORS, LOGHEADER.LOCATION, ' +\
                'VHF.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM VHF JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=VHF.LOGID '+\
                'JOIN SUMMARY ON VHF.LOGID = SUMMARY.LOGID '+\
                'ORDER BY SCORE DESC'

       digList = mydb.read_query(query)

       print(COLUMNHEADERS)
       for ent in digList:
           print(self.showData(ent))
       #print(digList,len(digList))
