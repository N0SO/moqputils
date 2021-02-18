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
- V0.0.5 - Added Added option to move logs with errors to
- another folder.
* Sun May 10 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.6 - Added CABRILLO bonus processing and improved 
- error handling.
* Wed May 20 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.7 - Added QTH checks to qso_valid. Marked
- QSOs that fail checks as errors.
- Moved common definitions of counties, state, modes, etc.
- to moqpdefs.py. 
- Began consolidation of qso_valid code ( we had three 
- methods with that name).
* Tue Feb 16 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.8 - Made qso date / time a datetime object instead of
-          separate strings for date and time.
* Wed Feb 17 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.9 - Updated to use MOQPQSOUtils as parent cllass
"""

from cabrilloutils.CabrilloUtils import *
from moqputils.moqpqsoutils import MOQPQSOUtils
from moqputils.dupecheck import DUPECheck
from moqputils.bonusaward import BonusAward

import os, shutil

from moqputils.moqpdefs import *

class MOQPLogcheck(MOQPQSOUtils):

    QSOTAGS = ['FREQ', 'MODE', 'DATETIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH', 'NOTES']

    def __init__(self, filename = None, 
                       acceptedpath = None,
                       cabbonus = None):
        self.VERSION = '0.0.9'
        if (filename):
           if (filename):
              self.appMain(filename, acceptedpath, cabbonus)

    def getVersion(self):
       return self.VERSION

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
           if (log['BONUS']['CABRILLO']):
               cab_bonus = '100'
           else:
               cab_bonus = '0'        
           csvdata += ('%s\t'%(cab_bonus))         
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


    def checkLog(self, fileName, cabbonus=False):
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
                               'K0GQ':Bonus.Award['K0GQ']['INLOG'],
                               'CABRILLO' : cabbonus}
            log['MOQPCAT'] = self.determineMOQPCatdict(log)
            log['SCORE'] = self.calculate_score(log['QSOSUM'], 
                                                log['MULTS'],
                                                log['BONUS'])
            log['ERRORS'] = errors
        return log


    def processOneFile(self, filename, 
                             headers=True, 
                             acceptedMovePath=None,
                             cabbonus=False): 
       dupecount = None
       errorcount = None
       logAccepted = False              
       if (os.path.isfile(filename)):
          print(filename)
          log = self.checkLog(filename, cabbonus)
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

    def processFileList(self, pathname, 
                              acceptedPath=None,
                              cabbonus=False):
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
                                                   acceptedPath,
                                                   cabbonus)
                     csvdata += thislog
                     Headers = False
           else: 
              csvdata += ('True\tLog File %s does not exist\n'% \
                          (fileName))
        return csvdata

    def appMain(self, pathname, acceptedpath, cabbonus):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.processOneFile(pathname, 
                                        True, 
                                        acceptedpath,
                                        cabbonus)
       else:
          csvdata = self.processFileList(pathname, 
                                         acceptedpath,
                                         cabbonus)
       if (csvdata):
          print('%s'%(csvdata))
