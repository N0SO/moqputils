#!/usr/bin/python3
"""
moqplables - A collection of classes to help search for county
             line operators.

Update History:
* Tue Jun 09 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
* Sat Jun 13 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.2 - Added 3 and 4 county line checks.
-           Pretty crude, lots of false positives.
* Sut Dec 12 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.1.0 - Update for ne DEVMODPATH sctructure.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpdefs import MOCOUNTY

VERSION = '0.0.1'

class CountyLineOps():
    #from moqpawardefs import STATELIST

    def __init__(self, callsign = None,
                        linecount = 3):
        if (callsign):
            self.appMain(callsign, linecount)

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

    def _2counyline(self, qsolist):
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

    def _3counyline(self, qsolist):
       detected = 0
       qsos = len(qsolist)
       if ( qsos > 5 ):
           nomatch = True
           i=0
           while (nomatch and (i < (qsos-3))):
               if ( (qsolist[i]['MYQTH'] != qsolist[i+1]['MYQTH']) and \
                    (qsolist[i]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+1]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+2]['MYQTH'] in MOCOUNTY) ):

                   if( (qsolist[i]['MYQTH'] == \
                           qsolist[i+3]['MYQTH']) and\
                       (qsolist[i+1]['MYQTH'] == \
                           qsolist[i+4]['MYQTH']) and\
                       (qsolist[i+2]['MYQTH'] == \
                           qsolist[i+5]['MYQTH'])    ):
                       nomatch = False
               i += 1
           if (nomatch):
               pass
           else:
               detected = i
       
       return detected

    def _4counyline(self, qsolist):
       detected = 0
       qsos = len(qsolist)
       if ( qsos > 7 ):
           nomatch = True
           i=0
           while (nomatch and (i < (qsos-4))):
               if ( (qsolist[i]['MYQTH'] != qsolist[i+1]['MYQTH']) and \
                    (qsolist[i]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+1]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+2]['MYQTH'] in MOCOUNTY) and \
                    (qsolist[i+3]['MYQTH'] in MOCOUNTY)):

                   if( (qsolist[i]['MYQTH'] == \
                           qsolist[i+4]['MYQTH']) and\
                       (qsolist[i+1]['MYQTH'] == \
                           qsolist[i+5]['MYQTH']) and\
                       (qsolist[i+2]['MYQTH'] == \
                           qsolist[i+6]['MYQTH']) and \
                       (qsolist[i+3]['MYQTH'] == \
                           qsolist[i+7]['MYQTH']) ):
                       nomatch = False
               i += 1
           if (nomatch):
               pass
           else:
               detected = i       
       return detected

    def detectCountyLineOps(self, qsolist, lc):
       if (lc == '2'):
           detected = self._2counyline(qsolist)
       elif (lc =='3'):
           detected = self._3counyline(qsolist)
       elif (lc =='4'):
           detected = self._4counyline(qsolist)
       return detected
        
    def checkCall(self,mydb, call, lc):
       qsolist = self.getdataFromDB(mydb, call)
       countyops = self.detectCountyLineOps(qsolist, lc)
       if (countyops):
          print(\
           'Call: %s - Potential County Line operation detected starting at QSO %d'%\
                                        (call, countyops))

    def appMain(self, call, lc):
       print(call, lc)
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (call =='allcalls'):
           loglist = mydb.fetchLogList()
           for nextlog in loglist:
               self.checkCall(mydb, nextlog['CALLSIGN'], lc)
           
       else:
           self.checkCall(mydb, call, lc)


