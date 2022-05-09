#!/usr/bin/env python3
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
Update History:
* Thu Dec 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.1 - Start tracking revs.               
* Wed Jan 08 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.2 - Lots of tweaks while processing 2019 MOQP files:
- Added code to category processing to handle DIGITAL               
* Thu Jan 16 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.3 - Added frequency band verifiaction to qso_valid method.
* Fri Jan 24 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.0 - Copied method processQSOList from logsummay.py.
- This ended dependancy on logsummary in preparation for
- making a child class to read all QSO data from SQL database.
* Sat May 16 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.1 - Updates for 2020 MOQP changes
* Sat May 23 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.2 - Updated to use moqpdefs.py for state, county, country
- designations.
* Mon Feb 22 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.3
- Updated to use MOQPQSOUtils as parent cllass.
- Eliminated code duplicated in MOQPQSOUtils
* Tue Feb 23 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.4
- Moved the more up-to-date file processing code out of
- MOQPLogCheck to the parent class MOQPCategory for
- efficiency and consistancy:
-        processLogdict (now depricted)
-        checkLog()
-        headerReview()
-        errCopy()
-* Wed Feb 24 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.5
- Added call to checkEmail method.
* Fri Feb 26 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.6
- Added ERROR and NOTES keys to QSOTAGS
* Sat Feb 27 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.7
- Minor tweak to exportcsv so command line error 
- report is pretty.
* Wed Mar 03 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.3.8
- Added SHOWME and MISSOURI status to summary generated
- Rearranged columns to make the display read more logically
* Thu May 05 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0
- Incorporated new MOQPLogFile class to hold the logfile.

       
"""
from moqputils.moqplogfile import MOQPLogFile
from moqputils.bonusaward import BonusAward
from moqputils.bothawards import *
from moqputils.dupecheck import DUPECheck
from moqputils.moqpmults import *
from moqputils.moqpdefs import *
import os, re

VERSION = '1.0.0' 
FILELIST = './'
ARGS = None

class MOQPCategory(MOQPLogFile):
    """
    QSOTAGS = ['FREQ', 'MODE', 'DATETIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 
               'URQTH', 'ERROR', 'NOTES']
    """
    
    def __init__(self, filename = None, cabbonus=None):
        self.cabbonus=cabbonus
        self.filename = filename
        if (filename):
           if (filename):
              self.appMain(filename)

    def getVersion(self):
       return VERSION


    def getLogFile(self, filename):
        print('MOQPCategory:getLogFile')
        log = None
        fileText = self.readFile(filename)
        if (self.IsThisACabFile(fileText)):
            fileText = fileText.splitlines()
            log = self.getQSOdata(fileText)
        return log

    def processQSOList(self,  data):
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
      
      for thisqso in data:
      
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
                 badmodeline += (' %s'%(thisqso[tag]))
             print('UNDEFINED MODE: %s -- QSO data = %s'%(mode, badmodeline))

      return  summary

    def processLog(self, fname):
       category = None
       log = self.readFile(fname)
       if ( log ):
          if self.IsThisACabFile(log):
             headerdata = self.getCABHeader(log)
             catdata = self.getCategory(headerdata)
             category = self.determineCategory(catdata)
             qth = self.getCabArray('LOCATION:',headerdata)
             qcall, qops, qso, cw, ph, dg, vhf = self.processQSOs( log)
             category.append(qth)
             category.append(qcall)
             category.append(qops)
             category.append(cw)
             category.append(ph)
             category.append(dg)
             category.append(qso)
             category.append(vhf)
       
       return category      

       
    def processLogdict(self, fname):
       """
       Read the Cabrillo log file and separate log header data
       from qso data. 
       Returns a dictionary with four elements:
          HEADER = a dictionary objject of the log header
          QSOLIST = a list dictionary objects with QSO data
          ERRORS = A list of errors encountered while 
                   processing the log.
          QSOSUM = a summary of the QSO statstics
                   QSOS = total number of QSOs
                   CW = number of CW QSOs
                   PH = number of PHONE QSOSs
                   DG = number of DIGITAL QSOs
                   VHF = number of VHF (>=144MHz) QSOs
       """
       print('*** Method MOQPCategory.processLogdict is '+\
             'depricated and should be replaced with a '+\
             'call to MOPQCategory.checkLog.')
       logSummary = None
       log = self.getLogFile(fname)
       if ( log ):
          qsosummary = self.processQSOList(log['QSOLIST'])
          logSummary = dict()
          logSummary['HEADER'] = log['HEADER']
          logSummary['QSOLIST'] = log['QSOLIST']
          logSummary['ERRORS'] = log['ERRORS']
          logSummary['QSOSUM'] = qsosummary
          logSummary['MULTS'] = log['MULTS']
          
       return logSummary

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

    """
    This method processes a single log file passed in filename
    and returns the summary ino in .CSV format to be printed
    or saved to a .CSV file.
    
    If the Headers option is false, it will skip printing the
    csv header info.
    """
    def exportcsvfile(self, filename, Headers=True):
       csvdata = None
       log = self.checkLog(filename, self.cabbonus)
       csvdata = self.exportcsv(log, Headers)
       if csvdata == None :
          csvdata = ('File %s does not exist or is not in CABRILLO format.'%filename)
       return csvdata
       
    def exportcsv(self, log, Headers):
       csvdata = None
       if (log):
           """
           print(log['QSOSUM'])
           print(log['BONUS'])
           print(log['MULTS'], log['SCORE'])
           print(log.keys())
           """
           if (Headers): 
               csvdata = COLUMNHEADERS
               
           else:
               csvdata = ''
               
           errcount = 0
           for q in log['QSOLIST']:
               if q['ERROR']: errcount +=1
           """			   
           errcount = len(log['ERRORS'])
           """
           qsoscore = (((log['QSOSUM']['CW'] + log['QSOSUM']['DG']) * 2) +\
                        log['QSOSUM']['PH']) * log['MULTS']
                        
           csvdata += '%d\t'%(errcount)
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
           csvdata += ('%s\t'%(log['QSOSUM']['VHF']))
           csvdata += ('%s\t'%(log['QSOSUM']['QSOS']))
           csvdata += ('%s\t'%(log['MULTS']))
           #csvdata += '%d\t'%(qsoscore)
           csvdata += '%s\t'%(log['BONUS']['W0MA'])   
           csvdata += '%s\t'%(log['BONUS']['K0GQ'])   
           csvdata += '%s\t'%(log['BONUS']['CABRILLO'])   
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += '%d\t'%(log['QSOSUM']['DUPES'])        
           csvdata += '%s\t'%(log['BONUS']['SHOWME'])   
           csvdata += '%s\t'%(log['BONUS']['MISSOURI'])   
           csvdata += ('%s\t'%(log['MOQPCAT']['MOQPCAT']))
           csvdata += ('%s\t'%(log['MOQPCAT']['DIGITAL']))
           csvdata += ('%s\t'%(log['MOQPCAT']['VHF']))
           csvdata += ('%s\t'%(log['MOQPCAT']['ROOKIE']))
           
           errstring =''
           if len(log['ERRORS'])> 0 :
               """
               Changed for better error report formating
               csvdata += 'LOG ERRORS:\n'
               for err in log['ERRORS']:
                   csvdata += '%s\n'%(err)
               """
               errstring = self.packNote(log['ERRORS'])
               if (len(errstring) > 4096):
                   tempstg = 'TOO MANY ERRORS TO LIST ALL - ' +\
                   'SEE THE RAW LOG FILE; ' + errstring[:4096]
                   errstring=tempstg
           csvdata += '%s\n'%(errstring)
       #print(csvdata)  
       return csvdata
        
    """
    This method processes all files in the passed in pathname
    """
    def exportcsvflist(self, pathname):
       csvdata = COLUMNHEADERS
       for (dirName, subdirList, fileList) in os.walk(pathname, topdown=True):
          if (fileList != ''): 
             Headers = True
             for fileName in fileList:
                fullPath = ('%s/%s'%(dirName, fileName))
                result = self.exportcsvfile(fullPath, Headers)
                if (result):
                    csvdata += result
                Headers = False
       return csvdata
       
    def errorCopy(self, target, destination):
        if(len(target)>0):
            for item in target:
               destination.append(item)
        return destination
    
    """
    This method processes a single file passed in filename
    If the cabbonus parameter is present it will us used to
    add the CABRILLO FILE bonus to the score
    
    Returns a dictionary objct.
    """
    def checkLog(self, fileName, cabbonus=False):
        result = dict()
        errors = []
        log = self.buildLog(fileName)
        if ( log ):
            headerStatus = self.headerReview(log['HEADER'])
            #result['HEADERSTAT'] = headerResult['STAT']

            """
            for qso in log['QSOLIST']:
                print(qso)
            """
            #get valid qsos
            validqsos = self.getValidQSOs()
            #get invalid qsos
            invalidqsos = self.getValidQSOs(witherrors=True)
            if (validqsos):
                sortedGood = self.sortQSOdictList(validqsos)
                if (sortedGood):
                    dupes = DUPECheck(sortedGood)
                    if (dupes.newlist):
                        #add back the original invalid qsos if any
                        newlist = dupes.newlist
                        if (invalidqsos):
                            for q in invalidqsos:
                                newlist.append(q)
                        #put list back in original order
                        log['QSOLIST'] = self.sortQSOdictList(newlist,
                                                         sortKey='QID')
                        validqsos = self.getValidQSOs(log['QSOLIST'])

                
            if(validqsos):
                Bonus = BonusAward(validqsos)
            
                mults = MOQPMults(validqsos)
                log['MULTS'] = mults.sumMults()
            
                ShowmeMo = BothAwards(log['HEADER']['CALLSIGN'],
                                                        validqsos)
                ShowMe = Missouri = False
                if ShowmeMo.Results:
                    if ShowmeMo.Results['SHOWME']['QUALIFY'] :
                        ShowMe = True
                    if ShowmeMo.Results['MO']['QUALIFY'] :
                        Missouri = True
                      
                qsosummary = self.sumQSOList(log['QSOLIST'])
            else: # Not a valid log file
                headerStatus['STAT'] = False
                headerStatus['ERRORS'] = ['Unable to process Cabrillo log header.']
                print('No valid QSOs for {}'.format(fileName))
                # Set things that got skipped because no valid qsos.
                Bonus = BonusAward()
                Bonus.Award['W0MA']['INLOG']=False
                Bonus.Award['K0GQ']['INLOG']=False

                log['MULTS'] = 0
                qsosummary = { 'QSOS':0,
                               'CW': 0,
                               'PH': 0,
                               'VHF': 0,
                               'DG':0,
                               'DUPES':0,
                               'INVALID':0 }
                ShowMe = Missouri = False
         
            log['QSOSUM'] = qsosummary
            
            log['HEADERSTAT']= headerStatus

            log['BONUS'] = {   'W0MA': Bonus.Award['W0MA']['INLOG'],
                               'K0GQ':Bonus.Award['K0GQ']['INLOG'],
                               'CABRILLO' : cabbonus,
                               'SHOWME': ShowMe,                    
                               'MISSOURI': Missouri }
            log['MOQPCAT'] = self.determineMOQPCatdict(log)
            log['SCORE'] = self.calculate_score(log['QSOSUM'], 
                                                log['MULTS'],
                                                log['BONUS'])
            """
            Build log error summary
            """
            qcount = 1
            lerrors =[]
            for qso in log['QSOLIST']:
                if (qso['ERROR'] or len(qso['NOTES']) > 0):
                    qline = self.showQSO(qso)
                    qerrors = self.buildQSOerrSum(qso, qso['QID'])                          
                    if (qerrors):
                        lerrors = self.errorCopy(qerrors, lerrors)
                qcount += 1
            # Add any log header errors
            if ( (headerStatus['STAT'] == False) or 
                        (len(headerStatus['ERRORS']) > 0) ):
                lerrors.append('LOG HEADER WARNINGS/ERRORS: ')
                for l in headerStatus['ERRORS']:
                    lerrors.append('\t {}'.format(l))
            log['ERRORS'] = lerrors
        return log

    def qsolist_valid(self, qsolist):
       qcount = 0
       errorData = []
       for qso in qsolist:
           qcount += 1
           qsoerrors = self.qso_valid(qso)
           if (qsoerrors):
              r = [qcount, qsoerrors]
              errorData.append(r)
       return errorData

    def appMain(self, pathname):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.exportcsvfile(pathname)
       else:
          csvdata = self.exportcsvflist(pathname)
       print(csvdata)
       
    def buildQSOerrSum(self, qso, qcount = None):
        elist = None
        if (qso['ERROR'] or len(qso['NOTES']) > 0):
            qline = self.showQSO(qso)
            elist = []
            if (qcount):
                elist.append('QSO LINE {}:'.format(qcount))
                addTab = '\t '
            else:
                addTab = ''
                
            elist.append('{} {}'.format(addTab, qline))
            if (qso['DUPE'] > 0):
                elist.append('{}DUPE of QSO {}'.format(\
                                                addTab,
                                                qso['DUPE']))
                                                
            if (len(qso['NOTES'])>0):
                for eline in qso['NOTES']:
                    elist.append('{} {}'.format(addTab, eline))
        return elist
       
if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())


