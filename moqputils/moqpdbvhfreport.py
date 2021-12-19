#!/usr/bin/env python3
"""
moqpdbvhfreport - Display VHF scores only from data stored
                  in the VHF table.

                  Prerequisits:
                   1. All logs loaded into database with
                      mqplogcheck -l
                   2. QSO Validation completed on all logs
                      with qsocheck -c allcalls
                   3. mqpcategory completed:
                      mqpcategory -c allcalls
                      mqpcategory -U (or  --vhf)

                  These steps create the summary tables
                  SUMMARY and VHF required by this code.

                  Added for the 2020 MOQP.

Update History:
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Thu Dec 09 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Refactored for efficiency.
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
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from htmlutils.htmldoc import htmlDoc


VERSION = '0.1.0'
#Column headers
COLUMNHEADERS = \
     'RANKING\tCALLSIGN\tOPS\tLOCATION\tSCORE\t'+\
     'QSOs\tCW QSOs\tPH QSOs\tRY QSOs\tMULTS\t'+\
     'CABFILE BONUS\tW0MA BONUS\tK0GQ BONUS'

#Column headers for HTML reports
HEADERLINE = [
    'RANK',
    'CALLSIGN',
    'OPERATORS',
    'LOCATION',
    'SCORE',
    'QSOs',
    'CW QSOs',
    'PH QSOs',
    'RY QSOs',
    'MULTS',
    'CABRILLO BONUS',
    'W0MA BONUS',
    'K0GQ BONUS']

"""
Index of dictionary keys from the database column names. Use 
these to iterate over the dictionary returned by the database
queries. The order will determin the order of the items in the
reports. The HEADER item names should match this for the reports
data to be in the correct order.
"""
DIGTABLEIDX = ['RANK',
               'CALLSIGN',
               'OPERATORS',
                'LOCATION',
                'SCORE',
                'QSOS',
                'CWQSO',
                'PHQSO',
                'RYQSO',
                'MULTS',
                'CABBONUS',
                'W0MABONUS',
                'K0GQBONUS']
"""                
HEADERLINE = \
    '<tr>\n'+\
    '<th>RANK</th>\n' +\
    '<th>CALLSIGN</th>\n' +\
    '<th>OPERATORS</th>\n' +\
    '<th>LOCATION></th>\n' +\
    '<th>SCORE</th>\n' +\
    '<th>QSOs</th>\n' +\
    '<th>CW QSOs</th>\n' +\
    '<th>PH QSOs</th>\n' +\
    '<th>RY QSOs</th>\n' +\
    '<th>MULTS</th>\n' +\
    '<th>CABRILLO BONUS</th>\n' +\
    '<th>W0MA BONUS</th>\n' +\
    '<th>K0GQ BONUS</th>\n' +\
    '</tr>\n'
"""

class MOQPDBVhfReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def showData(self, log):
       csvdata= None

       if (log):
           csvdata = ('%s\t'%(log['RANK']))
           csvdata += ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += ('%d\t'%(log['QSOS']))
           csvdata += ('%d\t'%(log['CWQSO']))
           csvdata += ('%d\t'%(log['PHQSO']))
           csvdata += ('%d\t'%(log['RYQSO']))
           csvdata += ('%s\t'%(log['MULTS']))
           csvdata += ('%s\t'%(log['CABBONUS']))
           csvdata += ('%s\t'%(log['W0MABONUS']))
           csvdata += ('%s'%(log['K0GQBONUS']))
       return csvdata

    def fetchVHF(self, callsign, ftype=None):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       call = callsign.upper()

       cquery = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.OPERATORS, LOGHEADER.LOCATION, ' +\
                'VHF.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM VHF JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=VHF.LOGID '
       if (ftype):
           ftype = ftype.lower()
           if (ftype =='mo'):
               cquery += 'AND LOCATION="MO" '
           elif (ftype == 'non-mo'):
               cquery += 'AND LOCATION<>"MO" '
       if (call != 'ALLCALLS'):
           cquery += 'AND LOGHEADER.CALLSIGN="%s" '%(call)

       cquery+= 'JOIN SUMMARY ON VHF.LOGID = SUMMARY.LOGID '+\
                'ORDER BY SCORE DESC, LOCATION ASC;'

       vList = mydb.read_query(cquery) 
       return vList

    def addRankingField(self, dictList, fname, maxRank = 3):
       rank = 1
       rankeddictList = []
       for station in dictList:
           if rank < maxRank: station[fname] = '%s'%(rank)
           else: station[fname] = ' '
           rankeddictList.append(station)
           rank += 1
       return rankeddictList

    def appMain(self, callsign):
       temp = self.fetchVHF(callsign, 'mo')
       rankeddigList = self.addRankingField(temp, 'RANK', 3)
       print(COLUMNHEADERS)
       for ent in rankeddigList:
           print(self.showData(ent))

       temp = self.fetchVHF(callsign, 'non-mo')
       rankeddigList = self.addRankingField(temp, 'RANK', 3)
       print(COLUMNHEADERS)
       for ent in rankeddigList:
           print(self.showData(ent))

class HTML_VHFRpt(MOQPDBVhfReport):
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain('ALLCALLS')

    def appMain(self, callsign):
       d = htmlDoc()
       d.openHead('2021 Missouri QSO Party VHF ONLY Scores',
                  './styles.css')
       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
             """<h2 align='center'>2021 Missouri QSO Party VHF ONLY Scores</h2>""")

       modictList = self.fetchVHF(callsign,ftype='mo')
       rankeddictList = self.addRankingField(modictList,
                                             'RANK',
                                              3)

       d.addTablefromDict(dictList=rankeddictList, 
                          HeaderList=HEADERLINE,
                          caption='MISSOURI STATIONS',
                          dictIndexList=DIGTABLEIDX)
       modictList = self.fetchVHF(callsign,ftype='non-mo')
       rankeddictList = self.addRankingField(modictList,
                                             'RANK',
                                              3)

       d.addTablefromDict(dictList=rankeddictList, 
                          HeaderList=HEADERLINE,
                          caption='NON-MISSOURI STATIONS',
                          dictIndexList=DIGTABLEIDX)
              
              
       d.closeBody()
       d.closeDoc()

       d.showDoc()
       d.saveAndView('ttest2.html')
