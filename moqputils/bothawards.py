#!/usr/bin/python

#import os
#from moqpcategory import *
#from generalaward import *
from showmeaward import ShowMeAward
from missouriaward import MissouriAward
from bonusaward import BonusAward

#VERSION = '0.2.0'
COMMONCALLS = ['K0M', 'N0M','W0M',
               'K0O', 'N0O','W0O',
               'K0S', 'N0S','W0S']
COMKEYS = 'MOS'
               
SHOWMECALLS = ['K0H', 'N0H','W0H',
               'K0W', 'N0W','W0W',
               'K0E', 'N0E','W0E']
SHOWMEKEYS = 'EHW'
SHOWMEMATCH = 6
                
MOCALLS = ['K0I', 'N0I','W0I',
           'K0U', 'N0U','W0U',
           'K0R', 'N0R','W0R']
MOKEYS = 'IRU'
MOMATCH = 8

WILDCARDS = ['W0MA', 'K0GQ']
                 

"""
BothAwards - Checks for:
             2019 MOQP SHOWME Award
             2019 MOQP MISSOURI Award
             2019 MOQP BONUS stations
"""
class BothAwards():

    VERSION = '0.2.0'

    def __init__(self, callsign=None, qsolist=None):
        self._showmeAward_ = ShowMeAward()
        self._missouriAward_ = MissouriAward()
        self._bonusAward_ = BonusAward()
#        self.KEYS = COMKEYS+SHOWMEKEYS+MOKEYS
#        self.Award = self.init_award(self.KEYS)
#        self.callset = self.combineListoflists( [SHOWMECALLS, 
#                                                 COMMONCALLS,
#                                                 MOCALLS ] )
#        print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                     self.Award, 
#                                                     self.callset))
        if (qsolist):
              self.appMain(callsign, qsolist)
              
    def parseAwards(self):
       """
       parseAwards -
       Fills the the _showme_.Award and _missouri_.Award elements
       with call signs from the database self.Awards. As each 
       self.Awards element is used, it is set to None to prevent
       being used again.
       """
       
       #SHOWME only requires one call per letter (key)
       for thiskey in self._showmeAward_.KEYS:
           print('checking for key %s...'%(thiskey))
           i = self.parseSingleKey(self.Award[thiskey], 
                               self._showmeAward_.Award[thiskey][0])
           if ( i >= 0):
               self._showmeAward_.Award[thiskey][0] = \
                                  self.Award[thiskey][i]
               self.Award[thiskey][i] = None
               
       #MISSOURI requires two S keys and two I keys
       for thiskey in self._missouriAward_.KEYS:
           if (thiskey in 'IS'):
               r = 2
           else:
               r = 1
           for ai in range(r):
               i = self.parseSingleKey(self.Award[thiskey], 
                               self._missouriAward_.Award[thiskey][ai])
               if ( i >= 0):
                   self._missouriAward_.Award[thiskey][ai] = \
                                  self.Award[thiskey][i]
                   self.Award[thiskey][i] = None
       
    """
    Fill the self.Awards elements with callsigns from the qso
    list passed in (logqsos) that match an element in the list
    self.callset. This will become our database of available
    calls for the SHOWME and MISSOURI awards.
    
    If the station happens to have worked all of the 1x1
    stations, checkLog returns True.
    """
    def checkLog(self, logqsos):
       #print('Running checkLog in class BothAwards')
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
       
    def appMain(self, callsign, qsolist):
        callList = self._showmeAward_.combineListoflists( \
                                           [COMMONCALLS,
                                            SHOWMECALLS,
                                            MOCALLS])
        #print('callList =%s'%(callList))
        qso1x1 = self._showmeAward_.collect1x1qsos(qsolist, 
                                                   callList)
        
        #print(qso1x1)
        #self.show1x1QSOs(qso1x1)
        #Bingo = self.checkLog(qsolist)
        Bonus = BonusAward(qsolist)
        #print(Bonus.Award)
        qso1x1 = self._showmeAward_.parseAward(qso1x1)
        #print(self._showmeAward_.Award)
        #self.show1x1QSOs(qso1x1)
        
        #self.show1x1QSOs(qso1x1)
        wildcard = Bonus.getNextUnused()
        if (wildcard != ''): Bonus.Award[wildcard]['WC'] = True
        #print('First wildcard is %s'%(wildcard))
        showmeStats = self._showmeAward_.qualify(SHOWMEMATCH, wildcard)
        #print(showmeStats)
        wildcard =''
        qso1x1 = self._missouriAward_.parseAward(qso1x1)
        wildcard = Bonus.getNextUnused()
        if (wildcard != ''): Bonus.Award[wildcard]['WC'] = True
        #print('2nd wildcard is %s'%(wildcard))
        missouriStats = self._missouriAward_.qualify(MOMATCH, wildcard)
#        print(missouriStats)
        #print(Bonus.getBonusList())
        return { 'SHOWME' : showmeStats,
                 'MO' : missouriStats,
                 'BONUS' : { 'W0MA': Bonus.Award['W0MA']['INLOG'],
                             'K0GQ':Bonus.Award['K0GQ']['INLOG']}}



if __name__ == '__main__':
   app = BothAwards()
   print('Class BothAwards V%s\n' \
         'Class MissouriAward V%s\n' \
         'Class ShowMeAward V%s' %( \
          self._showmeAward_._get_version(),
          self._missouriAward_._get_version(),
          self._bonusAward_._get_version()) )
