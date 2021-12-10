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
* Wed May 27 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Updated logheader to LOGHEADER.
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Added method updateDB to add VHF/UHF scores to
- the database table VHF (or update entries if an
- entry for the station exists already.
"""

from moqputils.moqpdbcategory import *
from moqputils.moqpdbutils import *
from moqputils.bonusaward import BonusAward

VERSION = '0.2.0' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\t' + \
                'VHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\n'

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
          ba=BonusAward(logsummary['QSOLIST'])
          if (ba.Award['W0MA']['INLOG']):
              w0mabonus = 100
          else:
              w0mabonus = 0
          if (ba.Award['K0GQ']['INLOG']):
              k0gqbonus = 100
          else:
              k0gqbonus = 0
          if (logsummary['HEADER']['CABBONUS']):
              cabBonus = 100
          else:
              cabBonus = 0
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

          self.updateDB(logsummary['HEADER']['CALLSIGN'],
                        logsummary['QSOSUM']['VHF'],
                        logsummary['MULTS'],
                        bonuspoints['W0MA'],
                        bonuspoints['K0GQ'],
                        bonuspoints['TOTAL'])

       return fullSummary

    def updateDB(self, call, qsos, mults, bonus1, bonus2, score):
        did = None
        db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        #logid = db.CallinLogDB(call)
        logid = db.read_pquery(\
            "SELECT ID FROM LOGHEADER WHERE CALLSIGN=%s",[call])
        if (logid): logid=logid[0]
        #print('Adding call %s, log ID %s, dig. qso count %d, mults %d'%(call, logid, qsos, mults))
        # Does record exist already?
        did = db.read_pquery("SELECT ID FROM VHF WHERE LOGID=%s",[logid])
        if (did):
            #update existing
            did = did[0]
            db.write_pquery(\
                "UPDATE VHF SET LOGID=%s,QSOS=%s,MULTS=%s, "+\
                "W0MABONUS=%s,K0GQBONUS=%s,SCORE=%s WHERE ID=%s",
                [logid,qsos,mults,bonus1,bonus2,score,did])
        else:
            #insert new
            did=db.write_pquery(\
                "INSERT INTO VHF "+\
                "(LOGID,QSOS,MULTS,W0MABONUS,K0GQBONUS,SCORE) "+\
                "VALUES (%s,%s,%s,%s,%s,%s)", 
                [logid,qsos,mults,bonus1,bonus2,score])
        return did

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
                "SELECT * FROM `LOGHEADER` WHERE ID=%d"%(logID))
            header = self.getLogHeader(dbheader)
            #print(header)
            #get digital QSOS only!
            #qsoqry = "SELECT * FROM QSOS WHERE LOGID=%s AND VALID=1"%(logID)
            qsoqry = "SELECT * FROM `QSOS` WHERE VALID=1 AND LOGID=%s AND (FREQ IN ('50','144','432') OR FREQ>=50000)"%(logID)
            #print(qsoqry)
            qsos = mydb.read_query(qsoqry)
            #print('qso count = %d, qsos:\n%s'%(len(qsos), qsos))
            if (len(qsos) >0):
                for qso in qsos:
                    mults.setMult(qso['URQTH'])
                #print('mults = %d'%(mults.sumMults()))
                log['HEADER'] = header
                log['QSOLIST'] = qsos
                log['MULTS'] = mults.sumMults()
                log['ERRORS'] = []
            else:
                log = None
        return log

    """
    def appMain(self, callsign):
       csvdata = 'Nothing.'
       if (callsign == 'allcalls'):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           loglist = mydb.read_query( \
              "SELECT ID, CALLSIGN FROM LOGHEADER WHERE 1")
           HEADER = True
           for nextlog in loglist:
               #print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.exportcsvfile(nextlog['CALLSIGN'], HEADER)        
               if (csvdata):
                   HEADER = False
                   print(csvdata)
       else:
           csvdata = self.exportcsvfile(callsign)
           print(csvdata)
    """

    def saveResults(self, mydb, vdata):
        dquery ='DROP TABLE IF EXISTS VHF;'
        dquery1 = 'CREATE TABLE VHF ('+\
          'ID int NOT NULL AUTO_INCREMENT, '+\
          'LOGID int NOT NULL, '+\
          'QSOS int NULL, '+\
          'CWQSO int NULL, '+\
          'PHQSO int NULL, '+\
          'RYQSO int NULL, '+\
          'MULTS int NULL, '+\
          'SCORE int NULL, '+\
          'PRIMARY KEY (ID));'
        mydb.write_query(dquery) # Delete old digital tables  
        mydb.write_query(dquery1) # Delete old digital tables  
        for entry in vdata:
            digid = mydb.write_pquery(\
               'INSERT INTO VHF '+\
               '(LOGID, QSOS, CWQSO, PHQSO, RYQSO, MULTS, SCORE) '+\
               'VALUES (%s, %s, %s, %s, %s, %s, %s)',
               [ entry['LOGID'], 
                 entry['QSOS'],
                 entry['CWQSO'],
                 entry['PHQSO'],
                 entry['RYQSO'],
                 entry['MULTS'],
                 entry['SCORE'] ])
            #print('Writing %d\n'%(digid))

    def appMain(self, callsign):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       vList = mydb.read_query(\
                 'SELECT * FROM SUMMARY WHERE VHF>0 ' +\
                 'ORDER BY VHFQSO DESC')
 
       #Score the digital list
       Vresult = []       
       for nextEnt in vList:
           qsoqry = \
             "SELECT * FROM `QSOS` WHERE LOGID=%s"%(nextEnt['LOGID'])
           qsoqry += " AND VALID=1 AND (FREQ IN ('50','144','432') OR FREQ>=50000)"
 
           entry = {'LOGID': nextEnt['LOGID'],
                    'QSOS': 0,
                    'CWQSO': 0,
                    'PHQSO': 0,
                    'RYQSO': 0,
                    'MULTS': 0,
                    'SCORE': 0 } 

           qsoList = mydb.read_query(qsoqry)

           #print(qsoList)
           if (len(qsoList)>0):
              for qso in qsoList:
                  if qso['MODE'] == 'CW': entry['CWQSO']+=1
                  if qso['MODE'] in MODES2: entry['PHQSO']+=1
                  if qso['MODE'] in MODES3: entry['RYQSO']+=1
              entry['QSOS'] = len(qsoList)
              vhfmults = MOQPMults(qsoList)
              entry['MULTS'] = vhfmults.sumMults()
              if (entry['MULTS'] == 0): entry['MULTS']=1
              entry['SCORE'] = ((((entry['CWQSO'] +
                                   entry['RYQSO']) * 2) +\
                                   entry['PHQSO']) *\
                                   entry['MULTS']) +\
                                   nextEnt['CABBONUS'] +\
                                   nextEnt['W0MABONUS'] +\
                                   nextEnt['K0GQBONUS']
              Vresult.append(entry)
       print(Vresult)
       self.saveResults(mydb, Vresult)
       print('%d Stations with VHF+ scores summarized database.'%(len(Vresult)))