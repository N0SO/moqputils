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


VERSION = '0.1.0'

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\t'+\
     'SCORE\tQSOS\tMULTS\t'+\
     'CABFILE BONUS\tW0MA BONUS\tK0GQ BONUS\t'

HEADERLINE = \
    '<tr>\n'+\
    '<th>RANK</th>\n' +\
    '<th>CALLSIGN</th>\n' +\
    '<th>OPERATORS</th>\n' +\
    '<th>LOCATION</th>\n' +\
    '<th>RY QSOs</th>\n' +\
    '<th>MULTS</th>\n' +\
    '<th>CABRILLO BONUS</th>\n' +\
    '<th>W0MA BONUS</th>\n' +\
    '<th>K0GQ BONUS</th>\n' +\
    '<th>SCORE</th>\n' +\
    '</tr>\n'
    
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
       csvdata= None

       if (log):
           csvdata = ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['SCORE']))
           csvdata += ('%d\t'%(log['QSOS']))
           csvdata += ('%s\t'%(log['MULTS']))
           csvdata += ('%s\t'%(log['CABBONUS']))
           csvdata += ('%s\t'%(log['W0MABONUS']))
           csvdata += ('%s'%(log['K0GQBONUS']))
       return csvdata

    def fetchDigital(self, callsign):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       call = callsign.upper()

       query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.OPERATORS, LOGHEADER.LOCATION, ' +\
                'DIGITAL.*, '+\
                'SUMMARY.W0MABONUS, SUMMARY.K0GQBONUS, '+\
                'SUMMARY.CABBONUS '+\
                'FROM DIGITAL JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=DIGITAL.LOGID '+\
                'AND LOCATION<>"%s" '%('MO')
       if (call != 'ALLCALLS'):
           query += 'AND LOGHEADER.CALLSIGN="%s" '%(call)

       query += 'JOIN SUMMARY ON DIGITAL.LOGID = SUMMARY.LOGID '+\
                'ORDER BY SCORE DESC;'

       digList = mydb.read_query(query)

       return digList       

    def appMain(self, callsign):

       digList = self.fetchDigital(callsign)
       
       print(COLUMNHEADERS)
       for ent in digList:
           print(self.showData(ent))
       #print(digList,len(digList))
       
class HTML_DigitalRpt(MOQPDBDigitalReport):
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain('ALLCALLS')

    def makeCell(self, cdata):
        return '<td>%s</td>'%(cdata)
            
    def makeRow(self, ranking, stationData):
        retData = '<tr>\n'
        if ranking<3:
            retData += self.makeCell(ranking)
        else:
            retData += '<td></td>'
        retData +='\n'
        retData += '</td>\n'
        retData += self.makeCell(stationData['CALLSIGN']) + '\n'
        retData += self.makeCell(stationData['OPERATORS']) + '\n'
        retData += self.makeCell(stationData['LOCATION']) + '\n'
        retData += self.makeCell(stationData['QSOS']) + '\n'
        retData += self.makeCell(stationData['MULTS']) + '\n'
        retData += self.makeCell(stationData['CABBONUS']) + '\n'
        retData += self.makeCell(stationData['W0MABONUS']) + '\n'
        retData += self.makeCell(stationData['K0GQBONUS']) + '\n'
        retData += self.makeCell(stationData['SCORE']) + '\n'
        retData += '</tr>\n'
        return retData
        
    def makeTable(self, qdata):
       retData = '<p><table>\n'
       retData += HEADERLINE
       rank = 1
       for station in qdata:
           retData += self.makeRow(rank, station)
           rank+=1
       retData += '</table></p>\n'
       
       return retData

    def displayDoc(self, stationList):
       PAGETITLE = '2021 Missouri QSO Party Digital Scores'
       STYLESHEET = './styles.css'
       WRAPPER = """<html>
          <head>
          <title>%s</title>
 	      <link href="%s" rel="stylesheet" type="text/css" />
          </head>
          <body>
          <H2 align="center">%s</H2>"""
          
       wholePage = WRAPPER % (PAGETITLE, 
                               STYLESHEET,
                               PAGETITLE)
       wholePage += self.makeTable(stationList)
       wholePage += '</body></html>'
       print(wholePage)

    def appMain(self, callsign):

       digList = self.fetchDigital(callsign)
       
       self.displayDoc(digList)
       
