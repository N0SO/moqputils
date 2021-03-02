#!/usr/bin/python

#import os
#from moqpcategory import *

from cabrilloutils.generalaward import *

COMMONCALLS = ['K0M', 'N0M','W0M',
               'K0O', 'N0O','W0O',
               'K0S', 'N0S','W0S']
COMKEYS = 'MOS'
               
SHOWMECALLS = ['K0S', 'N0S','W0S',
               'K0H', 'N0H','W0H',
               'K0O', 'N0O','W0O',
               'K0W', 'N0W','W0W',
               'K0M', 'N0M','W0M',
               'K0E', 'N0E','W0E']
SHOWMEKEYS = ['S','H', 'O', 'W', 'M', 'E']
SHOWMEMATCH = 6
                
                 
WILDCARDS = ['W0MA', 'K0GQ']
WILDKEYS = ['M', 'G']

VERSION = '0.2.0'

        
"""
ShowMeAward - Child class of GenAward class
              taylored for the 2019 MOQP SHOWME Award.
"""
class ShowMeAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = SHOWMEKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = SHOWMECALLS
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)
       
    def sumAward(self):
        retval = 0
        for k in self.KEYS:
            if (self.Award[k][0]['CALL']):
               retval += 1
        return retval
        
    def getStats(self):
        showmeCount = self.sumAward()
        calls = dict()
        for k in ['S','H','O','W','M','E']:
            if (self.Award[k][0]['CALL'] != None):
                calls[k] = self.Award[k][0]['CALL']
            else:
                calls[k] = ' '
        return {'COUNT':showmeCount,
                'CALLS':calls}
                
    def parseAward(self, qsolist):
        for call in self.callset:
            #print('Checking %s'%(call))
            qcount = len(qsolist[call])
            if ( (call in qsolist) and (qcount) ):
                AKey = call[2]  # 3rd char of 1x1 call
                #print('Target = %s'%( self.Award[AKey][0]['CALL']))
                if (self.Award[AKey][0]['CALL'] == None):
                    for i in range(qcount):
                        #print(i, qsolist[call][i])
                        qsolist = self.parseSingleKey(call, AKey, qsolist)
        #print('Award = %s\nqsolist = %s'%(self.Award, qsolist))                    
        return qsolist

    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
        #print('SHOWME AWARD = %s\nStats: %s'%(Bingo, 
        #                                     self.Award))
        return [Bingo,self.Award]


if __name__ == '__main__':
    app = GenAward()
    print('Class ShowMeAward V%s'%(app._get_version()))



