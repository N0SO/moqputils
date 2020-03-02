#!/usr/bin/python
"""
MOQPMults    - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file for the ARRL Missouri QSO Party.
               Inherits from ContestMults() class.
Update History:
* Sat Feb 22 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

from contestmults import *
from moqpdbutils import *

VERSION = '0.0.1'

COUNTYLIST = ['shared/multlists/Countylist.csv']

COLUMNHEADERS = 'COUNTY (ABREV)\tQSO COUNT'

class MOQPDBCountyCount(ContestMults):
    def __init__(self, callsign=None):
       self.mults = self.readmultlists(COUNTYLIST)
       if (callsign):
           self.appMain(callsign)

    def create_mult_dict(self, indexList):
       multDict = dict()
       #print(indexList)
       for i in indexList:
           if ('#US States' in i):
               break # Stop at end of MO counties list
           if (i[0] != '#'): # Skip comment lines
               iparts = i.split(',')
               multkey = str(iparts[1].rstrip().lstrip())
               multname = str(iparts[0].rstrip())
               #print(iparts, multkey, multname)
               multDict[multkey] = { 'FULLNAME' : multname,
                                     'COUNT' :  0 }
       #print(multDict)
       return multDict

    def setMult(self, mult):
       retval = False
       if (mult in self.mults):
          self.mults[mult]['COUNT'] += 1
          retval = True
       return retval

    def getMultList(self):
        returnList = []
        for multname in self.mults:
            returnList.append(('%s'%(multname)))
        return returnList

class MOQPDBCountyCountRpt():
    def __init__(self, validqsos):
       self.appMain()

    def processAll(self, mydb):
        ctys=MOQPDBCountyCount()
        query = "SELECT * FROM `QSOS` WHERE 1"
        qsolist = mydb.read_query(query)
        print("Total number of valid QSOS: %d"%(len(qsolist)))
        for qso in qsolist:
            ctys.setMult(qso['URQTH'])
        return ctys
    
    def appMain(self):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       countyData = self.processAll(mydb)
       counties = list(countyData.getMultList())
       print('%s'%(COLUMNHEADERS))
       for county in counties:
           print('%s (%s)\t%d'%(countyData.mults[county]['FULLNAME'], 
                               county,
                               countyData.mults[county]['COUNT']))

