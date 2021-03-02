#!/usr/bin/python

#import os
#from moqpcategory import *
from cabrilloutils.generalaward import *

MOCALLS = ['K0M', 'N0M','W0M',
           'K0I', 'N0I','W0I',
           'K0S', 'N0S','W0S',
           'K0O', 'N0O','W0O',
           'K0U', 'N0U','W0U',
           'K0R', 'N0R','W0R']
           
MOKEYS = ['M', 'I0', 'S0', 'S1', 'O', 'U', 'R', 'I1']

MOMATCH = 8
                 
WILDCARDS = ['W0MA', 'K0GQ']
WILDKEYS = ['M', 'G'] # Use 3rd char as key for cosistancy with 1x1 calls



VERSION = '0.2.0'


"""
MissouriAward - Child class of GenAward class
              taylored for the 2019 MOQP MISSOURI Award.
"""
class MissouriAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = MOKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = MOCALLS
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)
       
    def getStats(self):
        Count = self.sumAward()
        calls = dict()
        for k in MOKEYS:
            if (self.Award[k][0]['CALL'] != None):
                calls[k] = self.Award[k][0]['CALL']
            else:
                calls[k] = ' '
        return {'COUNT':Count,
                'CALLS':calls}

    def sumAward(self):
        retval = 0
        #missouriCount = missoursCount = 0
        for k in self.KEYS:
            if (self.Award[k][0]['CALL']):
               retval += 1
        """
        Account for the two I and S letters in MISSOURI
        """
        #if (self.Award['I'][1]): missouriCount +=1
        #if (self.Award['S'][1]): missoursCount +=1
        return retval

    """
    Parse list of 1x1 calls looking for:
       1x1 calls who's suffix (i.e. 3rd char of call)
       matches one of the key entries in self.KEYS.

    If a match is found in self.KEYS, AND the
    1x1 call list entry is not marked as USED
    (qsolist[call][i]['USED'] == False) then
    copy the call data elements (BAND, MODE, QTH)
    to self.Award[key] and mark the call as used
    in the 1x1 call list.
    
    The updated 1x1 call list is returned to the 
    caller and should be used to replace the one
    passed in.
    """
    def parseAward(self, qsolist):
        for call in self.callset:
            #print('Checking %s'%(call))
            qcount = len(qsolist[call])
            if ( (call in qsolist) and (qcount) ):
                AKey = call[2]  # 3rd char of 1x1 call
                #Allow for two I and S chars for MISSOURI
                repeat = True
                #print ('preloop')
                while (repeat):
                    #print('looping, AKey = %s'%(AKey))
                    if ( (AKey == 'I') or (AKey == 'S') ):
                        dual = True
                        if (AKey == 'I'): 
                            if (self.Award['I0'][0]['CALL'] == None):
                                AKey ='I0'
                            elif (self.Award['I1'][0]['CALL'] == None):
                                AKey = 'I1'
                            else:
                                AKey = None
                        elif (AKey =='S'): 
                            if (self.Award['S0'][0]['CALL'] == None):
                                AKey ='S0'
                            elif (self.Award['S1'][0]['CALL'] == None):
                                AKey = 'S1'
                            else:
                                AKey = None
                    #print (AKey)
                    if (AKey):
                        #print(self.Award)
                        #print('Target = %s'%( self.Award[AKey][0]))
                        qsolist = self.parseSingleKey(call, AKey, qsolist)
                        if (AKey in ['M','S1','O','U','R','I1']):
                            repeat = False
                        elif (AKey == 'I0'): AKey = 'I1'
                        elif (AKey == 'S0'): AKey = 'S1'
                    else: repeat = False
                
        #self.show1x1QSOs(qsolist)
        return qsolist

    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
#        print('MISSOURI AWARD = %s\nStats: %s'%(Bingo, 
#                                                  self.Award))
        return [Bingo,self.Award]


if __name__ == '__main__':
   app = MissouriAward()
   print('Class MissouriAward V%s'%(app._get_version()))
   
