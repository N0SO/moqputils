#!/usr/bin/env python3
"""
qsoutils - Utilities for processing and validating QSO: lines
           from CABRILLO files.
Update History:
* Thu Apr 16 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
"""
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

VERSION = '0.0.1' 
           
class QSOUtils():
    def __init__(self):
        pass
        
    def getVersion(self):
       return VERSION
       
    def qsotimeOBJ(self, ldate, ltime):
       datefmts = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%m-%d-%Y', '%m/%d/%Y']
       timefmts = ['%H%M', '%H:%M', '%H %M']
       logtimeobj = None

       logtime = self.padtime(ltime)
       logdate = ldate

       #Date
       d=0
       while (d<5):
           try:
               datefstg = datefmts[d]
               dateobj=datetime.strptime(logdate, datefstg)
               #print(dateobj)
               d=5
           except:
               #print('Format %s did not work for date %s.'%(datefstg, logdate))
               d += 1

       #time
       t=0
       while (t<2):
           try:
               timefstg = timefmts[t]
               timeobj=datetime.strptime(logtime, timefstg)
               #print(timeobj)
               t=3
           except:
              #print('Format %s did not work for time %s.'%(timefstg, logtime))
              t += 1

       logtimeobj = datetime.strptime(logdate+' '+logtime, datefstg+' '+timefstg)
       return logtimeobj
       

    def padtime(self, timestg):
        count = len(timestg)
        if (count < 4):
            pads = 4 - count
            padtime =''
            for i in range(pads):
                padtime += '0'
            padtime += timestg
        elif (count > 4):
            padtime = timestg[:3]
        else:
            padtime = timestg
        return padtime

