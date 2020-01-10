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

VERSION = '0.0.1'

MOCOUNTYMULTS = []

class MOQPMults(ContestMults):

    def __init__(self):
        self.multList = self.combine_multLists([MOCOUNTYMULTS,
                                                STATEMULTS,
                                                PROVIDENCEMULTS,
                                                ['DX'] ])
        
        self.mults = self.creat_mult_dict(self.multList)
        
        
