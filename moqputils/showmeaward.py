#!/usr/bin/python

import os
from moqpcategory import *

COMMONCALLS = ['K0M', 'N0M','W0M',
               'K0O', 'N0O','W0O',
               'K0S', 'N0S','W0S']
               
SHOWMECALLS = ['K0H', 'N0H','W0H',
               'K0W', 'N0W','W0W',
               'K0E', 'N0E','W0E']
                
MOCALLS = ['K0I', 'N0I','W0I',
                 'K0U', 'N0U','W0U',
                 'K0R', 'N0R','W0R']
                 
WILDCARDS = ['W0MA']

SHOWMEKEYS = 'SHOWME'

MOKEYS = 'MISSOURI'

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
            award[key] = None
        return award

    """
    Checks the award object KEYS for all elements set.
    Returns True (BINGO!) if all elements are set
    """
    def _bingo_(self, award, KEYS):
        bingo = True
        retval = False
        for key in KEYS:
            if key in award:
                if (award[key] == None):
                   bingo = False
                   break
            else:
                break
        retval = bingo
        return retval

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
              if (award[key] == None):
                  retval = key
       return retval
       
    def combineLists(self, list1, list2):
       retlist = []
       for i in list1:
           retlist.append(i)
       for i in list2:
           retlist.append(i)
       return retlist

    def checkLog(self, logqsos):
       retval = False
       for qso in logqsos:
          #print(qso)
          key = self._checkcall_(qso['URCALL'], 
                                 self.callset, 
                                 self.Award)
          if (key):
              self.Award[key] = qso['URCALL']
              
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
                award = ShowMeAward()
                awardm = MissouriAward()
                print(award.appMain(log['QSOLIST']))
                print(awardm.appMain(log['QSOLIST']))
            else:
                print('log file %s has errors:\n %s'\
				%(pathname, log['ERRORS']))

    def scorefileList(self, pathname):
        for (dirName, subdirList, fileList) in os.walk(pathname, topdown=True):
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
