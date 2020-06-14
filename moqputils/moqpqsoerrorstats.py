#!/usr/bin/env python3
"""
MOQPQSOErrorStats - Count valid and invalid QSOs in the MOQP
                    database and calculate error percentage. 

                  Prerequisits:
                   1. All logs loaded into database with
                      mqplogcheck -l
                   2. QSO Validation completed on all logs
                      with qsocheck -c allcalls
                  Added for the 2020 MOQP.
                  
Update History:
* Sat Jun 13 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

from moqpdbutils import *
from moqpdbconfig import *


VERSION = '0.0.1' 

COLUMNHEADERS = \
     'CALLSIGN\tVALID QSOs\tINVALID QSOs\tERROR PERCENT'
                

class MOQPQSOErrorStats():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsv(self, gq, bq, qp, call):
        csvdata='%s\t%d\t%d\t%.1f'%(call, gq, bq, qp*100)
        return csvdata

    def computeOne(self, mydb, call):
        query = """SELECT LOGHEADER.CALLSIGN,
                   LOGHEADER.LOCATION, LOGHEADER.CABBONUS,
                   LOGHEADER.OPERATORS, QSOS.*
                   FROM QSOS INNER JOIN LOGHEADER ON
                   LOGHEADER.ID=QSOS.LOGID
                   WHERE (CALLSIGN=%s AND VALID=%s)"""
                   
        goodqsos = mydb.read_pquery(query,[call, 1])
        badqsos = mydb.read_pquery(query,[call, 0])
        gq = len(goodqsos)
        bq = len(badqsos)
        qt = gq+bq
        if (gq == 0):
            ep = 1.0
        elif (bq == 0):
            ep = 0.0
        else:
            fbq=float(bq)
            fqt=float(qt)        
            ep = fbq/fqt
        return gq, bq, ep

    def ProcessData(self, mydb, call):
       ReportList = []
       if(call == 'allcalls'):
           loglist = mydb.fetchLogList()
           call_list = []
           for log in loglist:
               call_list.append(log['CALLSIGN'])
           #loglist = mydb.read_query( \
           #   "SELECT ID, CALLSIGN FROM logheader WHERE 1")
       else:
           call_list = [call]
       for nextcall in call_list:
           gq, bq, qp = self.computeOne(mydb, nextcall)
           tsvline = self.exportcsv(gq, bq, qp, nextcall)
           ReportList.append(tsvline)      
       return ReportList

    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       csvList = self.ProcessData(mydb, callsign)
       if (csvList):
           print(COLUMNHEADERS)
           for line in csvList:
               print(line)

