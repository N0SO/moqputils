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

from cabrilloutils.contestmults import *

VERSION = '0.0.1'

MULTFILES = ['shared/multlists/moqp-counties.csv',
             'shared/multlists/moqp-us-states.csv',
             'shared/multlists/moqp-dx.csv']

class MOQPMults(ContestMults):
    def __init__(self):
       self.mults = self.readmultlists(MULTFILES)

    def getVersion(self):
       return VERSION

