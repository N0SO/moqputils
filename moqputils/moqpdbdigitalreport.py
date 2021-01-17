#!/usr/bin/env python3
"""
moqpdbdigitalreport - Same features as moqpcategory -d, 
                  except read all data from an SQL database 
                  DIGITAL Summary table. 

                  Prerequisits:
                   1. All logs loaded into database with
                      mqplogcheck -l
                   2. QSO Validation completed on all logs
                      with qsocheck -c allcalls
                   3. mqpcategory completed:
                      mqpcategory -c allcalls
                      mqpcategory -U (or  --vhf)

                  These steps create the summary tables
                  SUMMARY and DIGITAL required by this code.
                
                  Added for the 2020 MOQP.
                  
Update History:
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

from moqpdbutils import *
from moqpdbconfig import *


VERSION = '0.0.1' 

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\t'+\
     'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t'+\
     'CABFILE BONUS\tSCORE\t'
                

class MOQPDBDigitalReport():
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
           csvdata += ('%s\t'%(log['W0MABONUS']))         
           csvdata += ('%s\t'%(log['K0GQBONUS']))         
           csvdata += ('%s\t'%(log['CABBONUS']))         
           csvdata += ('%s'%(log['SCORE']))         

       return csvdata

    def fetchDIGISummary(self, mydb, call='allcalls'):
        sumdata = None
        query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.LOCATION, LOGHEADER.CABBONUS, '+\
                'LOGHEADER.OPERATORS, DIGITAL.* '+\
                'FROM DIGITAL INNER JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=DIGITAL.LOGID '
        if (call != 'allcalls'):
            query += 'WHERE CALLSIGN=\'%s\' '%(call)
        else:
            query += 'ORDER BY LOGHEADER.LOCATION, DIGITAL.SCORE DESC'
        sumdata = mydb.read_query(query)
        return sumdata
        
    def ProcessData(self, call):
       ReportList = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       data = self.fetchDIGISummary(mydb, call)
       if (data):
           ReportList = []
           for ent in data:
               ReportList.append(self.exportcsvsumdata(ent))
       return ReportList

    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       csvList = self.ProcessData(callsign)
       if (csvList):
           print(COLUMNHEADERS)
           for line in csvList:
               print(line)

