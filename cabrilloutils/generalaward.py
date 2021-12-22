#!/usr/bin/python

#import os
#from moqpcategory import *

VERSION = '0.2.1'

"""
GenAward - Generic award class
    Generally not called by itself, but is used as a
    code base for other awards like the MOQP
    SHOWME and MISSOURI awards.
    Those classes would inherit this class.
"""
class GenAward():

    def __init__(self):
        pass
        
    def _get_version(self):
       return VERSION
       
       
    """
    Initializes and returns an award object with KEYS
    The returned object can hold up to three (3) calls
    that may be used for the KEY, along with the BAND,
    MODE and QTH for the associated QSO.
    """
    def init_award(self, KEYS):
        award = dict()
        for key in KEYS:
            award[key] = dict()
            for i in range(3):
                 award[key][i] = dict()
                 award[key][i]['CALL'] = None
                 award[key][i]['BAND'] = None 
                 award[key][i]['MODE'] = None 
                 award[key][i]['QTH'] = None 
        return award

    def combineLists(self, list1, list2):
       retlist = []
       for i in list1:
           retlist.append(i)
       for i in list2:
           retlist.append(i)
       return retlist
       
    def combineListoflists(self, listofLists):
       retlist = []
       for lst in listofLists:
           for e in lst:
               retlist.append(e)
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

    """
    Check to see if a callsign found in sourceElement is needed
    in targetElement to qualify for an award.
    sourceElement is s list of up to 3 callsigns (string format).
    targetElement is a single callsign (also string format).
    If the targetElement = None, one of three callsign from 
    sourceElement[0 to 2] may be needed. This method
    will return the sourceElement index [0 to 2] to the first
    callsign in the list that is not None.
    
    The caller is responsible for copying the data from
    sourceElement[i] to targetElement, then setting 
    sourceElement[i] = None
    """
    def parseSingleKey(self, call, AKey, qsolist):
        #print(self.Award[AKey][0])
        if (self.Award[AKey][0]['CALL'] == None):
            qcount = len(qsolist[call])
            for i in range(qcount):
                #print(i, qsolist[call][i])
                if (qsolist[call][i]['USED'] == False): 
                    self.Award[AKey][0]['CALL'] = call
                    self.Award[AKey][0]['BAND'] = qsolist[call][i]['BAND']
                    self.Award[AKey][0]['MODE'] = qsolist[call][i]['MODE']
                    self.Award[AKey][0]['QTH'] = qsolist[call][i]['QTH']
                    qsolist[call][i]['USED'] = 'True'
                    #print('Needed %s for %s: BAND:%s, MODE:%s, QTH:%s'%(call, AKey, 
                                              #self.Award[AKey][0]['BAND'],
                                              #self.Award[AKey][0]['MODE'],
                                              #self.Award[AKey][0]['QTH']))
                    break
        return qsolist
              
    """
    Does this log qualify for the award?
    """
    def qualify(self, match, wildcard):
        qualify = False
        if (wildcard):
            wcreturn = wildcard
        else:
            wcreturn = ''
        stats = self.getStats()
        if (stats['COUNT'] == match):
            qualify = True
            wcreturn = ''
        elif ( (stats['COUNT'] == (match - 1)) and 
               (wildcard != "") ): # Change this from != None to fix issue #33
            qualify = True
            wcreturn = wildcard
        return { 'QUALIFY': qualify,
                 'COUNT': stats['COUNT'],
                 'CALLS': stats['CALLS'],
                 'WILDCARD': wcreturn }

    def showReport(self, match, wildcard, awardName, callsign):
        Returndata = []
        stats = self.qualify(match, wildcard)
#        print('Stats from showReport:\n%s'%(stats))
        if (stats['QUALIFY'] == True):
           str = 'QUALIFIES '
        else:
           str = 'DOES NOT QUALIFY '
        Returndata.append('%s %s for the %s award.' \
                                    %(callsign, str, awardName))
        
        str = 'Stations worked:\n'
        for k in stats['CALLS'].keys():
            str += ('%s = %s\n'%(k[0], stats['CALLS'][k]))
        Returndata.append(str)
        
        Returndata.append('WILDCARD: '+stats['WILDCARD'])
        
        return Returndata

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
       
    def getBand(self, freq):
       band = None
       nfreq = float(freq)
       
       if (nfreq >= 1800.0 and nfreq <= 2000.0):
           band = '160M'
       elif (nfreq >= 3500.0 and nfreq <= 4000.0):
           band = '80M'
       elif (nfreq >= 7000.0 and nfreq <= 7300.0):
           band = '40M'
       elif (nfreq >= 14000.0 and nfreq <= 14350.0):
           band = '20M'
       elif (nfreq >= 21000.0 and nfreq <= 214500.0):
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
       
    """
    Collect all 1x1 QSOS in qsolist and
    return a list of dict object with:
    {'CALL': {0: {'BAND': '20M', 'MODE': 'CW', 'QTH': 'GAS', 'USED': False}, 
              1: {'BAND': '20M', 'MODE': 'CW', 'QTH': 'GAS', 'USED': False}, 
              2: {'BAND': '80M', 'MODE': 'CW', 'QTH': 'GAS', 'USED': False},
              .
              .
              .
              N: {'BAND': '80M', 'MODE': 'CW', 'QTH': 'GAS', 'USED': False}},
    
    { CALL :  {1: {BAND, MODE, URQTH},
               . 
               . 
               . 
               {N: {BAND, MODE, QTH} }}
       .
       .
       .          
    """
    def collect1x1qsos(self, qsolist, callList):
        qsos = dict()

        for call in callList:
            qsos[call] = dict()
            qindex = 0
            for thisqso in qsolist:
                if (call == thisqso['URCALL']):
                    nextq = dict()
                    nextq['BAND'] = self.getBand(thisqso['FREQ'])
                    nextq['MODE'] = thisqso['MODE']
                    nextq['QTH'] = thisqso['URQTH']
                    nextq['USED'] = False
                    # DUP check
                    dup = False
                    for dc in range(len(qsos[call])):
                        if ( (nextq['BAND'] == qsos[call][dc]['BAND']) and
                             (nextq['MODE'] == qsos[call][dc]['MODE']) and
                             (nextq['QTH'] == qsos[call][dc]['QTH']) ):
                            dup = True
                    if ( dup == False ):
                        #print ('DUPE!')
                        qsos[call][qindex] = nextq
                        qindex += 1

        return qsos
        
    def show1x1QSOs(self, qsolist):
        textData =[]
        qkeys = qsolist.keys()
        #print('qkeys = %s'%(qkeys))
        for qkey in qsolist:
            if (len(qsolist[qkey])):
                qcount = len(qsolist[qkey])
                for i in range(qcount):
                   print('%s(%d): %s'%(qkey,i,qsolist[qkey][i]))

        

if __name__ == '__main__':
   app = GenAward()
   print('Class GenAward V%s'%(app._get_version()))
