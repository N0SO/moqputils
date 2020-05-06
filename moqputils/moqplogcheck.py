#!/usr/bin/env python3
"""
MOQPLogcheck  - Check logs submitted for the ARRL Missouri
QSO Party and determine if the file will load correctly into
the MOQP SQL database. Look for the following:
    1. Verify the file is a CABRILLO file.
    2. Look for the following CABRILLO header tags:
        A) CALLSIGN: is populated.
        B) EMAIL: is populated.
        C) LOCATION: is populated and valid.
        D) The CATEGORY- fields have enough info
           to determine the MOQP category:
                i) - STATION:
               ii) - OPERATOR:
              iii) - POWER:
               iv) - MODE:
    3. Review QSO: lines and verify:
         A) QSO Date / time fall within contest times.
         B) FREQUENCY / BAND is in-band.
         C) MYCALL matches CALLSIGN:
         D) MYREPORT is valid
         E) MYQTH matches LOCATION:
                i) - 3 char county code for MO stations
               ii) - State, Provinance or DX for non-MO
         F) URCALL is populated.
         G) URREPORT is valid
         H) URQTH is a 3 char county code, state, prov or DX.
    4. DUPE checks.
    5. Determine contacts with BONUS stations.
    6. Summarize QSOS and compute perliminary score.
    7. Determine SHOWME and MISSOURI certificate status.

Update History:
* Tue Apr 14 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
- Same basic funtion as moqpcategory.py
* Thu Apr 16 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Added enhanced log header verification.
- Steps 1 & 2 above.
* Thu Apr 17 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3 - Added DUPE and BONUS checks.
* Mon Apr 27 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.4 - Added ERROR flags for sorting of files with errors.
* Mon Apr 29 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.5 - Added Added option tp move logs with errors to
- another folder.
"""

from CabrilloUtils import *
from moqpmults import *
from generalaward import GenAward
from dupecheck import DUPECheck
from bonusaward import BonusAward
import os, shutil

INSTATE = ['MO', 'MISSOURI']

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT'

#STATIONS = 'FIXED MOBILE PORTABLE ROVER EXPEDITION HQ SCHOOL'
STATIONS = ['FIXED', 'MOBILE','PORTABLE', 'ROVER','EXPEDITION',
            'HQ','SCHOOL']

MODES = 'SSB USB LSB FM PH CW RY RTTY DIG DIGI MIXED'

OVERLAY = 'ROOKIE'

US = 'CT EMA ME NH RI VT WMA ENY NLI NNJ NNY SNJ WNY DE EPA MDC WPA '
US += 'AL GA KY NC NFL SC SFL WCF TN VA PR VI AR LA MS NM NTX OK STX '
US+= 'WTX EB LAX ORG SB SCV SDG SF SJV SV PAC AZ EWA ID MT NV OR UT '
US+= 'WWA WY AK MI OH WV IL IN WI CO IA KS MN NE ND SD CA '

DX = 'DX DK2 DL8 HA8 ON4'

COLUMNHEADERS = 'LOG ERRORS\tCALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\t' + \
                'CW QSO\tPH QSO\tRY QSO\tTOTAL\tVHF QSO\t' + \
                'MULTS\tDUPES\tW0MA\tK0GQ\tSCORE\t' + \
                'MOQP CATEGORY\tDIGITAL\tVHF\tROOKIE\n'


VERSION = '0.0.5'

