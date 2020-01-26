#!/usr/bin/env python3
"""
moqpdbcategory  - Same features as moqpcategory, except read
                  all data froman SQL database. The main
                  difference rom the moqpcategory class is 
                  all of the file read/write methods have been
                  over ridden by same name methods that read
                  data from and SQL database and update recors
                  in the same database.
                  
                  QSO Validation (QSL, time check, etc) should
                  already have been performed on the data.
                
                  Based on 2019 MOQP Rules
Update History:
* Fri Jan 24 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

from moqpcategory import *
from moqpdbutils import *

VERSION = '0.0.1' 

class MOQPDBCategory(MOQPCategory):
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
           csvdata += ('%s\t'%(log['MULTS']))         
           csvdata += ('%s\t'%(log['SCORE']))         
           csvdata += ('%s\t'%(log['MOQPCAT']['MOQPCAT']))
           csvdata += ('%s\t'%(log['MOQPCAT']['DIGITAL']))
           csvdata += ('%s\t'%(log['MOQPCAT']['VHF']))
           csvdata += ('%s'%(log['MOQPCAT']['ROOKIE']))

           for err in log['ERRORS']:
               if ( err != [] ):
                   csvdata += err
       
       else:
          csvdata = ('No log data in databas for .'%callsign)
       print(csvdata)  
        
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
        logID = mydb.CallinLogDB(callsign)
        if (logID):
            log=dict()
            dbheader = mydb.read_query( \
                "SELECT * FROM `logheader` WHERE ID=%d"%(logID))
            header = self.getLogHeader(dbheader)
            #print(header)
            qsos = mydb.read_query("SELECT * FROM QSOS WHERE ( (LOGID=%s) AND (VALID=%s) )"%(logID, 1))
            for qso in qsos:
                mults.setMult(qso['URQTH'])
            #print('mults = %d'%(mults.sumMults()))
            log['HEADER'] = header
            log['QSOLIST'] = qsos
            log['MULTS'] = mults.sumMults()
            log['ERRORS'] = []
        return log

    def getLogHeader(self, dbheader):
        header = self.makeHEADERdict()
        header['START-OF-LOG'] = dbheader[0]['START']
        header['CALLSIGN'] = dbheader[0]['CALLSIGN']
        header['CREATED-BY'] = dbheader[0]['CREATEDBY']
        header['LOCATION'] = dbheader[0]['LOCATION']
        header['CONTEST'] = dbheader[0]['CONTEST']
        header['NAME'] = dbheader[0]['NAME']
        header['ADDRESS'] = dbheader[0]['ADDRESS']
        header['ADDRESS-CITY'] = dbheader[0]['CITY']
        header['ADDRESS-STATE-PROVINCE'] = dbheader[0]['STATEPROV']
        header['ADDRESS-POSTALCODE'] = dbheader[0]['ZIPCODE']
        header['ADDRESS-COUNTRY'] = dbheader[0]['COUNTRY']
        header['EMAIL'] = dbheader[0]['EMAIL']
        header['CATEGORY-ASSISTED'] = dbheader[0]['CATASSISTED']
        header['CATEGORY-BAND'] = dbheader[0]['CATBAND']
        header['CATEGORY-MODE'] = dbheader[0]['CATMODE']
        header['CATEGORY-OPERATOR'] = dbheader[0]['CATOPERATOR']
        header['CATEGORY-OVERLAY'] = dbheader[0]['CATOVERLAY']
        header['CATEGORY-POWER'] = dbheader[0]['CATPOWER']
        header['CATEGORY-STATION'] = dbheader[0]['CATSTATION']
        header['CATEGORY-TRANSMITTER'] = dbheader[0]['CATXMITTER']
        header['CATEGORY-TIME'] = ''
        header['CERTIFICATE'] = dbheader[0]['CERTIFICATE']
        header['OPERATORS'] = dbheader[0]['OPERATORS']
        header['CLAIMED-SCORE'] = dbheader[0]['CLAIMEDSCORE']
        header['CLUB'] = dbheader[0]['CLUB']
        header['IOTA-ISLAND-NAME'] = dbheader[0]['IOTAISLANDNAME']
        header['OFFTIME'] = dbheader[0]['OFFTIME']
        header['SOAPBOX'] = dbheader[0]['SOAPBOX']
        return header

    def appMain(self, callsign):
       csvdata = 'Nothing.'
       if (callsign == 'allcalls'):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           loglist = mydb.read_query( \
              "SELECT ID, CALLSIGN FROM logheader WHERE 1")
           for nextlog in loglist:
               print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.exportcsvfile(nextlog['CALLSIGN'])        
               print(csvdata)
       else:
           csvdata = self.exportcsvfile(callsign)
           print(csvdata)
