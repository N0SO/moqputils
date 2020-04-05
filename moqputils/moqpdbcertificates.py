#!/usr/bin/env python3

from moqpcertificates import MOQPCertificates
from moqpdbutils import MOQPDBUtils
from moqpdbconfig import *
from moqpmults import MOQPMults
from bothawards import BothAwards


class MOQPDBCertificates(MOQPCertificates):

    def __init__(self, call = None):
        if (call):
            self.appMain(call)

    def processLogdict(self, callsign):
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
       log = self.getLogFile(callsign)
       if ( log ):
          qsosummary = self.processQSOList(log['QSOLIST'])
          logSummary = dict()
          logSummary['HEADER'] = log['HEADER']
          logSummary['QSOLIST'] = log['QSOLIST']
          logSummary['ERRORS'] = log['ERRORS']
          logSummary['QSOSUM'] = qsosummary
          logSummary['MULTS'] = log['MULTS']
          
       return logSummary

    def getLogFile(self, callsign):
        log = None
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()
        mults = MOQPMults()
        #Fetch log header
        header = mydb.fetchCABHeader(callsign)
        #print(header)
        qsos = mydb.fetchValidQSOS(callsign)

        for qso in qsos:
            mults.setMult(qso['URQTH'])
        #print('mults = %d'%(mults.sumMults()))
        log = dict()
        log['HEADER'] = header
        log['QSOLIST'] = qsos
        log['MULTS'] = mults.sumMults()
        log['ERRORS'] = []
        return log
 
    def parseLog(self, callsign, Headers=True):
       """
       This method processes a single file passed in filename
       If the Headers option is false, it will skip printing the
       csv header info.
    
       Using dictionary objects
       """
       fullSummary = None
       logsummary = self.processLogdict(callsign)
       #print('parseLog: parsing errors: \n%s'%(logsummary['ERRORS'] ))
       #print(logsummary)
       if (logsummary):
          moqpcat = self.determineMOQPCatdict(logsummary)
          #print(moqpcat)
          Score = self.calculate_score(logsummary['QSOSUM'], logsummary['MULTS'])
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MULTS'] = logsummary['MULTS']
          fullSummary['SCORE'] = Score
          fullSummary['MOQPCAT'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          fullSummary['ERRORS'] = logsummary['ERRORS']
       else:
          print('No log in database for call %s.'%(filename))
       return fullSummary

    def scoreLog(self, call, HEADER=False):
        #print(call)
        tsvdata=None
        log = self.parseLog(call)
        #print('log=%s'%(log))
        if log:
            tsvdata = ''
            if (log['ERRORS'] == []):
                bawards = BothAwards()
                result = (bawards.appMain(\
                           log['HEADER']['CALLSIGN'],
                           log['QSOLIST']))
                #print(result)
                if (HEADER):
                   tsvdata += 'STATION\tSHOWME AWARD\tS\tH\t O\tW\tM\tE\tWC\t' \
                      'MISSOURI AWARD\tM\tI\tS\tS\t O\tU\tR\tI\tWC\t' \
                      'W0MA BONUS\tK0GQ BONUS'
                tsvdata += ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
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
        return tsvdata

    def appMain(self, call):
       csvdata = 'Nothing.'
       if (call == 'allcalls'):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           loglist = mydb.read_query( \
              "SELECT ID, CALLSIGN FROM logheader WHERE 1")
           HEADER = True
           for nextlog in loglist:
               #print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.scoreLog(nextlog['CALLSIGN'], HEADER)
               HEADER=False     
               print(csvdata)
       else:
           csvdata = self.scoreLog(call)
           print(csvdata)
