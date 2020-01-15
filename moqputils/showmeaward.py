#!/usr/bin/python

import os
from moqpcategory import *

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
WILDKEYS = 'MG'



VERSION = '0.1.2'

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
    def parseSingleKey(self, sourceElement, targetElement):
        retval = -1
        #print(sourceElement, targetElement)
        if (targetElement == None):
            for i in range(3):
                if (sourceElement[i]):
                    retval = i
                    break
        return retval
              
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
               (wildcard != None) ):
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
       elif (nfreq >= 14000.0 and nfreq <= 14300.0):
           band = '20M'
       elif (nfreq >= 21000.0 and nfreq <= 214500.0):
           band = '15M'
       elif (nfreq >= 28000.0 and nfreq <= 29700.0):
           band = '10M'
       elif (nfreq >= 50000.0 and nfreq <= 54000.0):
           band = '6M'
       elif (nfreq >= 144000.0 and nfreq <= 148000.0):
           band = '2M'
       elif (nfreq >= 420000.0 and nfreq <= 450000.0):
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
        
"""
ShowMeAward - Child class of GenAward class
              taylored for the 2019 MOQP SHOWME Award.
"""
class ShowMeAward(GenAward):

    def __init__(self, qsolist=None):
       self.KEYS = COMKEYS+SHOWMEKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = self.combineLists(SHOWMECALLS, COMMONCALLS)
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
                #print('Target = %s'%( self.Award[AKey][0]))
                if (self.Award[AKey][0]):
                    for i in range(qcount):
                        #print(i, qsolist[call][i])
                        if (qsolist[call][i]['USED'] == False): 
                            self.Award[AKey][0]['CALL'] = call
                            self.Award[AKey][0]['BAND'] = qsolist[call][i]['BAND']
                            self.Award[AKey][0]['MODE'] = qsolist[call][i]['MODE']
                            self.Award[AKey][0]['QTH'] = qsolist[call][i]['QTH']
                            qsolist[call][i]['USED'] = 'True'
       
        #print('Award = %s\nqsolist = %s'%(self.Award, qsolist))                    
        return qsolist

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
       self.KEYS = COMKEYS+MOKEYS
       self.Award = self.init_award(self.KEYS)
       self.callset = self.combineLists(MOCALLS, COMMONCALLS)
#       print('Keys = %s\nAward = %s\ncallset = %s'%(self.KEYS,
#                                                   self.Award, 
#                                                   self.callset))
       if (qsolist):
              self.appMain(qsolist)
       
    def getStats(self):
        Count = self.sumAward()
        calls = dict()
        for k in ['M','I0','S0','S1','O','U','R','I1']:
            i1 = k[0]
            i2 = 0
            if (len(k) == 2):
                i2 = 1
            if (self.Award[i1][i2]['CALL'] != None):
                calls[k] = self.Award[i1][i2]['CALL']
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

                
    def parseAward(self, qsolist):
        for call in self.callset:
            print('Checking %s'%(call))
            qcount = len(qsolist[call])
            if ( (call in qsolist) and (qcount) ):
                AKey = call[2]  # 3rd char of 1x1 call
                #Allow for two I and S chars for MISSOURI
                
                print('Target = %s'%( self.Award[AKey][0]))
                if (self.Award[AKey][0]):
                    for i in range(qcount):
                        print(i, qsolist[call][i])
                        if (qsolist[call][i]['USED'] == False): 
                            self.Award[AKey][0]['CALL'] = call
                            self.Award[AKey][0]['BAND'] = qsolist[call][i]['BAND']
                            self.Award[AKey][0]['MODE'] = qsolist[call][i]['MODE']
                            self.Award[AKey][0]['QTH'] = qsolist[call][i]['QTH']
                            qsolist[call][i]['USED'] = 'True'
       
        #print('Award = %s\nqsolist = %s'%(self.Award, qsolist))                    
        return qsolist

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
       if (qsolist):
              self.appMain(qsolist)


    def appMain(self, qsolist):
        Bingo = self.checkLog(qsolist)
#        print('MISSOURI AWARD = %s\nStats: %s'%(Bingo, 
#                                                  self.Award))
        return [Bingo,self.Award]

