#!/usr/bin/env python3
"""
qsoutils - Utilities for processing and validating QSO: lines
           from CABRILLO files.
Update History:
* Thu Apr 16 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
* Sun May 03 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Added more date formats to QSO date checks
- two-digit year formats added.
* Fri May 15 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3 - Added more qso time utils
- Fixed a bug in getBand causing false DUPES
"""
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from CabrilloUtils import CabrilloUtils

VERSION = '0.0.1' 
           
class QSOUtils(CabrilloUtils):
    def __init__(self):
        pass
        
    def getVersion(self):
       return VERSION

    def getBand(self, freq):
       band = None
       try:
           nfreq = float(freq)
       except:
           nfreq = 0
       
       if (nfreq >= 1800.0 and nfreq <= 2000.0):
           band = '160M'
       elif (nfreq >= 3500.0 and nfreq <= 4000.0):
           band = '80M'
       elif (nfreq >= 7000.0 and nfreq <= 7300.0):
           band = '40M'
       elif (nfreq >= 14000.0 and nfreq <= 14350.0):
           band = '20M'
       elif (nfreq >= 21000.0 and nfreq <= 21450.0):
           band = '15M'
       elif (nfreq >= 28000.0 and nfreq <= 29700.0):
           band = '10M'
       elif ( (nfreq >= 50000.0 and nfreq <= 54000.0) or \
               (nfreq == 50.0) ):
           band = '6M'
       elif ( (nfreq >= 144000.0 and nfreq <= 148000.0) or \
              (nfreq == 144.0) ):
           band = '2M'
       elif ( (nfreq >= 420000.0 and nfreq <= 450000.0) or \
              (nfreq == 432.0) ):
           band = '432'

       return band
       
    def qsotimeOBJ(self, ldate, ltime):
       datefmts = ['%Y-%m-%d', 
                   '%Y/%m/%d', 
                   '%Y%m%d', 
                   '%m-%d-%Y', 
                   '%m/%d/%Y',
                   '%y-%m-%d', 
                   '%y/%m/%d', 
                   '%y%m%d', 
                   '%m-%d-%y', 
                   '%m/%d/%y']
                   
       timefmts = ['%H%M', '%H:%M', '%H %M']
       logtimeobj = None

       logtime = self.padtime(ltime)
       logdate = ldate

       #Date
       datefcount = len(datefmts)
       timefcount = len(timefmts)
       d=0
       while (d<datefcount):
           try:
               datefstg = datefmts[d]
               dateobj=datetime.strptime(logdate, datefstg)
               #print(dateobj)
               d=datefcount
           except:
               #print('Format %s did not work for date %s.'%(datefstg, logdate))
               d += 1

       #time
       t=0
       while (t<timefcount):
           try:
               timefstg = timefmts[t]
               timeobj=datetime.strptime(logtime, timefstg)
               #print(timeobj)
               t=timefcount
           except:
              #print('Format %s did not work for time %s.'%(timefstg, logtime))
              t += 1
       try:
           logtimeobj = datetime.strptime(logdate+' '+logtime, datefstg+' '+timefstg)
       except:
           logtimeobj = None
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

    def validateQSOtime(self, qsodate, qsotime):
        timeValid = False
        """ Defines contest period in UTC. This needs to be 
            read in from a config file. """
        day1Start = self.qsotimeOBJ('2020-04-04', '1400')
        day1Stop = self.qsotimeOBJ('2020-04-05', '0400')
        day2Start = self.qsotimeOBJ('2020-04-05', '1400')
        day2Stop = self.qsotimeOBJ('2020-04-05', '2000')
        logtime = self.qsotimeOBJ(qsodate, qsotime)
        if (logtime):
           if ( ((logtime >= day1Start) and \
                                       (logtime <= day1Stop)) \
              or ((logtime >= day2Start) and \
                                       (logtime <= day2Stop)) ):
              timeValid = True
        return timeValid

    def showQSO(self, qso):
        fmt = '%s %s %s %s %s %s %s %s %s %s %s'
        qsoLine = (fmt %( qso['DUPE'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATE'],
                          qso['TIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH']))
        return qsoLine

    def compareCalls(self, call1, call2):
        callvalid=False
        """ Strip off any extra stuff after a / or \ at the
            end of the callsigns """
        call1_s = self.stripCallsign(call1)
        call2_s = self.stripCallsign(call2)
        if (call1_s == call2_s):
            callvalid=True
        return callvalid