class MOQPLogcheck(CabrilloUtils):

    QSOTAGS = ['FREQ', 'MODE', 'DATE', 'TIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH']

    def __init__(self, filename = None, acceptedpath = None):
        if (filename):
           if (filename):
              self.appMain(filename, acceptedpath)

    def getVersion(self):
       return VERSION

    def validateQSOtime(self, qso):
        qsoutils = DUPECheck()
        timeValid = False
        day1Start = qsoutils.qsotimeOBJ('2020-04-04', '1400')
        day1Stop = qsoutils.qsotimeOBJ('2020-04-05', '0400')
        day2Start = qsoutils.qsotimeOBJ('2020-04-05', '1400')
        day2Stop = qsoutils.qsotimeOBJ('2020-04-05', '2000')
        logtime = qsoutils.qsotimeOBJ(qso['DATE'], qso['TIME'])
        if (logtime):
           if ( ((logtime >= day1Start) and \
                 (logtime <= day1Stop)) \
              or \
              ((logtime >= day2Start) and \
               (logtime <= day2Stop)) ):
                timeValid = True
        return timeValid
    
    def makeQSOdict(self):
       """
       Return an empty dictionary for Cabrillo QSO Data
       based on the QSOTAGS list above
       """
       qso = self.MakeEmptyDict(self.QSOTAGS, '')
       return qso

    def qso_valid(self, qso):
       errorData = []
       qsovalid = True
       valid_date_chars = set('0123456789/-')
       valid_call_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-')
       genaward = GenAward()
       #if ( qso['FREQ'].isnumeric() ):
       if ( self.is_number(qso['FREQ']) ):
          if (genaward.getBand(qso['FREQ'])):
              pass
          else:
              errorData.append( \
              ('QSO FREQ Parameter out of band: %s'%(qso['FREQ'])) )
       else:
          errorData.append( ('QSO FREQ Parameter invalid: %s'%(qso['FREQ'])) )
          qsovalid = False
       
       if ( qso['MODE'] in self.MODES ):
          pass
       else:
          errorData.append(  ('QSO MODE Parameter invalid: %s'%(qso['MODE'])) )
          qsovalid = False
       if all(char in valid_date_chars for char in qso['DATE']):
          pass
       else:
          errorData.append(  ('QSO DATE Parameter invalid: %s'%(qso['DATE'])) )
          qsovalid = False
          qso['DATE'] = None
       if ( qso['TIME'].isnumeric() ):
          pass
       else:
          errorData.append(  ('QSO TIME Parameter invalid: %s'%(qso['TIME'])) )
          qsovalid = False
          qso['TIME'] = None
       if ( qso['DATE'] and qso['TIME'] ):
          if (self.validateQSOtime(qso)):
             pass
          else:
             errorData.append(  (\
              'QSO DATE/TIME outside contest time period: %s %s'\
               %(qso['DATE'],
                 qso['TIME'])) )
       #if ( qso['MYCALL'].isalnum() ):
       if all(char in valid_call_chars for char in qso['MYCALL']):
          pass
       else:
          errorData.append(  ('QSO MYCALL Parameter invalid: %s'%(qso['MYCALL'])) )
          qsovalid = False

       #if ( qso['MYREPORT'].isnumeric() ):
       if ( self.is_number(qso['MYREPORT']) ):
          pass
       else:
          errorData.append(  ('QSO MYREPORT Parameter invalid: %s'%(qso['MYREPORT'])) )
          qsovalid = False

       if ( qso['MYQTH'].isalpha() ):
          pass
       else:
          errorData.append(  ('QSO MYQTH Parameter invalid: %s'%(qso['MYQTH'])) )
          qsovalid = False

       #if ( qso['URCALL'].isalnum() ):
       if all(char in valid_call_chars for char in qso['URCALL']):
          pass
       else:
          errorData.append(  ('QSO URCALL Parameter invalid: %s'%(qso['URCALL'])) )
          qsovalid = False

