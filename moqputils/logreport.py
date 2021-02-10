#!/usr/bin/env python3
"""
logreport - 

Update History:
* Sat Feb 15 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Thu May 07 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Updates for 2020 MOQP:
-          Read config data here instead of in moqpdbutils
-          Added DUPES field to QSO report.
-          Improved error handling.
* Sat Jun 20 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Adding HTML display options to support web apps.
"""

VERSION = '0.1.0' 

from moqputils.moqpdbutils import *
from cabrilloutils.CabrilloUtils import CabrilloUtils
from moqputils.moqpdbconfig import *

class LogReport():

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def processHeader(self, header, endhtml=False):
        cab = CabrilloUtils()
        if (endhtml):
            csvdata ='<p>'
            endstg ='<br>'
        else:
            csvdata = ''
            endstg = '\n'
        for tag in cab.CABRILLOTAGS:
            csvdata += ('%s: %s%s'%(tag, header[tag], endstg))
        if (endhtml):
            csvdata +='</p>'
        return csvdata

    def showQSO(self, qso, html=False):
        if (html):
            fmt ="""<tr>
                    <td><a href='./qslcheck.php?qsoid=%d' target='_blank'>%d</a></td>
                    <td>%d</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td>
                    </tr>"""
        else:
            fmt = '%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'+\
                  '%s\t%s\t%s\t%s\t%s\t%s\n'
        qsoLine = (fmt %( qso['ID'], qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATE'],
                          qso['TIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH'],
                          qso['VALID'],
                          qso['QSL'],
                          qso['NOLOG'],
                          qso['DUPE'],
                          qso['NOQSOS'],
                          qso['NOTE']))
        return qsoLine

    def processQSOs(self, qsolist, header=True):
        if (header):
            csvdata = 'QSOID\tLOGID\tFREQ\tMODE\tDATE\tTIME\t'+ \
                      'MYCALL\tMYREPORT\tMYQTH\t'+ \
                      'URCALL\tURREPORT\tURQTH\t'+ \
                      'VALID\tQSLID\tNOLOG\tDUPE\tNOQSOS\tNOTES\n'
            header = False
        else:
            csvdata = ''
        for qso in qsolist:
            csvdata += self.showQSO(qso)
        return csvdata

    def processOne(self, mydb, callsign):
        logID=mydb.CallinLogDB(callsign)
        if (logID):
            log=mydb.fetchValidLog(callsign)
         
            query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID`=%d) AND (VALID=0) )"%(logID) )
            #print(query)
            invalid_qsos = mydb.read_query(query)

            csvdata = self.processHeader(log['HEADER'])

            csvdata += self.processQSOs(log['QSOLIST'])

            csvdata +=\
                '----------------INVALID QSOS-------------\n'
            csvdata += self.processQSOs(invalid_qsos)
        else:
            csvdata = ('Call %s not in database.'%(callsign))
        
        return csvdata

    def processAll(self, mydb):
        csvdata = []
        headers = True
        #loglist = mydb.read_query( \
        #       "SELECT ID, CALLSIGN FROM logheader WHERE CLUB!='' ORDER BY CLUB ASC")
        loglist = mydb.fetchLogList()
        #print(loglist)
        #print(len(loglist))
        if (loglist):
            Headers = True
            for nextlog in loglist:
                #print(nextlog)
                csvd=self.processOne(mydb, 
                               nextlog['CALLSIGN'])
                csvdata.append(csvd)
                Headers = False
            #print(csvdata)
            return csvdata

    def appMain(self, callsign):
       print('Log Report for %s:'%(callsign))
       csvdata = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata=self.processAll(mydb)
       else:
           csvdata = []
           csvdata.append(self.processOne(mydb, callsign))
       if(csvdata):
           for csvline in csvdata:
               print(csvline)

