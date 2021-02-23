#!/usr/bin/env python3
"""
Update History:
* Wed Feb 16 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Consolidated code from moqplogcheck, moqpcategory
-          in an attempt to make common routines for log
-          evaluation.
"""

from cabrilloutils.qsoutils import QSOUtils
from moqputils.moqpmults import *
from moqputils.moqpdefs import *


class MOQPQSOUtils(QSOUtils):

    def __init__(self):
       self.VERSION='0.0.1'
       pass

    def getVersion(self):
       return self.VERSION

    def makeQSOdict(self):
       """
       Return an empty dictionary for Cabrillo QSO Data
       based on the QSOTAGS list above
       """
       qso = self.MakeEmptyDict(self.QSOTAGS, '')
       return qso

    def getQSOdict(self, qsodata):
       qutils = QSOUtils()
       qelements = 10
       qso = None
       qso_errors = []
       q_errors = []
       #qso_data = dict()
       temp = qsodata.replace(':','')
       qsoparts = temp.split(' ')
       qsolen = len(qsoparts)
       qso_elements_parsed=0
       qso = self.makeQSOdict()
       tagi = 0
       while (tagi < qelements):
           if (tagi == 2): 
               """
               qso elements 2 and 3 should be date/time
               """
               qsotimeobj = qutils.qsotimeOBJ(\
	                     self.packLine(qsoparts[2]),
                             self.packLine(qsoparts[3]))
               qso[self.QSOTAGS[tagi]] = qsotimeobj
               qso_elements_parsed += 2
               tagi += 1
           else: 
               qso[self.QSOTAGS[tagi]] = \
                   self.packLine(qsoparts[qso_elements_parsed])
               qso_elements_parsed += 1
               tagi += 1
           if (qso_elements_parsed >= qsolen):
               # No more elements to parse
               break
           #print(qso, tagi)
       #Validate QSO
       q_errors = self.qso_valid(qso)
       #print(qsodata, qso_elements_parsed, qsolen, qso)
       if ( (qso_elements_parsed != qelements) or len(q_errors) ):
          qso_errors.append(qsodata)
          if (qso_elements_parsed != qelements):
             qso_errors.append(\
              '\tQSO has %d elements, it should have %d.'\
                                                    %(qsolen, qelements))
          if (len(q_errors)):
              for i in range(len(q_errors)): 
                  qso_errors.append('\t%s'%(q_errors[i]))
       qso['NOTES'] = qso_errors
       return qso       

    def getQSOdata(self, logtext):
       thislog = dict()
       mults = MOQPMults()
       qsos = []
       errorData = []
       headerNotes =[]
       header = self.makeHEADERdict()
       linecount = 0
       errors = 0
       dupes = 0
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
                qsos.append(qso)
                #print(qso)
                #print('qso errors = %s'%(qso['ERRORS']))
                if (qso['NOTES'] == []):
                   #print(qso['DATA'])
                   mults.setMult(qso['URQTH'])
                else:
                   errorData.append( \
                      ('QSO BUSTED, log file line %d: '% \
                        (linecount)) )
                   for err in qso['NOTES']:
                      errorData.append(" %s"%(err))

             elif (cabkey in header):
                header[cabkey] += recdata
             else:
                errString =\
                 'CAB TAG ERROR, log file line %d: \"%s\"'% \
                                       (linecount, cabline)
                headerNotes.append(errString)
                errorData.append(errString)
          else:
            errString =\
              'CAB DATA BAD, log line %d: \"%s\" skipping'% \
                                               (linecount, 
                                                    cabline)
            headerNotes.append(errString)
            errorData.append(errString)
       # Done processing
       header['NOTES'] = headerNotes
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
                 #print('%s : %s'%(tag, thisqso[tag]))
                 badmodeline += (' %s'%(thisqso[tag]))
             print('UNDEFINED MODE: %s -- QSO data = %s'%(mode, badmodeline))
         else:
           summary['DUPES'] += 1
      return  summary

    def qso_valid(self, qso):
       #print(qso)
       errorData = []
       qsovalid = True
       valid_date_chars = set('0123456789/-')
       valid_call_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-')
       qutils = QSOUtils()
       if ( self.is_number(qso['FREQ']) ):
          if (qutils.getBand(qso['FREQ'])):
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
       if (qso['DATETIME']):
          if (qutils.validateQSOtime(qso['DATETIME'])):
             pass
          else:
             errorData.append(  (\
              'QSO DATE/TIME outside contest time period: %s'\
               %(qso['DATETIME'])))
       else:
          errorData.append('QSO DATE/TIME strings invalid!')
          qsovalid = False

       if all(char in valid_call_chars for char in qso['MYCALL']):
          pass
       else:
          errorData.append(  ('QSO MYCALL Parameter invalid: %s'%(qso['MYCALL'])) )
          qsovalid = False

       if ( self.is_number(qso['MYREPORT']) ):
          if ( \
               ( (len(qso['MYREPORT']) == 3) and (qso['MODE'] in MODES3) ) or \
               ( (len(qso['MYREPORT']) == 2) and (qso['MODE'] in MODES2) ) ):
              pass
          else:
              errorData.append( \
                'QSO MY SIG REPORT %s does not match MODE: %s'%\
                (qso['MYREPORT'],
                 qso['MODE']) )
              qsovalid = False
       else:
          errorData.append(  ('QSO MYREPORT Parameter invalid: %s'%(qso['MYREPORT'])) )
          qsovalid = False

       if ( (qso['MYQTH'].isalpha()) and (\
            (qso['MYQTH'] in MOCOUNTY) or \
               (qso['MYQTH'] in US) or \
               (qso['MYQTH'] in CANADA) or \
               (qso['MYQTH'] in DX) ) ): 
          pass
       else:
          errorData.append(  ('QSO MYQTH Parameter invalid: %s'%(qso['MYQTH'])) )
          qsovalid = False

       if all(char in valid_call_chars for char in qso['URCALL']):
          pass
       else:
          errorData.append(  ('QSO URCALL Parameter invalid: %s'%(qso['URCALL'])) )
          qsovalid = False

       if ( self.is_number(qso['URREPORT']) ):
          if ( \
               ( (len(qso['URREPORT']) == 3) and (qso['MODE'] in MODES3) ) or \
               ( (len(qso['URREPORT']) == 2) and (qso['MODE'] in MODES2) ) ):
              pass
          else:
              errorData.append( \
                'QSO UR SIG REPORT %s does not match MODE: %s'%\
                (qso['URREPORT'],
                 qso['MODE']) )
              qsovalid = False
       else:
          errorData.append(  ('QSO URREPORT Parameter invalid: %s'%(qso['URREPORT'])) )
          qsovalid = False

       if ( (qso['URQTH'].isalpha()) and (\
            (qso['URQTH'] in MOCOUNTY) or \
               (qso['URQTH'] in US) or \
               (qso['URQTH'] in CANADA) or \
               (qso['URQTH'] in DX) ) ): 
          pass
       else:
          errorData.append(  ('QSO URQTH Parameter invalid: %s'%(qso['URQTH'])) )
          qsovalid = False
          
       return errorData

    def calculate_score(self, qsosum, mults, bonus):
        if (bonus['W0MA']):
            w0mabonus = 100
        else:
            w0mabonus = 0
        if (bonus['K0GQ']):
            k0gqbonus = 100
        else:
            k0gqbonus = 0
        if (bonus['CABRILLO']):
            cab_bonus = 100
        else:
            cab_bonus = 0
        Score = 0
        cwpoints = qsosum['CW'] * 2
        digipoints = qsosum['DG'] * 2
        qsopoints = cwpoints + digipoints + qsosum['PH']
        Score = (qsopoints * mults)  + \
                           w0mabonus + \
                           k0gqbonus + \
                           cab_bonus
        return Score
        
    def getMOQPLog(self, fileName):
        logtext = None
        log = None
        logtext = self.readFile(fileName)
        if (self.IsThisACabFile(logtext)):
            if (logtext):
                log = self.getQSOdata(logtext)
                if (log):
                    log['RAWTEXT'] = logtext
        return log


if __name__ == '__main__':
    app = MOQPLoadLogs()
    print('Class MOQPLoadLogs() Version %s'%(app.getVersion))


