#!/usr/bin/python

#import os
#from moqpcategory import *

from generalaward import *
BONUSCALLS = ['W0MA', 'K0GQ']
BONUSKEYS =  ['M', 'G']


"""
BonusAward - Bonus points for working the WILDCARD calls
"""
class BonusAward(GenAward):

    VERSION = '0.1.0'
    
    def __init__(self, qsolist=None):
       self.KEYS = BONUSCALLS
       self.Award = self.init_award(self.KEYS)
#       self.callset = BONUSCALLS
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)


    """
    Initializes and returns an award object with KEYS
    The returned object can hold up to three (3) calls
    that may be used for the KEY, along with the BAND,
    MODE and QTH for the associated QSO.
    """
    def init_award(self, KEYS):
        award = dict()
        for key in KEYS:
            award[key] = { 'INLOG': False,
                           'BAND': None,
                           'MODE': None,
                           'QTH': None, 
                           'WC': False}
        return award

    def parseLog(self, qsolist,
                       KEYS = None,
                       Award = None): 
        if (KEYS == None): KEYS = self.KEYS
        if (Award == None): Award = self.Award 
        for key in KEYS:
            if ( self.IsBonus(key, Award) == False ):
                for qso in qsolist:
                    if( qso['URCALL'] == key ):
                        Award[key]['BAND'] = \
                                    self.getBand(qso['FREQ'])
                        Award[key]['MODE'] = qso['MODE']
                        Award[key]['QTH'] = qso['URQTH']
                        Award[key]['INLOG'] = True
                        break
        return Award
    
    def IsBonus(self, key, Award = None):
        if (Award == None): Award = self.Award 
        return Award[key]['INLOG']
        
    def getNextUnused(self, KEYS = None, Award = None):
        if (KEYS == None): KEYS = self.KEYS
        if (Award == None): Award = self.Award 
        retkey =''
        for key in KEYS:
            if (Award[key]['INLOG']):
                if (Award[key]['WC'] == False):
                    retkey = key
                    break
        return retkey
        
    def getBonusList(self, KEYS = None, Award = None):
        if (KEYS == None): KEYS = self.KEYS
        if (Award == None): Award = self.Award 
        bonusList = []
        for key in KEYS:
            if (Award[key]['INLOG']):
                bonusList.append(key)
        return bonusList

    def appMain(self, qsolist):
        self.Award = self.parseLog(qsolist)
        return self.Award
