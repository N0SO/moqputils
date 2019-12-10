#!/usr/bin/python
"""
ShowMe  - Determine which Missouri QSO Party stations 
          qualify for the ShowMe and/or MISSOURI awards

Update History:
* Thu Dec 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start of work
"""

from moqpcategory import *
import os
from showmeaward import ShowMeAward



class ShowMe(MOQPCategory):

    

    def __init__(self, pathname = None):
        if (pathname):
            self.appMain(pathname)

    def appMain(self, pathname):
        print('Input path: %s'%(pathname))
        log = self.parseLog(pathname)
        award = ShowMeAward(log['QSOLIST'])
        
        
    
