#!/usr/bin/python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
Update History:
* Thu Dec 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.1 - Start tracking revs.               
"""
from logsummary import *
import os

VERSION = '0.2.2' 
FILELIST = './'
ARGS = None

INSTATE = 'MO MISSOURI'

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT'

STATIONS = 'FIXED MOBILE PORTABLE ROVER EXPEDITION HQ SCHOOL'

MODES = 'SSB USB LSB FM PH CW RTTY DIG MIXED'

OVERLAY = 'ROOKIE'

US = 'CT EMA ME NH RI VT WMA ENY NLI NNJ NNY SNJ WNY DE EPA MDC WPA '
US += 'AL GA KY NC NFL SC SFL WCF TN VA PR VI AR LA MS NM NTX OK STX '
US+= 'WTX EB LAX ORG SB SCV SDG SF SJV SV PAC AZ EWA ID MT NV OR UT '
US+= 'WWA WY AK MI OH WV IL IN WI CO IA KS MN NE ND SD CA '

DX = 'DX'

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\t' + \
                'CW QSO\tPH QSO\tRY QSO\tTOTAL\tVHF QSO\t' + \
                'MOQP CATEGORY\n'


class MOQPCategory(LogSummary):

    QSOTAGS = ['FREQ', 'MODE', 'DATE', 'TIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH']

    def __init__(self, filename = None):
        if (filename):
           if (filename):
              self.appMain(filename)

    def getVersion(self):
       return VERSION

    def getLogFile(self, filename):
        log = None
        fileText = self.readFile(filename)
        if (self.IsThisACabFile(fileText)):
            log = self.getQSOdata(fileText)
        return log

    def makeQSOdict(self):
       """
       Return an empty dictionary for Cabrillo QSO Data
       based on the QSOTAGS list above
       """
       qso = self.MakeEmptyDict(self.QSOTAGS, '')
       return qso

    def getQSOdict(self, qsodata):
       qso = None
       qso_errors = []
       qso_data = dict()
       temp = qsodata.replace(':','')
       qsoparts = temp.split(' ')
       #print(len(qsoparts))
       if (len(qsoparts) == 10):
          i=0
          qso = self.makeQSOdict()
          for tag in self.QSOTAGS:
             #print('qso[%s] = %s %d'%(tag, qsoparts[i], i))
             qso[tag] = qsoparts[i].strip()
             i += 1
          #print qso
          qso_errors = self.qso_valid(qso)
       else:
          qso_errors = ['QSO has %d elements, should have 10.'%(len(qsoparts))]
       qso_data['ERRORS'] = qso_errors
       qso_data['DATA'] = qso
       return qso_data       
       
    def getQSOdata(self, cabdata):
       thislog = dict()
       qsos = []
       errorData = []
       header = self.makeHEADERdict()
       linecount = 0
       for line in cabdata:
          linecount += 1
          cabline = self.packLine(line)
          #print('Raw CABDATA = %s'%(line))
          linesplit = cabline.split(':')
          lineparts = len(linesplit)
          #print('%d Split data items: %s'%(lineparts, linesplit))
          if (lineparts >= 2):
             cabkey = linesplit[0].strip()
             recdata = linesplit[1].strip()
             #print('cabkey =%s\nrecdata =%s\n'%(cabkey, recdata))
             if (lineparts > 2):
                tagpos = cabline.find(':')
                templine = cabline[tagpos:].replace(':','')
                recdata = templine.strip()
             if (cabkey == 'QSO'):
                qso = self.getQSOdict(recdata)
                #print('qso errors = %s'%(qso['ERRORS']))
                if (qso['ERRORS'] == []):
                   qsos.append(qso['DATA'])
                else:
                   errorData.append( \
                      ('QSO BUSTED, line %d: \"%s\" \n' \
                        '    %s\n'% \
                        (linecount, cabline, qso['ERRORS'])) )
             elif (cabkey in header):
                header[cabkey] += recdata
             else:
                errorData.append( \
                  ('CAB TAG unknown, line %d: \"%s\"\n'% \
                            (linecount, cabline)) )
          else:
            errorData.append( \
           ('CAB data bad, line %d: \"%s\" skipping'% \
                                               (linecount, cabline)) )
       thislog['HEADER'] = header
       thislog['QSOLIST'] = qsos
       thislog['ERRORS'] = errorData
       return thislog

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
       logSummary = None
       log = self.getLogFile(fname)
       if ( log ):
          qsosummary = self.processQSOList(log['QSOLIST'])
          logSummary = dict()
          logSummary['HEADER'] = log['HEADER']
          logSummary['QSOLIST'] = log['QSOLIST']
          logSummary['ERRORS'] = log['ERRORS']
          logSummary['QSOSUM'] = qsosummary
          
       return logSummary

    def _moqpcatloc_(self, log):
       moqpcatstg = None
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
       moqpcatstg = None
       compstring = log['HEADER']['CATEGORY-STATION'].strip()
       if (compstring in STATIONS):
           if (compstring == 'FIXED'):
               moqpcatstg = ' FIXED'
           elif ( (compstring == 'MOBILE') \
                     or (compstring == 'ROVER') \
                     or compstring == 'PORTABLE'):
               moqpcatstg = ' MOBILE'
           elif (compstring == 'EXPEDITION'):
               moqpcatstg = ' EXPEDITION'
           elif (compstring == 'SCHOOL'):
               moqpcatstg = 'SCHOOL'
       return moqpcatstg

    def _moqpcatop_(self, log):
       moqpcatstg = None
       compstring = log['HEADER']['CATEGORY-OPERATOR'].strip()
       if (compstring == 'SINGLE-OP'):
          moqpcatstg  = 'SINGLE-OP'
       elif (compstring == 'MULTI-OP'):
          moqpcatstg   = 'MULTI-OP'
       elif (compstring == 'CHECKLOG'):
          moqpcatstg   = 'CHECKLOG'
       return moqpcatstg

    def _moqpcatpower_(self, log):
       moqpcatstg = None
       compstring = log['HEADER']['CATEGORY-POWER'].strip()
       if (compstring == 'LOW' \
                 or compstring == 'HIGH' \
                 or compstring == 'QRP'):
           moqpcatstg  = ('%s POWER'%(compstring))
       return moqpcatstg
    
    def _moqpcatmode_(self, log):
       moqpcatstg = None
       compstring = log['HEADER']['CATEGORY-MODE'].strip()
       if (compstring == 'PH' \
                     or compstring == 'SSB'):
          moqpcatstg = 'PHONE'
       elif (compstring == 'CW'):
          moqpcatstg = 'CW'
       elif (compstring == 'MIXED'):
          moqpcatstg = 'MIXED'
       return moqpcatstg

    def _combine_moqpcat_parts(self, moqpcatstg, newstring):
       retstring = None
       if (newstring):
          retstring = ('%s %s'%(moqpcatstg, newstring))
       return retstring    

    def determineMOQPCatstg(self, log):
       moqpcatstg = self._moqpcatloc_(log)

       if (moqpcatstg):
          temp=self._moqpcatsta_(log)
          moqpcatstg = self._combine_moqpcat_parts(moqpcatstg, temp)

       if (moqpcatstg):
          temp=self._moqpcatop_(log)
          if temp == 'CHECKLOG':
             moqpcatstg = 'CHECKLOG'
          else:
             moqpcatstg = self._combine_moqpcat_parts(moqpcatstg, temp)
       
             if (moqpcatstg):
                temp=self._moqpcatpower_(log)
                moqpcatstg = self._combine_moqpcat_parts(moqpcatstg, temp)

             if (moqpcatstg):
                temp=self._moqpcatmode_(log)
                moqpcatstg = self._combine_moqpcat_parts(moqpcatstg, temp)

             if (moqpcatstg):
                if (log['QSOSUM']['DG'] > 0):
                    moqpcatstg += '+DG'
                if (log['QSOSUM']['VHF'] > 0):
                    moqpcatstg += '+VHF'
          
             if (moqpcatstg):
                if (log['HEADER']['CATEGORY-OVERLAY'].strip() == 'ROOKIE'):
                    moqpcatstg += ' ROOKIE'                         

       return moqpcatstg
       
    """
    This method processes a single log file passed in filename
    and returns the summary ino in .CSV format to be printed
    or saved to a .CSV file.
    
    If the Headers option is false, it will skip printing the
    csv header info.
    """
    def exportcsvfile(self, filename, Headers=True):
       csvdata = None
       log = self.parseLog(filename)
       if (log):
       
           if (Headers): 
               csvdata = COLUMNHEADERS
               
           else:
               csvdata = ''

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
           csvdata += ('%s\n'%(log['MOQPCAT']))

           for err in log['ERRORS']:
               if ( err != [] ):
                   csvdata += err
       
       else:
          csvdata = ('File %s does not exist or is not in CABRILLO format.'%filename)
       print(csvdata)  
        
    """
    This method processes a single file passed in filename
    If the Headers option is false, it will skip printing the
    csv header info.
    
    Using dictionary objects
    """
    def parseLog(self, filename, Headers=True):
       fullSummary = None
       logsummary = self.processLogdict(filename)
       #print( logsummary['ERRORS'] )
       if (logsummary):
          moqpcat = self.determineMOQPCatstg(logsummary)
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MOQPCAT'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          fullSummary['ERRORS'] = logsummary['ERRORS']
       else:
          print('File %s does not exist or is not in CABRILLO format.'%filename)
       return fullSummary
 
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
       
    def qso_valid(self, qso):
       errorData = []
       qsovalid = True
       valid_date_chars = set('0123456789/-')
       valid_call_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-')
       #if ( qso['FREQ'].isnumeric() ):
       if ( self.is_number(qso['FREQ']) ):
          pass
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

       if ( qso['TIME'].isnumeric() ):
          pass
       else:
          errorData.append(  ('QSO TIME Parameter invalid: %s'%(qso['TIME'])) )
          qsovalid = False

       #if ( qso['MYCALL'].isalnum() ):
       if all(char in valid_call_chars for char in qso['MYCALL']):
          pass
       else:
          errorData.append(  ('QSO MYCALL Parameter invalid: %s'%(qso['MYCALL'])) )
          qsovalid = False

       if ( qso['MYREPORT'].isnumeric() ):
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

       if ( qso['URREPORT'].isnumeric() ):
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
       
if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())


