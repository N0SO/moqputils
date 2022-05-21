#!/usr/bin/env python3
"""
DUPECheck  - Check logs submitted for the ARRL Missouri
QSO Party for DUPES
Update History:
* Fri Apr 17 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
* Fri Feb 26 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0
- Added 'DUPE of QSO xx' to qso['NOTES'] and set new
- qso['ERROR'] flag for dupes to mark qso as invalid.
* Sat Feb 27 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1
- Added code to make sure oldest QSO is kept and newer
- qso is marked as DUPE regardless of order in log.
* Tue May 17 2022  Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.2
- Added code to use the ['QID'] key/field to mark DUPES.
- The previous version was marking the correct DUPE with
- the wrong DUPE ID, making it difficult for a human to
- confirm the DUPE. This was only on the MOQPCategory-
- updates branch and was never a problem in the Master.
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
       return dupe
              
    def findDupes(self, qsolist):
       newlist = self.addDupefield(qsolist)
       qcount = len(newlist)
       if (qcount > 1):
          for q in range(qcount): 
             if (q > 0): #Skip first QSO
                 if newlist[q]['ERROR'] == False: #Skip invalid QSOs
                    #for t in range(qcount-1):
                    for t in range(q-1):
                         if (t != q) and (newlist[t]['ERROR'] == False):
                             dupe = self.compareqsos(newlist[q], 
                                                 newlist[t])
                             if (dupe):
                                 #Determine which QSO is older
                                 if (newlist[q]['DATETIME'] >= newlist[t]['DATETIME']):
                                     dupeOf = q
                                     dupeIs = t
                                 else:
                                     dupeOf = t
                                     dupeIs = q
                                 newlist[dupeOf]['DUPE'] = newlist[dupeIs]['QID']
                                 #newlist[dupeOf]['NOTES'] = 'DUPE of QSO %d'%(dupeIs+1)
                                 newlist[dupeOf]['ERROR'] = True
                                 #print('QSO {} DUPE of qso {}:\n{}\n{}'.format(newlist[dupeOf]['QID'],newlist[dupeIs]['QID'], newlist[t], newlist[q]))
       return newlist
