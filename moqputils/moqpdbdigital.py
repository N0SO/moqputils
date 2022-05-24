#!/usr/bin/env python3
"""
moqpdbdigital   - Creates digital mode only scores table named 
                  DIGITAL; Uses data from tables LOGHEADER, QSO 
                  and SUMMARY to create the new DIGITAL scores
                  table with a LOGID that points to the LOGHEADER
                  table. The valid digital only QSOs are fetched
                  from the QSO table to create the new DIGITAL
                  table. Also uses data from the SUMMARY table.
                  Same features as moqpdbcategory, except read only
                  digital mode QSOs for categorization and summary.

                  QSO Validation (DUPE, QSL, time checks, etc) 
                  should already have been 
                  performed on the data.
        
                  Updated for the 2021 MOQP.
Update History:
* Thu Feb 13 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Wed May 27 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Updated logheader to LOGHEADER.
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Added method updateDB to add digital scores to
- the database table DIGITAL (or update entries if an
- entry for the station exists already.
* Fri Aug 28 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Fixed bug causing an error and failure to
- to insert new table data found during updates.
* Wed Dec 08 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.0 - Changes for 2021
-  1. Refactored code to use data already collected
-     in SUMMARY, LOGHEADER and QSO tables instead of
-     repeating the previous operations.
   2. Now deletes old tables and re-creates them with 
      fresh reults each time.  
* Mon May 23 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Changes for 2022
-          Fix for issue #35
-          Code now queries for digital only contacts with
-          W0MA and K0GQ to use for adding bonus points for
-          those stations.
"""

from moqputils.moqpdbcategory import *
from moqputils.moqpdbutils import *
from moqputils.bonusaward import BonusAward
from moqputils.moqpdefs import DIGIMODES
from moqputils.moqpmults import *

VERSION = '1.0.0' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\t' + \
                'RY QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\n'

class MOQPDBDigital(MOQPDBCategory):
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def saveResults(self, mydb, digidata):
        dquery ='DROP TABLE IF EXISTS DIGITAL;'
        dquery1 = 'CREATE TABLE DIGITAL ('+\
          'ID int NOT NULL AUTO_INCREMENT, '+\
          'LOGID int NOT NULL, '+\
          'QSOS int NULL, '+\
          'MULTS int NULL, '+\
          'W0MABONUS int NULL, '+\
          'K0GQBONUS int NULL, '+\
          'SCORE int NULL, '+\
          'PRIMARY KEY (ID));'
        mydb.write_query(dquery) # Delete old digital tables  
        mydb.write_query(dquery1) # Delete old digital tables  
        for entry in digidata:
            digid = mydb.write_pquery(\
               'INSERT INTO DIGITAL '+\
               '(LOGID, QSOS, MULTS, W0MABONUS, K0GQBONUS, SCORE) '+\
               'VALUES (%s, %s, %s, %s, %s, %s)',
               [ entry['LOGID'], 
                 entry['QSOS'],
                 entry['MULTS'],
                 entry['W0MABONUS'],
                 entry['K0GQBONUS'],
                 entry['SCORE'] ])
            #print('Writing %d\n'%(digid))

    def appMain(self, callsign):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       digList = digList = mydb.read_query(\
                 'SELECT * FROM SUMMARY WHERE DIGITAL>0 ' +\
                 'ORDER BY RYQSO DESC')
 
       #Score the digital list
       digresult = []       
       for nextEnt in digList:
           query = \
            "SELECT * FROM QSOS WHERE LOGID=%d"%(nextEnt['LOGID'])
           query += " AND VALID=1 AND ("+\
                "MODE LIKE '%RY%' OR "+\
                "MODE LIKE '%DG%' OR "+\
                "MODE LIKE '%DIG%' OR "+\
                "MODE LIKE '%DIGI%' OR "+\
                "MODE LIKE '%RTTY%' OR "+\
                "MODE LIKE '%FT8%' OR "+\
                "MODE LIKE '%FT4%' OR "+\
                "MODE LIKE '%PSK31%')"

           entry = {'LOGID': nextEnt['LOGID'],
                    'QSOS': 0,
                    'MULTS': 0,
                    'SCORE': 0 } 

           qsoList = mydb.read_query(query)

           #print(qsoList)
           if (len(qsoList)>0):
              entry['QSOS'] = len(qsoList)
              digimults = MOQPMults(qsoList)
              entry['MULTS'] = digimults.sumMults()
              if (entry['MULTS'] == 0): entry['MULTS']=1
              entry['W0MABONUS'] = 0
              entry['K0GQBONUS'] = 0
              bonus = BonusAward(qsoList)
              if (bonus.Award['W0MA']['INLOG']):
                  entry['W0MABONUS']=100
              if (bonus.Award['K0GQ']['INLOG']):
                  entry['K0GQBONUS']=100
              entry['SCORE'] = ((len(qsoList) * 2)\
                                 * entry['MULTS']) + \
                                 nextEnt['CABBONUS'] + \
                                 entry['W0MABONUS'] + \
                                 entry['K0GQBONUS']
              digresult.append(entry)
           #print(len(qsoList), nextEnt['RYQSO'], entry['MULTS'])
           #print(nextEnt)
           #print(entry)
           #exit()          
       self.saveResults(mydb, digresult)
       print('%d Stations with digital scores summarized database.'%(len(digresult)))
