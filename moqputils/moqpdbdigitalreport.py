#!/usr/bin/env python3
"""
moqpdbdigitalreport - Same features as moqpcategory -d,
                  except read all data from an SQL database
                  DIGITAL Summary table.

                  Prerequisits:
                   1. All logs loaded into database with
                      mqplogcheck -l
                   2. QSO Validation completed on all logs
                      with qsocheck -c allcalls
                   3. mqpcategory completed:
                      mqpcategory -c allcalls
                      mqpcategory -d

                  These steps create the summary tables
                  SUMMARY and DIGITAL required by this code.

                  Added for the 2020 MOQP.

Update History:
* Sat May 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs
* Thu Dec 09 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Refactored for efficiency.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from htmlutils.htmldoc import *


VERSION = '0.1.0'

#Column headers for printed/csv reports
COLUMNHEADERS = \
     'RANKING\tCALLSIGN\tOPS\tLOCATION\t'+\
     'SCORE\tQSOS\tMULTS\t'+\
     'CABFILE BONUS\tW0MA BONUS\tK0GQ BONUS\t'

#Column headers for HTML reports
HEADERLINE = [
    'RANK',
    'CALLSIGN',
    'OPERATORS',
    'LOCATION',
    'SCORE',
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
                'MULTS',
                'CABBONUS',
                'W0MABONUS',
                'K0GQBONUS']
    
class MOQPDBDigitalReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def showData(self, log):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
       """
       csvdata= ""

       if (log):
           csvdata += ('%s\t'%(log['RANK']))
           csvdata += ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += ('%d\t'%(log['QSOS']))
           csvdata += ('%s\t'%(log['MULTS']))
           csvdata += ('%s\t'%(log['CABBONUS']))
           csvdata += ('%s\t'%(log['W0MABONUS']))
           csvdata += ('%s'%(log['K0GQBONUS']))
       return csvdata

    def fetchDigital(self, callsign, ftype=None):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       call = callsign.upper()

       query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.OPERATORS, LOGHEADER.LOCATION, ' +\
                'DIGITAL.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM DIGITAL JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=DIGITAL.LOGID '
       if (ftype):
           ftype = ftype.lower()
           if (ftype =='mo'):
               query += 'AND LOCATION="MO" '
           elif (ftype == 'non-mo'):
               query += 'AND LOCATION<>"MO" '
       if (call != 'ALLCALLS'):
           query += 'AND LOGHEADER.CALLSIGN="%s" '%(call)

       query += 'JOIN SUMMARY ON DIGITAL.LOGID = SUMMARY.LOGID '+\
                'ORDER BY LOCATION ASC, SCORE DESC;'

       digList = mydb.read_query(query)
       return digList

    def addRankingField(self, dictList, fname, maxRank = 2):
       rank = 1
       rankeddictList = []
       for station in dictList:
           if rank < maxRank: station[fname] = '%s'%(rank)
           else: station[fname] = ' '
           rankeddictList.append(station)
           rank += 1
       return rankeddictList
        

    def appMain(self, callsign):

       digList = self.fetchDigital(callsign,'mo')
       rankeddigList = self.addRankingField(digList, 'RANK', 3)
       
       print(COLUMNHEADERS)
       for ent in rankeddigList:
           print(self.showData(ent))

       digList = self.fetchDigital(callsign,'non-mo')
       rankeddigList = self.addRankingField(digList, 'RANK', 3)
       
       print(COLUMNHEADERS)
       for ent in rankeddigList:
           print(self.showData(ent))

       
class HTML_DigitalRpt(MOQPDBDigitalReport):
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain('ALLCALLS')

    def appMain(self, callsign):
       d = htmlDoc()
       d.openHead('2021 Missouri QSO Party Digital Scores',
                  './styles.css')
       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
             """<h2 align='center'>2021 Missouri QSO Party DIGITAL ONLY Scores</h2>""")

       modictList = self.fetchDigital(callsign,ftype='mo')
       rankeddictList = self.addRankingField(modictList,
                                             'RANK',
                                              3)

       d.addTablefromDict(dictList=rankeddictList, 
                          HeaderList=HEADERLINE,
                          caption='MISSOURI STATIONS',
                          dictIndexList=DIGTABLEIDX)
       modictList = self.fetchDigital(callsign,ftype='non-mo')
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
