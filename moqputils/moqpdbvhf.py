#!/usr/bin/env python3
"""
moqpdbcategory  - Same features as moqpdbcategory, except read only
                  VHF QSOs for the compare

                  The main dfference from the moqpcategory class 
                  is all of the file read/write methods have been
                  over ridden by same name methods that read
                  data from and SQL database and update records
                  in the same database SUMMARY table.
                  
                  QSO Validation (QSL, time check, etc) should
                  already have been performed on the data.
                
                  Based on 2019 MOQP Rules
Update History:
* Thu Feb 13 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

from moqpdbcategory import *
from moqpdbutils import *
from bonusaward import BonusAward

VERSION = '0.0.1' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\t' + \
                'VHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0RGQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\n' +\

class MOQPDBVhf(MOQPDBCategory):
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsvfile(self, callsign, Headers=True):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
    
       If the Headers option is false, it will skip printing the
       csv header info.
       """
       csvdata = None
       log = self.parseLog(callsign)
       """
       print (log.keys())
       print(log['QSOSUM'].keys())
       print(log['MULTS'])
       print(log['MOQPCAT']['MOQPCAT'])
       """
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
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY']))
           #csvdata += ('%s\t'%(log['QSOSUM']['CW']))
           #csvdata += ('%s\t'%(log['QSOSUM']['PH']))
           #csvdata += ('%s\t'%(log['QSOSUM']['DG']))
           #csvdata += ('%s\t'%(log['QSOSUM']['QSOS']))
           csvdata += ('%s\t'%(log['QSOSUM']['VHF']))
           csvdata += ('%s\t'%(log['MULTS']))         
           csvdata += ('%s\t'%(log['SCORE']['SCORE']))         
           csvdata += ('%s\t'%(log['SCORE']['W0MA']))         
           csvdata += ('%s\t'%(log['SCORE']['K0GQ']))         
           csvdata += ('%s\t'%(log['SCORE']['CABFILE']))         
           csvdata += ('%s\t'%(log['SCORE']['TOTAL']))         
           #csvdata += ('%s\t'%(log['MOQPCAT']['MOQPCAT']))
           #csvdata += ('%s\t'%(log['MOQPCAT']['DIGITAL']))
           #csvdata += ('%s\t'%(log['MOQPCAT']['VHF']))
           #csvdata += ('%s'%(log['MOQPCAT']['ROOKIE']))

           for err in log['ERRORS']:
               if ( err != [] ):
                   csvdata += err
       
       else:
          csvdata = None

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
          ba=BonusAward(logsummary['QSOLIST'])
          if (ba.Award['W0MA']['INLOG']):
              w0mabonus = 100
          else:
              w0mabonus = 0
          if (ba.Award['K0GQ']['INLOG']):
              k0gqbonus = 100
          else:
              k0gqbonus = 0
          cabBonus = logsummary['HEADER']['CABBONUS']
          qsoScore = self.calculate_score(logsummary['QSOSUM'], logsummary['MULTS'])
          bonuspoints = { 'W0MA':w0mabonus,
                          'K0GQ':k0gqbonus,
                          'CABFILE':cabBonus,
                          'SCORE':qsoScore,
                          'TOTAL':(qsoScore + w0mabonus + k0gqbonus + cabBonus) }
          
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MULTS'] = logsummary['MULTS']
          fullSummary['SCORE'] = bonuspoints
          fullSummary['MOQPCAT'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          fullSummary['ERRORS'] = logsummary['ERRORS']
          #mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
          #mydb.setCursorDict()
          #mydb.writeSummary(fullSummary)
       else:
          print('No log in database for call %s.'%(filename))
       return fullSummary

    def getLogFile(self, callsign):
        log = None
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()
        mults = MOQPMults()
        #Fetch log header
        logID = mydb.CallinLogDB(callsign)
        if (logID):
            log=dict()
            dbheader = mydb.read_query( \
                "SELECT * FROM `logheader` WHERE ID=%d"%(logID))
            header = self.getLogHeader(dbheader)
            #print(header)
            #get digital QSOS only!
            qsos = mydb.read_query("SELECT * FROM QSOS WHERE ( (LOGID=%s) AND (VALID=1) AND FREQ>=50000 )"%(logID))
            for qso in qsos:
                mults.setMult(qso['URQTH'])
            #print('mults = %d'%(mults.sumMults()))
            log['HEADER'] = header
            log['QSOLIST'] = qsos
            log['MULTS'] = mults.sumMults()
            log['ERRORS'] = []
        return log


    def appMain(self, callsign):
       csvdata = 'Nothing.'
       if (callsign == 'allcalls'):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           loglist = mydb.read_query( \
              "SELECT ID, CALLSIGN FROM logheader WHERE 1")
           Headers = True
           for nextlog in loglist:
               #print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.exportcsvfile(nextlog['CALLSIGN'], Headers)        
               Headers = False
               if (csvdata):
                   print(csvdata)
       else:
           csvdata = self.exportcsvfile(callsign)
           print(csvdata)
