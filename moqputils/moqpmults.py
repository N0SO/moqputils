#!/usr/bin/env python3
"""
MOQPMults    - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file for the ARRL Missouri QSO Party.
               Inherits from ContestMults() class.
Update History:
* Fri Jan 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
* Sat Feb 27 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0
- Added call to parent class method sumMultsinQSOList 
- if a QSO list is passed as an input parameter.
* Fri Apr 10 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0
- Updates to support new mobile/rover bonus for making
- 50 or more QSOs in a county. The mobile/rover will
- get credit for that county when the 50+ QSO mark
- is reached.
- Updated to look for contest mult definition files
- in /usr/local/share/moqputils/multlists
* Fri Apr 24 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.1
- Added child class MOQPMults_E to process the new
- county credit for mobile/portable stations. This
- will be used to add Enhancemnent Issue #67,
- 50 County Activation Credit for Mobles and Portable
- Stations.
* Fri Apr 24 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.2
- Added code to pass in the CAT-STATION field from the
- cabrillo header and only apply the activation credit
- for MOBILE, PORTABLE, ROVER stations.

"""

from cabrilloutils.contestmults import *
from moqputils.moqpdefs import MOCOUNTY

VERSION = '1.0.2'
THRESHOLD = 50 #Threshold for the This County Activated bonus
CATSTATION = ['MOBILE',
              'PORTABLE',
              'ROVER']
QUERY = """
        SELECT MYQTH, COUNT(*) AS occurrences
        FROM QSOS WHERE LOGID={}
        GROUP BY MYQTH
        order by occurrences DESC
        """

MULTFILES = ['/usr/local/share/moqputils/multlists/moqp-counties.csv',
             '/usr/local/share/moqputils/multlists/moqp-us-states.csv',
             '/usr/local/share/moqputils/multlists/moqp-dx.csv']

class MOQPMults(ContestMults):
    def __init__(self, qsolist=None):
       self.mults = self.readmultlists(MULTFILES)

       if (qsolist):
           self.sumMultsinQSOList(qsolist)

    def __version__(self):
       return VERSION

    def getVersion(self):
       return self.__version__()

class MOQPMults_E(MOQPMults):
       def __init__(self, 
                    qsolist=None, 
                    station=None,
                    logID=None, 
                    mydb=None):
           super().__init__(qsolist)
           self.logID = logID
           self.mydb = mydb
           self.station = station
           self.activatedCount50 = 0
           self.activatedNames = []
           if station in CATSTATION and (logID and mydb):
               self.countActivations()

       def countActivations(self):
           #Get counties activated list
           qsos = self.mydb.read_query(QUERY.format(self.logID))
           for qso in qsos:
               if qso['MYQTH'] in MOCOUNTY:
                   if qso['occurrences'] >= THRESHOLD:
                       self.setMult(qso['MYQTH'])
                       self.activatedCount50 += 1
                   self.activatedNames.append([ qso['MYQTH'],
                                                qso['occurrences'] ])

       def getActivatedNamesCount(self):
           return len(self.activatedNames)