"""
BothAwards - Checks for:
             2019 MOQP SHOWME Award
             2019 MOQP MISSOURI Award
             2019 MOQP BONUS stations
"""
class BothAwards(GenAward):

    def __init__(self, callsign=None, qsolist=None):
        self._showmeAward_ = ShowMeAward()
        self._missouriAward_ = MissouriAward()
        self._bonusAward_ = BonusAward()
        self.KEYS = COMKEYS+SHOWMEKEYS+MOKEYS
        self.Award = self.init_award(self.KEYS)
        self.callset = self.combineListoflists( [SHOWMECALLS, 
                                                 COMMONCALLS,
                                                 MOCALLS ] )
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
       
    def show1x1QSOs(self, qsolist):
        textData =[]
        qkeys = qsolist.keys()
        #print('qkeys = %s'%(qkeys))
        for qkey in qsolist:
            if (len(qsolist[qkey])):
                qcount = len(qsolist[qkey])
                for i in range(qcount):
                   print('%s(%d): %s'%(qkey,i,qsolist[qkey][i]))

    def appMain(self, callsign, qsolist):
        callList = self.combineListoflists([COMMONCALLS,
                                            SHOWMECALLS,
                                            MOCALLS,
                                            WILDCARDS])
        #print('callList =%s'%(callList))
        qso1x1 = self.collect1x1qsos(qsolist, callList)
        
        #print(qso1x1)
        #self.show1x1QSOs(qso1x1)
        #Bingo = self.checkLog(qsolist)
        Bonus = BonusAward(qsolist)
        qso1x1 = self._showmeAward_.parseAward(qso1x1)
        #print(self._showmeAward_.Award)
        #self.show1x1QSOs(qso1x1)
        
        wildcard =''
        for call in WILDCARDS:
            if (call in qso1x1):
                if (len(qso1x1[call])>0):
                    if (qso1x1[call][0]['USED'] == False):
                        wildcard = call
                        qso1x1[call][0]['USED'] = True
                        break
        #self.show1x1QSOs(qso1x1)

        showmeStats = self._showmeAward_.qualify(SHOWMEMATCH, wildcard)
        #print(showmeStats)
#        showmeData = self._showmeAward_.showReport(SHOWMEMATCH,
#                                          Bonus.Award['M'][0],
#                                          'SHOWME','This Station')

        wildcard =''
        for call in WILDCARDS:
            if call in qso1x1:
                if (len(qso1x1[call])>0):
                    if(qso1x1[call][0]['USED'] == False):
                        wildcard = call
                        qso1x1[call][0]['USED'] = True
                        break

        qso1x1 = self._missouriAward_.parseAward(qso1x1)
        missouriStats = self._missouriAward_.qualify(MOMATCH, wildcard)
#        print(missouriStats)
#        missouriData = self._missouriAward_.showReport(SHOWMEMATCH,
#                                       Bonus.Award['M'][0],
#                                       'MISSOURI','This Station')
        """
        for line in showmeData:
            print(line)
        for line in missouriData:
            print(line)
        
        return [Bingo,self.Award]
        """
        return { 'SHOWME' : showmeStats,
                 'MO' : missouriStats,
                 'BONUS' : {'W0MA' : Bonus.Award['M'][0]['CALL'],
                            'K0GQ' : Bonus.Award['G'][0]['CALL']} }


"""
ShowMe - For command line operations. 
"""
class ShowMe(MOQPCategory):

    def __init__(self, pathname = None):
        if (pathname):
            self.appMain(pathname)
            
            
    def scoreFile(self, pathname, HEADER=False):
        log = self.parseLog(pathname)
        if log:
            if (log['ERRORS'] == []):
                bawards = BothAwards()
                result = (bawards.appMain(\
                           log['HEADER']['CALLSIGN'],
                           log['QSOLIST']))
                #print(result)
                if (HEADER):
                   print('STATION\tSHOWME AWARD\tS\tH\t O\tW\tM\tE\tWC\t' \
                      'MISSOURI AWARD\tM\tI\tS\tS\t O\tU\tR\tI\tWC\t' \
                      'W0MA BONUS\tK0GQ BONUS')
                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s' \
                        %(log['HEADER']['CALLSIGN'],
                          result['SHOWME']['QUALIFY'],
                          result['SHOWME']['CALLS']['S'],
                          result['SHOWME']['CALLS']['H'],
                          result['SHOWME']['CALLS']['O'],
                          result['SHOWME']['CALLS']['W'],
                          result['SHOWME']['CALLS']['M'],
                          result['SHOWME']['CALLS']['E'],
                          result['SHOWME']['WILDCARD'],
                          result['MO']['QUALIFY'],
                          result['MO']['CALLS']['M'],
                          result['MO']['CALLS']['I0'],
                          result['MO']['CALLS']['S0'],
                          result['MO']['CALLS']['S1'],
                          result['MO']['CALLS']['O'],
                          result['MO']['CALLS']['U'],
                          result['MO']['CALLS']['R'],
                          result['MO']['CALLS']['I1'],
                          result['MO']['WILDCARD'],
                          result['BONUS']['W0MA'],
                          result['BONUS']['K0GQ']))
                          
            else:
                print('log file %s has errors' \
				%(pathname))
        else:
            print(\
            'File %s does not exist or is not in CABRILLO Format'\
                %(pathname))

    def scoreFileList(self, pathname):
        for (dirName, subdirList, fileList) in os.walk(pathname, 
                                                   topdown=True):
           if (fileList != ''): 
               Headers = True
               for fileName in fileList:
                   fullPath = ('%s/%s'%(dirName, fileName))
                   self.scoreFile(fullPath, Headers)
                   if (Headers): Headers = False

    def appMain(self, pathname):
        #print('Input path: %s'%(pathname))
        if (os.path.isfile(pathname)):
            self.scoreFile(pathname)
        else:
            self.scoreFileList(pathname)

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