#       if ( qso['URREPORT'].isnumeric() ):
       if ( self.is_number(qso['URREPORT']) ):
          pass
       else:
          errorData.append(  ('QSO URREPORT Parameter invalid: %s'%(qso['URREPORT'])) )
          qsovalid = False

       if ( qso['URQTH'].isalpha() ):
          pass
       else:
          errorData.append(  ('QSO URQTH Parameter invalid: %s'%(qso['URQTH'])) )
          qsovalid = False
          
       return errorData

    def getQSOdict(self, qsodata):
       qso = None
       qso_errors = []
       qso_data = dict()
       temp = qsodata.replace(':','')
       qsoparts = temp.split(' ')
       #print(len(qsoparts))
       if (len(qsoparts) >= 10):
          i=0
          qso = self.makeQSOdict()
          for tag in self.QSOTAGS:
             #print('qso[%s] = %s %d'%(tag, qsoparts[i], i))
             qso[tag] = self.packLine(qsoparts[i])
             i += 1
          #print qso
          qso_errors = self.qso_valid(qso)
       else:
          qso_errors = ['QSO has %d elements, should have at least 10.'%(len(qsoparts))]
       qso_data['ERRORS'] = qso_errors
       qso_data['DATA'] = qso
       return qso_data       

    def getQSOdata(self, logtext):
       thislog = dict()
       mults = MOQPMults()
       qsos = []
       errorData = []
       header = self.makeHEADERdict()
       linecount = 0
       for line in logtext:
          linecount += 1
          line = line.upper()
          cabline = self.packLine(line)
          #print('Raw CABDATA = %s'%(line))
          linesplit = cabline.split(':')
          lineparts = len(linesplit)
          #print('%d Split data items: %s'%(lineparts, linesplit))
          if (lineparts >= 2):
             cabkey = self.packLine(linesplit[0])
             recdata = self.packLine(linesplit[1])
             #print('cabkey =%s\nrecdata =%s\n'%(cabkey, recdata))
             if (lineparts > 2):
                tagpos = cabline.find(':')
                templine = cabline[tagpos:].replace(':','')
                recdata = self.packLine(templine)
             if (cabkey == 'QSO'):
                qso = self.getQSOdict(recdata)
                #print('qso errors = %s'%(qso['ERRORS']))
                if (qso['ERRORS'] == []):
                   #print(qso['DATA'])
                   qsos.append(qso['DATA'])
                   mults.setMult(qso['DATA']['URQTH'])
                else:
                   errorData.append( \
                      ('QSO BUSTED, line %d: \"%s\" '% \
                        (linecount, cabline)) )
                   for err in qso['ERRORS']:
                      errorData.append(" %s"%(err))

             elif (cabkey in header):
                header[cabkey] += recdata
             else:
                errorData.append( \
                  ('CAB TAG unknown, line %d: \"%s\"'% \
                            (linecount, cabline)) )
          else:
            errorData.append( \
           ('CAB data bad, line %d: \"%s\" skipping'% \
                                               (linecount, 
                                                  cabline)) )
       thislog['HEADER'] = header
       thislog['QSOLIST'] = qsos
       thislog['MULTS'] = mults.sumMults()
       thislog['ERRORS'] = errorData
       #print(thislog['MULTS'], mults.sumMults())
       return thislog

    def sumQSOList(self,  data):
      """
      Process and return summary data from a list of
      QSO dictionary objects.
      """
      summary = dict()
      summary['QSOS'] = 0
      summary['CW'] = 0
      summary['PH'] = 0
      summary['VHF'] = 0
      summary['DG'] = 0
      summary['DUPES'] = 0
      
      for thisqso in data:
         if (thisqso['DUPE'] == 0):
      
           summary['QSOS'] += 1
                        
           try:
             tfreq = thisqso['FREQ']
             freq = float(tfreq)
           except:
             freq = 0.0
           if ((freq >= 50000.0) or (tfreq in self.VHFFREQ) ):
             summary['VHF'] += 1
                                   
           mode = thisqso['MODE'].upper()
           if ('CW' in mode):
             summary['CW'] += 1
           elif (mode in self.PHONEMODES):
             summary['PH'] += 1
           elif (mode in self.DIGIMODES):
             summary['DG'] += 1
           else:
             badmodeline = ('QSO:')
             for tag in self.QSOTAGS:
                 badmodeline += (' %s'%(data[tag]))
             print('UNDEFINED MODE: %s -- QSO data = %s'%(mode, badmodeline))
         else:
           summary['DUPES'] += 1
      return  summary

    def calculate_score(self, qsosum, mults, bonus):
        if (bonus['W0MA']):
            w0mabonus = 100
        else:
            w0mabonus = 0
        if (bonus['K0GQ']):
            k0gqbonus = 100
        else:
            k0gqbonus = 0
        Score = 0
        cwpoints = qsosum['CW'] * 2
        digipoints = qsosum['DG'] * 2
        qsopoints = cwpoints + digipoints + qsosum['PH']
        Score = (qsopoints * mults)  + w0mabonus + k0gqbonus
        return Score

    def _moqpcatloc_(self, log):
       moqpcatstg = ''
       compstring = log['HEADER']['LOCATION'].strip()
       if(compstring in INSTATE):
          moqpcatstg = 'MISSOURI'
       elif (compstring in US):
          moqpcatstg = 'US'
       elif (compstring in CANADA):
          moqpcatstg = ('CANADA: (%s)'%(log['HEADER']['LOCATION']))
       elif (compstring in DX):
          moqpcatstg = 'DX'          
       return moqpcatstg

    def _moqpcatsta_(self, log):
       moqpcatstg = ''
       compstring = log['HEADER']['CATEGORY-STATION'].strip()
       if (compstring in STATIONS):
           if (compstring == 'FIXED'):
               moqpcatstg = 'FIXED'
           elif ( (compstring == 'MOBILE') \
                     or (compstring == 'ROVER') \
                     or compstring == 'PORTABLE'):
               moqpcatstg = 'MOBILE'
           elif (compstring == 'EXPEDITION'):
               moqpcatstg = 'EXPEDITION'
           elif (compstring == 'SCHOOL'):
               moqpcatstg = 'SCHOOL'
       return moqpcatstg

    def _moqpcatop_(self, log):
       moqpcatstg = ''
       compstring = log['HEADER']['CATEGORY-OPERATOR'].strip()
       if (compstring == 'SINGLE-OP'):
          moqpcatstg  = 'SINGLE-OP'
       elif (compstring == 'MULTI-OP'):
          moqpcatstg   = 'MULTI-OP'
       elif (compstring == 'CHECKLOG'):
          moqpcatstg   = 'CHECKLOG'
       return moqpcatstg

    def _moqpcatpower_(self, log):
       moqpcatstg = ''
       compstring = log['HEADER']['CATEGORY-POWER'].strip()
       if (compstring == 'LOW' \
                 or compstring == 'HIGH' \
                 or compstring == 'QRP'):
           moqpcatstg  = ('%s POWER'%(compstring))
       return moqpcatstg
    
    def _moqpcatmode_(self, log):
       moqpcatstg = ''
       compstring = log['HEADER']['CATEGORY-MODE'].strip()
       if (compstring == 'PH' \
                     or compstring == 'SSB'):
          moqpcatstg = 'PHONE'
       elif (compstring == 'CW'):
          moqpcatstg = 'CW'
       elif (compstring == 'MIXED'):
          moqpcatstg = 'MIXED'
       elif (compstring == 'RY' or \
             compstring =='RTTY' or \
             compstring == 'DIG' or \
             compstring == 'DIGI'):
          moqpcatstg = 'DIGITAL'
       return moqpcatstg

    def determineMOQPCatstg(self, moqpcat):
       moqpcatstg = 'UNKNOWN'
       if (moqpcat['OPERATOR'] =='CHECKLOG'):
           moqpcatstg = 'CHECKLOG'
           
       elif (moqpcat['LOCATION'] == 'DX'):
           moqpcatstg = 'DX'
       
       elif (moqpcat['STATION'] == 'SCHOOL'):
           moqpcatstg = ('%s %s'%(moqpcat['LOCATION'], 
                                  moqpcat['STATION']))

       elif ('CANADA' in moqpcat['LOCATION']):
           moqpcatstg = 'CANADA'

       elif (moqpcat['LOCATION'] == 'US'):
           moqpcatstg = ('%s %s'%(moqpcat['LOCATION'],
                                   moqpcat['OPERATOR']))
           if (moqpcat['OPERATOR'] == 'MULTI-OP'):
               pass
           elif (moqpcat['OPERATOR'] == 'SINGLE-OP'):
               moqpcatstg += (' %s'%(moqpcat['POWER']))
 
       elif (moqpcat['LOCATION'] == 'MISSOURI'):
           moqpcatstg = ('%s %s %s'%(moqpcat['LOCATION'],
                                     moqpcat['STATION'],
                                     moqpcat['OPERATOR']))
                                     
           if (moqpcat['STATION'] == 'FIXED'):
               if(moqpcat['OPERATOR'] == 'MULTI-OP'):
                   pass
               elif (moqpcat['OPERATOR'] == 'SINGLE-OP'):
                   moqpcatstg += (' %s'%(moqpcat['POWER']))
                             
           elif (moqpcat['STATION'] == 'EXPEDITION'):
               if(moqpcat['OPERATOR'] == 'MULTI-OP'):
                   pass
               elif (moqpcat['OPERATOR'] == 'SINGLE-OP'):
                   moqpcatstg += (' %s'%(moqpcat['POWER']))

           elif (moqpcat['STATION'] == 'MOBILE'):
               moqpcatstg = ('%s %s'%(moqpcat['LOCATION'],
                                    moqpcat['STATION']))
               if (moqpcat['POWER'] == 'HIGH POWER'):
                   moqpcatstg += ' UNLIMITED'
               else:
                   moqpcatstg += (' %s'%(moqpcat['OPERATOR']))
                   if (moqpcat['OPERATOR'] == 'MULTI-OP'):
                       pass
                   elif (moqpcat['OPERATOR'] == 'SINGLE-OP'):
                       moqpcatstg += (' %s %s'% (moqpcat['POWER'],
                                                 moqpcat['MODE']))
                                     
       return moqpcatstg
       
    def determineMOQPCatdict(self, log):
       moqpcatdict = { 'LOCATION':'',
                       'STATION':'',
                       'OPERATOR':'',
                       'POWER':'',
                       'MODE':'',
                       'ROOKIE':'',
                       'VHF':'',
                       'DIGITAL':'',
                       'MOQPCAT':''}

       moqpcatdict['LOCATION'] = self._moqpcatloc_(log)
          
       moqpcatdict['STATION']=self._moqpcatsta_(log)
       
       moqpcatdict['OPERATOR']=self._moqpcatop_(log)

       moqpcatdict['POWER']=self._moqpcatpower_(log)

       moqpcatdict['MODE']=self._moqpcatmode_(log)

       if (log['QSOSUM']['DG'] > 0):
           moqpcatdict['DIGITAL'] = 'DIGITAL'
           
       if (log['QSOSUM']['VHF'] > 0):
           moqpcatdict['VHF'] = 'VHF'
          
       if (log['HEADER']['CATEGORY-OVERLAY'].upper().strip() == 'ROOKIE'):
           moqpcatdict['ROOKIE'] = 'ROOKIE'                         
       moqpcatdict['MOQPCAT'] = self.determineMOQPCatstg(moqpcatdict)
       #print(moqpcatdict)         
       return moqpcatdict

    def exportcsv(self, log, Headers=True):
       #print(Headers)
       if (log):
       
           if (Headers): 
               csvdata = COLUMNHEADERS
               
           else:
               csvdata = ''

           if (log['ERRORS'] != []):
               csvdata += 'True'
           csvdata += '\t'
           csvdata += ('%s\t'%(log['HEADER']['CALLSIGN']))
           csvdata += ('%s\t'%(log['HEADER']['OPERATORS']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-STATION']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OPERATOR']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-POWER']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-MODE']))
           csvdata += ('%s\t'%(log['HEADER']['LOCATION']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY']))
           csvdata += ('%s\t'%(log['QSOSUM']['CW']))
           csvdata += ('%s\t'%(log['QSOSUM']['PH']))
           csvdata += ('%s\t'%(log['QSOSUM']['DG']))
           csvdata += ('%s\t'%(log['QSOSUM']['QSOS']))
           csvdata += ('%s\t'%(log['QSOSUM']['VHF']))
           csvdata += ('%s\t'%(log['MULTS'])) 
           csvdata += ('%s\t'%(log['QSOSUM']['DUPES'])) 
           if (log['BONUS']['W0MA']):
               w0mabonus = '100'
           else:
               w0mabonus = '0'        
           csvdata += ('%s\t'%(w0mabonus))         
           if (log['BONUS']['K0GQ']):
               k0gqbonus = '100'
           else:
               k0gqbonus = '0'        
           csvdata += ('%s\t'%(k0gqbonus))         
           csvdata += ('%s\t'%(log['SCORE']))         
           csvdata += ('%s\t'%(log['MOQPCAT']['MOQPCAT']))
           csvdata += ('%s\t'%(log['MOQPCAT']['DIGITAL']))
           csvdata += ('%s\t'%(log['MOQPCAT']['VHF']))
           csvdata += ('%s\n'%(log['MOQPCAT']['ROOKIE']))

           if (log['ERRORS'] != []):
               for err in log['ERRORS']:
                   csvdata += ('ERROR LINE\t%s\n'%(err))
       else:
          csvdata = None
       return csvdata
       

    def headerReview(self, header):
        errors =[]
        goodHeader = True
        if ('START-OF-LOG' in header):
            tag = self.packLine(header['LOCATION'])
            if (\
                (tag in INSTATE) or
                (tag in US) or
                (tag in CANADA) or
                (tag in DX) ):
                pass
            else:
                errors.append('LOCATION: %s tag INVALID'% \
                            (header['LOCATION']))
                goodKey = False
            if (\
                (header['CATEGORY-STATION']) and
                (header['CATEGORY-OPERATOR']) and
                (header['CATEGORY-POWER']) and
                (header['CATEGORY-MODE']) ):
                pass
            else:
                #Missing some CATEHORY data
                errors.append(\
                    'CATEGORY-xxx: tags may be incomplete')
                goodKey = False
            if (header['CALLSIGN'] == ''):
                 errors.append('CALLSIGN: %s tag INVALID'% \
                            (header['CALLSIGN']))
                 goodHeader = False
            if (header['EMAIL'] == ''):
                 errors.append('EMAIL: %s tag INVALID'% \
                            (header['EMAIL']))
                 goodHeader = False
        else:
            #Not a CAB Header object
            errors.append('No valid CAB Header')
            goodHeader = False

        result = { 'STAT' : goodHeader,
                   'ERRORS' : errors }
        return result

    def errorCopy(self, target, destination):
        if(len(target)>0):
            for item in target:
               destination.append(item)
        return destination

    def getMOQPLog(self, fileName):
        logtext = None
        log = None
        logtext = self.readFile(fileName)
        if (self.IsThisACabFile(logtext)):
            if (logtext):
                log = self.getQSOdata(logtext)
        return log


    def checkLog(self, fileName):
        result = dict()
        log = self.getMOQPLog(fileName)
        if ( log ):
            errors = log['ERRORS']
            headerResult = self.headerReview(log['HEADER'])
            errors = self.errorCopy(headerResult['ERRORS'], 
                                                     errors)
            result['HEADERSTAT'] = headerResult['STAT']
            dupes = DUPECheck(log['QSOLIST'])
            #print(dupes.newlist)
            if (dupes.newlist):
                qcount = 1
                for qso in dupes.newlist:
                    if (qso['DUPE'] == 0):
                      pass
                    else:
                      errors.append('QSO %d DUPE of QSO %s'% \
                                  (qcount, dupes.showQSO(qso)))
                    qcount += 1
                
                log['QSOLIST'] = dupes.newlist
            
            Bonus = BonusAward(log['QSOLIST'])
                      
            qsosummary = self.sumQSOList(log['QSOLIST'])
            
            #print(qsosummary)

            log['QSOSUM'] = qsosummary

            log['BONUS'] = { 'W0MA': Bonus.Award['W0MA']['INLOG'],
                               'K0GQ':Bonus.Award['K0GQ']['INLOG']}
            log['MOQPCAT'] = self.determineMOQPCatdict(log)
            log['SCORE'] = self.calculate_score(log['QSOSUM'], 
                                                log['MULTS'],
                                                log['BONUS'])
            log['ERRORS'] = errors
        return log


    def processOneFile(self, filename, headers=True, acceptedMovePath=None): 
       dupecount = None
       errorcount = None
       logAccepted = False              
       if (os.path.isfile(filename)):
          log = self.checkLog(filename)
          if (log):
             call = log['HEADER']['CALLSIGN']
             dupecount = log['QSOSUM']['DUPES']
             errorcount = len(log['ERRORS'])
             #print("errorcount = %d, DUPE count = %d, PATH = %s"%(errorcount, dupecount, acceptedMovePath))
             if (errorcount == dupecount): logAccepted = True
             csvdata = self.exportcsv(log, headers)
             if (csvdata == None):
                csvdata = ('True\tFile %s is not in MOQP Cabrillo format Dude.\n'\
                         %(filename))
          else:
             csvdata = ('True\tFile %s is not in MOQP Cabrillo format.\n'\
                         %(filename))
       else:
          csvdata = ('True\tLog File %s does not exist\n'% \
                          (filename))
       if (logAccepted and acceptedMovePath): 
          if (os.path.exists(acceptedMovePath)):
              # Move to accepted logs folder 
              try:
                 dest = shutil.move(filename, acceptedMovePath)
                 print('mv %s %s'%(filename, acceptedMovePath))
              except Exception as e:
                 print('Move of %s to %s failed\n%s!'% \
                                             (filename,
                                              acceptedMovePath,
                                              e.args))

       return csvdata 
    """   
    def moveLogwithErrs(self, thislog, filename, errormovepath):
       moved = False
       if (errormovepath):
           lines = thislog.splitlines()
           #print(len(lines), lines)
           if(len(lines) > 1):
               if (lines[0].startswith('LOG ERROR')):
                   index = 1
               else:
                   index = 0
           else:
               index = 0
           #print(lines[index])
           if (lines[index].startswith('True')):
               print('Moving file %s to %s'% \
               (filename, errormovepath))
               try:
                   dest = shutil.move(filename, errormovepath)
                   moved = True
               except:
                   print('Move of %s to %s failed!'% \
                                              (filename,
                                               errormovepath))
       return moved 
    """
    def processFileList(self, pathname, acceptedPath=None):
        csvdata = ''
        for (dirName, subdirList, fileList) in  \
                      os.walk(pathname, topdown=True):
           if (fileList != ''): 
              Headers = True
              for fileName in fileList:
                 if (fileName.startswith('.')):
                     pass
                 else:
                     fullPath = ('%s/%s'%(dirName, fileName))
                     thislog = self.processOneFile(fullPath, 
                                                   Headers,
                                                   acceptedPath)
                     csvdata += thislog
                     """
                     moved = self.moveLogwithErrs(thislog,
                                                  fullPath,
                                                  errcopypath)
                     """
                     Headers = False
                     #if moved: break
           else: 
              csvdata += ('True\tLog File %s does not exist\n'% \
                          (fileName))
        return csvdata

    def appMain(self, pathname, acceptedpath):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.processOneFile(pathname, 
                                        True, 
                                        acceptedpath)
       else:
          csvdata = self.processFileList(pathname, acceptedpath)
       if (csvdata):
          print('%s'%(csvdata))
