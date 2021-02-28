#!/usr/bin/env python3
"""
moqpdbcategory  - Same features as moqpcategory, except read
                  all log header and QSO data from an SQL 
                  database. The data is printed for display
                  as just as the MOQPCategory data is, but
                  the resulting report is also written to the
                  SUMMARY table in the database.

                  The main dfference from the moqpcategory class 
                  is all of the file read/write methods have been
                  over ridden by same name methods that read
                  data from and SQL database and update records
                  in the same database SUMMARY table.
                  
                  QSO Validation (QSL, time check, etc) should
                  already have been performed on the data.
                
                  Based on 2019 MOQP Rules
Update History:
* Fri Jan 24 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Sat May 16 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Updates for 2020 MOQP changes
* Tue Feb 23 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 
- Starting Updates for 2021 MOQP changes.
"""

from moqputils.moqpcategory import *
from moqputils.moqpdbutils import *
from moqputils.bonusaward import BonusAward
from moqputils.configs.moqpdbconfig import *

VERSION = '0.1.0' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\t' + \
                'CW QSO\tPH QSO\tRY QSO\tQSO COUNT\tVHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0RGQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\t' +\
                'DIGITAL\tVHF\tROOKIE\n'

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
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY']))
           csvdata += ('%s\t'%(log['QSOSUM']['CW']))
           csvdata += ('%s\t'%(log['QSOSUM']['PH']))
           csvdata += ('%s\t'%(log['QSOSUM']['DG']))
           csvdata += ('%s\t'%(log['QSOSUM']['QSOS']))
           csvdata += ('%s\t'%(log['QSOSUM']['VHF']))
           csvdata += ('%s\t'%(log['MULTS']))         
           csvdata += ('%s\t'%(log['SCORE']['SCORE']))         
           csvdata += ('%s\t'%(log['SCORE']['W0MA']))         
           csvdata += ('%s\t'%(log['SCORE']['K0GQ']))         
           csvdata += ('%s\t'%(log['SCORE']['CABRILLO']))         
           csvdata += ('%s\t'%(log['SCORE']['TOTAL']))         
           csvdata += ('%s\t'%(log['MOQPCAT']['MOQPCAT']))
           csvdata += ('%s\t'%(log['MOQPCAT']['DIGITAL']))
           csvdata += ('%s\t'%(log['MOQPCAT']['VHF']))
           csvdata += ('%s'%(log['MOQPCAT']['ROOKIE']))

           for err in log['ERRORS']:
               if ( err != [] ):
                   csvdata += err
       
       else:
          csvdata = 'No log data in databas for %s.'%(callsign)
       return csvdata 
        
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
          ba=logsummary['BONUS']
          if (ba['W0MA']):
              w0mabonus = 100
          else:
              w0mabonus = 0
          if (ba['K0GQ']):
              k0gqbonus = 100
          else:
              k0gqbonus = 0
          if(ba['CABRILLO'] > 0):
              cabBonus = 100
          else:
              cabBonus = 0
          bonuspoints = { 'W0MA':w0mabonus,
                          'K0GQ':k0gqbonus,
                          'CABRILLO':cabBonus}
          
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MULTS'] = logsummary['MULTS']
          fullSummary['BONUS'] = bonuspoints
          fullSummary['MOQPCAT'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          fullSummary['ERRORS'] = logsummary['ERRORS']
          fullSummary['SCORE'] = dict()
          fullSummary['SCORE']['TOTAL'] = self.calculate_score(\
	                                  logsummary['QSOSUM'], 
                                          logsummary['MULTS'],
                                          bonuspoints)
          fullSummary['SCORE']['W0MA'] = bonuspoints['W0MA']
          fullSummary['SCORE']['K0GQ'] = bonuspoints['K0GQ']
          fullSummary['SCORE']['CABRILLO'] = bonuspoints['CABRILLO']
          fullSummary['SCORE']['SCORE'] = self.calculate_score(\
	                                  logsummary['QSOSUM'], 
                                          logsummary['MULTS'],
                                          {'W0MA': 0,
					   'K0GQ': 0,
					   'CABRILLO': 0})

          mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
          mydb.setCursorDict()
          mydb.writeSummary(fullSummary)
       else:
          print('No log in database for call %s.'%(callsign))
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
       logSummary = None
       """
       log = self.getLogFile(callsign)
       return log

    def getLogFile(self, callsign):
        log = None
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()
        #Fetch log header
        logID = mydb.CallinLogDB(callsign)
        if (logID):
            log=dict()
            dbheader = mydb.read_query( \
                "SELECT * FROM `LOGHEADER` WHERE ID=%d"%(logID))
            #print(dbheader)
            header = self.getLogHeader(dbheader)
            qsos = mydb.read_query("SELECT * FROM QSOS WHERE ( (LOGID=%s) AND (VALID=%s) )"%(logID, 1))
            mults = MOQPMults(qsos)
            Bonus = BonusAward(qsos)
            """
            for qso in qsos:
                mults.setMult(qso['URQTH'])
            """
            #print('mults = %d'%(mults.sumMults()))
            log['HEADER'] = header
            log['QSOLIST'] = qsos
            log['MULTS'] = mults.sumMults()
            log['BONUS'] = { 'W0MA': Bonus.Award['W0MA']['INLOG'],
                             'K0GQ':Bonus.Award['K0GQ']['INLOG'],
                             'CABRILLO' : header['CABBONUS']}
            log['QSOSUM'] = self.processQSOList(qsos)
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
        # Added to handle cabrillo file bonus status stored in logheaders table
        header['CABBONUS'] = dbheader[0]['CABBONUS']
        return header

    def appMain(self, callsign):
       csvdata = 'Nothing.'
       if (callsign == 'allcalls'):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           loglist = mydb.fetchLogList()
           #loglist = mydb.read_query( \
           #   "SELECT ID, CALLSIGN FROM logheader WHERE 1")
           Headers = True
           for nextlog in loglist:
               #print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.exportcsvfile(nextlog['CALLSIGN'], Headers)        
               Headers = False
               print(csvdata)
       else:
           csvdata = self.exportcsvfile(callsign)
           print(csvdata)
