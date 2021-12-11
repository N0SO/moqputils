#!/usr/bin/env python3
"""
moqpdbvhfreport - Display VHF scores only from data stored
                  in the VHF table.

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
- Much of the code replaced was holdover from the file
- processing version, which inefficiently recalculated
- a number of things already available in the LOGHEADER,
- SUMMARY, and QSO tables. Code reworked to:
-    1. Use the VHF field in SUMMARY to determine LOGIDs
-       that contain VHF QSOs.
-    2. Select only QSOs  for the log being scored based
-       on the FREQ field in the QSO table. 
-    3. Count total number of VHF QSOs, also CW, PH and 
-       RY QSOS.
-    4. Use the BONUS fields from SUMMARY when scoring.
-    5. Save only the LOGID and new results in the VHF
-       table. Delete and recreate the table each time.
-    6. Remove all report generation code. Use 
=       moqpdbvhfreports class to display results.
- Lots of 'extra' code was removed.      
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

    def showData(self, log):
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

       call = callsign.upper()

       cquery = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.OPERATORS, LOGHEADER.LOCATION, ' +\
                'VHF.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM VHF JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=VHF.LOGID '
       if (call != 'ALLCALLS'):
           cquery += 'AND LOGHEADER.CALLSIGN="%s" '%(call)

       cquery+= 'JOIN SUMMARY ON VHF.LOGID = SUMMARY.LOGID '+\
                'ORDER BY SCORE DESC'

       digList = mydb.read_query(cquery)

       print(COLUMNHEADERS)
       for ent in digList:
           print(self.showData(ent))
