#!/usr/bin/python
"""
MOQPMults    - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file for the ARRL Missouri QSO Party.
               Inherits from ContestMults() class.
Update History:
* Fri Jan 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

from contestmults import *
from moqpdbutils import *
from moqpdbconfig import *

VERSION = '0.0.1'

MULTFILES = ['shared/multlists/moqp-counties.csv']

COLUMNHEADERS = 'CALLSIGN\tOPS\tLOCATION\tCOUNTY COUNT\t COUNTY NAMES\n'

class MOQPDBCountyMults(ContestMults):
    def __init__(self, callsign=None):
       self.mults = self.readmultlists(MULTFILES)
       if (callsign):
           self.appMain(callsign)

    def getVersion(self):
       return VERSION

    def create_mult_dict(self, indexList):
       multDict = dict()
       for i in indexList:
          multkey = i.strip()
          multDict[multkey] = 0
       return multDict

    def setMult(self, mult, multval):
       retval = False
       if (mult in self.mults):
          self.mults[mult] = multval
          retval = True
       return retval

    def getMultList(self):
        returnList = ''
        for multname in self.mults:
            if (self.mults[multname]):
                returnList += ('%s '%(multname))
        return returnList

class MOQPDBCountyRpt():
    def __init__(self, callsign=None):
       if (callsign):
           self.appMain(callsign)

    def processOne(self, mydb, callsign, Headers = True):
        csvData = None
        logID = mydb.CallinLogDB(callsign)
        ctys=MOQPDBCountyMults()
        if (logID):
            # Get valid QSO list for call
            log = mydb.fetchValidLog(callsign)
            # Loop through QSOS and set mults(counties)
            # present in this log
            if (len(log['QSOLIST']) > 0):
                for qso in log['QSOLIST']:
                    ctys.setMult(qso['URQTH'], qso['ID'])
            # Build report for this log
            if (Headers):
                csvData = COLUMNHEADERS
            else:
                csvData = ''
            csvData += ('%s\t%s\t%s\t'%(callsign,
                                   log['HEADER']['OPERATORS'], 
                                   log['HEADER']['LOCATION']))
            # Get total county count
            csvData += ('%d\t'%(ctys.sumMults())) 
            # Get list of counties worked
            csvData += ('%s'%(ctys.getMultList()))
            #print(csvData)
        return csvData
           
    def processAll(self, mydb):
        csvdata = []
        headers = True
        loglist = mydb.fetchLogList()
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
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata = self.processAll(mydb)
           for csvLine in csvdata:
               print(csvLine)
       else:
           csvdata = self.processOne(mydb, callsign)
           print(csvdata)
