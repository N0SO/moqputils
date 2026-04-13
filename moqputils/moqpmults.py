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
"""

from cabrilloutils.contestmults import *

VERSION = '1.0.0'

MULTFILES = ['/usr/local/share/moqputils/multlists/moqp-counties.csv',
             '/usr/local/share/moqputils/multlists/moqp-us-states.csv',
             '/usr/local/share/moqputils/multlists/moqp-dx.csv']

class MOQPMults(ContestMults):
    def __init__(self, qsolist=None):
       self.mults = self.readmultlists(MULTFILES)

       if (qsolist):
           self.sumMultsinQSOList(qsolist)

    def getVersion(self):
       return VERSION

if __name__ == '__main__':
    app=MOQPMults()
    print(f'MOQP Contest Mults (MOQPMults) V{app.getVersion()}')
