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
                      mqpcategory -d

                  These steps create the summary tables
                  SUMMARY and DIGITAL required by this code.

                  Added for the 2020 MOQP.

Update History:
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs
* Thu Dec 09 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Refactored for efficiency.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *


VERSION = '0.1.0'

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\t'+\
     'SCORE\tQSOS\tMULTS\t'+\
     'CABFILE BONUS\tW0MA BONUS\tK0GQ BONUS\t'


class MOQPDBDigitalReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

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
                'DIGITAL.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM DIGITAL JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=DIGITAL.LOGID '+\
                'JOIN SUMMARY ON DIGITAL.LOGID = SUMMARY.LOGID '+\
                'ORDER BY SCORE DESC'

       digList = mydb.read_query(query)

       print(COLUMNHEADERS)
       for ent in digList:
           print(self.showData(ent))
       #print(digList,len(digList))