#!/usr/bin/python3
"""
moqplables - A collection of classes to help search for county
             line operators.

Update History:
* Tue Jun 09 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

from moqpdbutils import *
from moqpdbconfig import *
from moqpdefs import MOCOUNTY

VERSION = '0.0.1'

class CountyLineOps():
    #from moqpawardefs import STATELIST

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def getdataFromDB(self, db, call):
        qsolist = None
        qsolist = db.read_pquery(\
                 """SELECT LOGHEADER.CALLSIGN, 
                           LOGHEADER.OPERATORS,
                           LOGHEADER.LOCATION, QSOS.*
                           FROM LOGHEADER JOIN QSOS
                           ON LOGHEADER.ID=QSOS.LOGID
                           WHERE CALLSIGN=%s
                           ORDER BY QSOS.ID""", [call])
        return qsolist

    def detectCountyLineOps(self, qsolist):
       detected = 0
       qsos = len(qsolist)
       if ( qsos > 3 ):
           nomatch = True
           i=0
           while (nomatch and (i < (qsos-2))):
               if ( (qsolist[i]['MYQTH'] != qsolist[i+1]['MYQTH']) and \
                    (qsolist[i]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+1]['MYQTH'] in MOCOUNTY) ):

                   if( (qsolist[i]['MYQTH'] == \
                           qsolist[i+2]['MYQTH']) and\
                       (qsolist[i+1]['MYQTH'] == \
                           qsolist[i+3]['MYQTH']) ):
                       nomatch = False
               i += 1
           if (nomatch):
               pass
           else:
               detected = i
       return detected
        
    def checkCall(self,mydb, call):
       qsolist = self.getdataFromDB(mydb, call)
       countyops = self.detectCountyLineOps(qsolist)
       if (countyops):
          print(\
           'Call: %s - Potential County Line operation detected starting at QSO %d'%\
                                        (call, countyops))

    def appMain(self, call):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (call =='allcalls'):
           loglist = mydb.fetchLogList()
           for nextlog in loglist:
               self.checkCall(mydb, nextlog['CALLSIGN'])
           
       else:
           self.checkCall(mydb, call)


