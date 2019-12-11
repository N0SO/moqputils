#!/usr/bin/python

import os
from moqpcategory import *

COMMONCALLS = ['K0M', 'N0M','W0M',
               'K0O', 'N0O','W0O',
               'K0S', 'N0S','W0S']
               
SHOWMECALLS = ['K0H', 'N0H','W0H',
               'K0W', 'N0W','W0W',
               'K0E', 'N0E','W0E']
SHOWMEKEYS = 'SHOWME'
                
MOCALLS = ['K0I', 'N0I','W0I',
                 'K0U', 'N0U','W0U',
                 'K0R', 'N0R','W0R']
MOKEYS = 'MISSOURI'
                 
WILDCARDS = ['W0MA', 'K0GQ']
WILDKEYS = 'MG'



VERSION = '0.1.0'

"""
GenAward - Generic award class
    Generally not called by itself, but is used as a
    code base for other awards like SHOWME and MISSOURI.
    Those classes would inherit this class.
"""
class GenAward():

    def __init__(self):
        pass
        
    """
    Initializes and returns an award object with KEYS
    """
    def init_award(self, KEYS):
        award = dict()
        for key in KEYS:
            award[key] = {0:None, 1:None, 2:None}
        return award

    def combineLists(self, list1, list2):
       retlist = []
       for i in list1:
           retlist.append(i)
       for i in list2:
           retlist.append(i)
       return retlist

    """
    Checks the award object KEYS for all elements set.
    Returns True (BINGO!) if all elements are set
    """
    def _bingo_(self, award, KEYS):
        bingo = True
        for key in KEYS:
            if key in award:
                nokeypresent = True
                for i in range(3):
                   if (award[key][i] != None):
                       nokeypresent = False
                if (nokeypresent): 
                   bingo = False
            else:
                bingo = False
                break
        return bingo

    """
    Checks the call passed in to see if the award object 
    has that key set. Returns True if needed.
    """
    def _checkcall_(self, call, callset, award):
       retval = None
       #print(call)
       if (call in callset):
          key = call[2] 
          #print('call = %s, key = %s'%(call, key))
          if (key in award):
              #print('Found %s for key %s'%(call, key))
              if ( (award[key][0] == None) or \
                   (award[key][1] == None) or \
                   (award[key][2] == None) ):
                  retval = key
       return retval
       
    """
    Make sure a call added to an award is unique
    """
    def isunique(self, call, award):
        index = -1
        if (award[0] == None):
            if ( (award[1] != call) and \
                 (award[2] != call) ): index = 0
        elif (award[1] == None):
            if ( (award[0] != call) and \
                 (award[2] != call) ): index = 1
        elif (award[2] == None):
            if ( (award[0] != call) and \
                 (award[1] != call) ): index = 2
        return index
       
    def checkLog(self, logqsos):
       retval = False
       for qso in logqsos:
          #print(qso)
          key = self._checkcall_(qso['URCALL'], 
                                 self.callset, 
                                 self.Award)
          if (key):
              index = self.isunique(qso['URCALL'], 
                                    self.Award[key])
              if (index != -1):
                  self.Award[key][index] = qso['URCALL']

          if (self._bingo_(self.Award, self.KEYS)):
              #print('***BINGO*** - SHOWME complete!')
              retval = True
              #print(award)
              break
          else:
              #print('Not Bingo!')
              continue
          #print(qso)
          #print(self.award)
       return retval
       
"""
ShowMeAward - Child class of GenAward class
              taylored for the 2019 MOQP SHOWME Award.
"""
class ShowMeAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = SHOWMEKEYS
       self.Award = self.init_award(SHOWMEKEYS)
       self.callset = self.combineLists(SHOWMECALLS, COMMONCALLS)
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)
       
    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
        #print('SHOWME AWARD = %s\nStats: %s'%(Bingo, 
        #                                     self.Award))
        return [Bingo,self.Award]

"""
MissouriAward - Child class of GenAward class
              taylored for the 2019 MOQP MISSOURI Award.
"""
class MissouriAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = MOKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = self.combineLists(MOCALLS, COMMONCALLS)
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)
       
    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
#        print('MISSOURI AWARD = %s\nStats: %s'%(Bingo, 
#                                                  self.Award))
        return [Bingo,self.Award]

"""
BonusAward - Bonus points for working the WILDCARD calls
"""
class BonusAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = WILDKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = WILDCARDS
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))

    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
#        print('MISSOURI AWARD = %s\nStats: %s'%(Bingo, 
#                                                  self.Award))
        return [Bingo,self.Award]



"""
ShowMe - For command line operations. 
"""
class ShowMe(MOQPCategory):

    def __init__(self, pathname = None):
        if (pathname):
            self.appMain(pathname)
            
    def scoreFile(self, pathname):
        log = self.parseLog(pathname)
        if log:
            if (log['ERRORS'] == []):
#                award = ShowMeAward(log['QSOLIST'])
#                awardm = MissouriAward(log['QSOLIST'])
                bonus = BonusAward()
                bonus.appMain(log['QSOLIST'])
                award = ShowMeAward()
                awardm = MissouriAward()
                print(award.appMain(log['QSOLIST']))
                print(awardm.appMain(log['QSOLIST']))
                print(bonus.Award['M'][0],bonus.Award['G'][0])
            else:
                print('log file %s has errors' \
				%(pathname))
        else:
            print(\
            'File %s does not exist or is not in CABRILLO Format'\
                %(pathname))

    def scorefileList(self, pathname):
        for (dirName, subdirList, fileList) in os.walk(pathname, 
                                                   topdown=True):
           if (fileList != ''): 
               Headers = True
               for fileName in fileList:
                   fullPath = ('%s/%s'%(dirName, fileName))
                   self.scoreFile(fullPath)

    def appMain(self, pathname):
        print('Input path: %s'%(pathname))
        if (os.path.isfile(pathname)):
            self.scoreFile(pathname)
        else:
            self.scorefileList(pathname)

if __name__ == '__main__':
   app = ShowMeAward()
   """
   app._checkcall_('N0S')
   app._checkcall_('W0H')
   app._checkcall_('W0O')
   app._checkcall_('W0W')
   app._checkcall_('W0M')
   app._checkcall_('W0E')
   print(app._bingo_(app.award, SHOWMEKEYS))
   print(app.award)
   """
