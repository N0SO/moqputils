#!/usr/bin/env python3
"""
logreport - 

Update History:
* Sat Feb 15 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

VERSION = '0.0.1' 

from moqpdbutils import *
from CabrilloUtils import CabrilloUtils

class LogReport():

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def processHeader(self, header):
        cab = CabrilloUtils()
        csvdata = ''
        for tag in cab.CABRILLOTAGS:
            csvdata += ('%s: %s\n'%(tag, header[tag]))
        return csvdata

    def showQSO(self, qso):
        fmt = '%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'
        qsoLine = (fmt %( qso['ID'],
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
                          qso['NOQSOS'],
                          qso['NOTE']))
        return qsoLine

    def processQSOs(self, qsolist, header=True):
        if (header):
            csvdata = 'QSOID\tLOGID\tFREQ\tMODE\tDATE\tTIME\t'+ \
                      'MYCALL\tMYREPORT\tMYQTH\t'+ \
                      'URCALL\tURREPORT\tURQTH\t'+ \
                      'VALID\tQSLID\tNOLOG\tNOQSOS\tNOTES\n'
            header = False
        else:
            csvdata = ''
        for qso in qsolist:
            csvdata += self.showQSO(qso)
        return csvdata

    def processOne(self, mydb, callsign):
        log=mydb.fetchValidLog(callsign)

        logID=mydb.CallinLogDB(callsign)
         
        query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID`=%d) AND (VALID=0) )"%(logID) )
        #print(query)
        invalid_qsos = mydb.read_query(query)

        csvdata = self.processHeader(log['HEADER'])

        csvdata += self.processQSOs(log['QSOLIST'])

        csvdata +='----------------INVALID QSOS-------------\n'
        csvdata += self.processQSOs(invalid_qsos)
        
        return csvdata
        


    def processAll(self, mydb):
        csvdata = []
        headers = True
        loglist = mydb.read_query( \
               "SELECT ID, CALLSIGN FROM logheader WHERE CLUB!='' ORDER BY CLUB ASC")
        #loglist = mydb.fetchLogList()
        #print(loglist)
        #print(len(loglist))
        if (loglist):
            Headers = True
            for nextlog in loglist:
                #print(nextlog)
                csvd=self.processOne(mydb, 
                               nextlog['CALLSIGN'], Headers)
                csvdata.append(csvd)
                Headers = False
            #print(csvdata)
            return csvdata

    def appMain(self, callsign):
       print('Log Report for %s:'%(callsign))
       csvdata = ['No Data.']
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata=self.processAll(mydb)
       else:
           csvdata = self.processOne(mydb, callsign)
           print(csvdata)
#       for csvLine in csvdata:
#           print(csvdata)
