#!/usr/bin/env python3
"""
moqpdbvhf       - Same features as moqpdbcategory, except read only
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
* Thu Dec 09 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.0 - Refactored Code
- Much of the code replaced was holdover from the file
- processing version, which inefficiently recalculated
- a number of things already available in the LOGHEADER,
- SUMMARY, and QSO tables. Code reworked to:
-    1. Use the VHF field in SUMMARY to determine LOGIDs
-       that contain VHF QSOs.
-    2. Select only QSOs  for the log being scored based
-       on the FREQ field in the QSO table. 
-    3. Count total number of VHF QSOs, also CW, PH and 
-       RY QSOS.
-    4. Use the BONUS fields from SUMMARY when scoring.
-    5. Save only the LOGID and new results in the VHF
-       table. Delete and recreate the table each time.
-    6. Remove all report generation code. Use 
=       moqpdbvhfreports class to display results.
- Lots of 'extra' code was removed.      
* Tue May 24 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 -  Updated code to fix issue #34.
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
          'W0MABONUS int  NULL, ' +\
          'K0GQBONUS int NULL, ' +\
          'SCORE int NULL, '+\
          'PRIMARY KEY (ID));'
        mydb.write_query(dquery) # Delete old digital tables  
        mydb.write_query(dquery1) # Delete old digital tables  
        for entry in vdata:
            digid = mydb.write_pquery(\
             """INSERT INTO VHF 
                (LOGID, QSOS, CWQSO, PHQSO, RYQSO, 
                 MULTS, W0MABONUS, K0GQBONUS, SCORE) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
               [ entry['LOGID'], 
                 entry['QSOS'],
                 entry['CWQSO'],
                 entry['PHQSO'],
                 entry['RYQSO'],
                 entry['MULTS'],
                 entry['W0MABONUS'],
                 entry['K0GQBONUS'],
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
                    'W0MABONUS': 0,
                    'K0GQBONUS': 0,
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
              bonus = BonusAward(qsoList)
              if (bonus.Award['W0MA']['INLOG']):
                  entry['W0MABONUS']=100
              if (bonus.Award['K0GQ']['INLOG']):
                  entry['K0GQBONUS']=100
              entry['SCORE'] = ((((entry['CWQSO'] +
                                   entry['RYQSO']) * 2) +\
                                   entry['PHQSO']) *\
                                   entry['MULTS']) +\
                                   nextEnt['CABBONUS'] +\
                                   nextEnt['W0MABONUS'] +\
                                   nextEnt['K0GQBONUS']
              Vresult.append(entry)
       self.saveResults(mydb, Vresult)
       print('%d Stations with VHF+ scores summarized database.'%(len(Vresult)))
