#!/usr/bin/env python3
"""
DUPECheck  - Check logs submitted for the ARRL Missouri
QSO Party for DUPES
Update History:
* Fri Apr 17 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
"""

from cabrilloutils.qsoutils import QSOUtils

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
       #print(tqso, cqso)
       if (tcall == ccall):
          #print('tcall = %s, ccall =%s'%(tcall, ccall))
          tband = self.getBand(tqso['FREQ'])
          cband = self.getBand(cqso['FREQ'])
          if (tband == cband):
             #print('tband = %s, cband =%s'%(tband, cband))
             if (tqso['MODE'] == cqso['MODE']):
                #print('tmode = %s, cmode =%s'%(tqso['MODE'], cqso['MODE']))
                if (tqso['URQTH'] == cqso['URQTH']):
                   #print('turqth = %s, curqth =%s'%(tqso['URQTH'], cqso['URQTH']))
                   if (tqso['MYQTH'] == cqso['MYQTH']):
                      dupe = True
                      #print('tmyqth = %s, cmyqth =%s'%(tqso['MYQTH'], cqso['MYQTH']))
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
             if (q > 0): #Skip first QSO
                 for t in range(q-1):
                     dupe = self.compareqsos(newlist[q], 
                                                 newlist[t])
                     if (dupe):
                         newlist[q]['DUPE'] = t+1
       return newlist
