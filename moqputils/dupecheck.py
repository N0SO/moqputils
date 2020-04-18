#!/usr/bin/env python3
"""
DUPECheck  - Check logs submitted for the ARRL Missouri
QSO Party for DUPES
Update History:
* Fri Apr 17 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
"""

from qsoutils import QSOUtils

class DUPECheck(QSOUtils):

    def __init__(self, qsolist = None):
       if (qsolist):
          self.newlist = self.findDupes(qsolist)   
       else:
          self.newlist = None

    def getVersion(self):
       return VERSION
       
    def addDupefield(self, qsolist):
       newlist = []
       for qso in qsolist:
          qso['DUPE'] = 0
          newlist.append(qso)
       return newlist

    def compareqsos(self, tqso, cqso):
       dupe = False
       tcall = self.stripCallsign(tqso['URCALL'])
       ccall = self.stripCallsign(cqso['URCALL'])
       if (tcall == ccall):
          tband = self.getBand(tqso['FREQ'])
          cband = self.getBand(cqso['FREQ'])
          if (tband == cband):
             if (tqso['MODE'] == cqso['MODE']):
                if (tqso['URQTH'] == cqso['URQTH']):
                   if (tqso['MYQTH'] == cqso['MYQTH']):
                      dupe = True
       """               
       if (dupe):
          print('----\ntcall: %s <==> ccall: %s'%(tcall, ccall))
          print('tband: %s <==> cband: %s'%(tband, cband))
          print('tmode: %s <==> cmode: %s'%(tqso['MODE'], cqso['MODE']))
          print('turqth: %s <==> curqth: %s'%(tqso['URQTH'], cqso['URQTH']))
          print('tmyqth: %s <==> cmyqth: %s'%(tqso['MYQTH'], cqso['MYQTH']))
       """   
       return dupe
              
    def findDupes(self, qsolist):
       newlist = self.addDupefield(qsolist)
       qcount = len(newlist)
       if (qcount > 1):
          for q in range(qcount):
             for t in range(qcount):
                if (q == t):
                   t += 1
                else:
                      if (newlist[q-1]['DUPE'] == 0):
                         dupe = self.compareqsos(newlist[q-1], 
                                                 newlist[t-1])
                      if (dupe):
                         newlist[t-1]['DUPE'] = q          
       return newlist
