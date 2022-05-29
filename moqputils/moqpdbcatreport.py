#!/usr/bin/env python3
"""
moqpdbcatreport - Same features as moqpcategory, except read
                  all data from an SQL database. The log file
                  header is fetched fron the LOGHEADER table,
                  the SUMMARY is fetched from the SUMMARY table,
                  and a CSV report is created and displayed.
                  
                  QSO Validation (QSL, time check, etc) should
                  already have been performed on the data, and
                  the SUMMARY row for this log should have been
                  updated before running this report.
                
                  Based on 2019 MOQP Rules.
                  
Update History:
* Thu Jan 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Sun May 17 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Updates for 2020 MOQP changes
- Integrated necessary log header data
- Used SQL to sort report by:
-      MOQP Category
-      Total Score
-      Location.
* Sun Sep 05 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Updates for 2021 and new devpath.py
* Fri May 27 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Added code to use YEAR parameter set in moqpdefs.py in
-          titles so they don't have to be updated every year.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *


VERSION = '0.1.1' 

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\tMOQP CATEGORY\t'+\
     'SCORE\tCW QSO\tPH QSO\tRY QSO\tQSO COUNT\t'+\
     'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t'+\
     'CABFILE BONUS\tVHF QSO\tVHF\tDIGITAL\tROOKIE\t'+\
     'STATION\tOPERATOR\tPOWER\tMODE\tOVERLAY\t'
 
HEADERLINE = \
    '<tr>\n'+\
    '<th>RANK</th>\n' +\
    '<th>CALLSIGN</th>\n' +\
    '<th>OPERATORS</th>\n' +\
    '<th>CW QSOs</th>\n' +\
    '<th>PH QSOs</th>\n' +\
    '<th>RY QSOs</th>\n' +\
    '<th>MULTS</th>\n' +\
    '<th>W0MA BONUS</th>\n' +\
    '<th>K0GQ BONUS</th>\n' +\
    '<th>CABRILLO BONUS</th>\n' +\
    '<th>SCORE</th>\n' +\
    '</tr>\n'

class MOQPDBCatReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsvsumdata(self, log, Headers=True):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
    
       If the Headers option is false, it will skip printing the
       csv header info.
       """
       csvdata= None

       if (log):
           #print(log)
       
           if (Headers): 
               csvdata = COLUMNHEADERS
               
           else:
               csvdata = ''
               
           cw = int(log['CWQSO'])
           ph = int(log['PHQSO'])
           ry = int(log['RYQSO'])
           qsocount = cw + ph + ry

           csvdata += ('%s\t'%(log['CALLSIGN']))
           csvdata += ('%s\t'%(log['OPERATORS']))
           csvdata += ('%s\t'%(log['LOCATION']))
           csvdata += ('%s\t'%(log['MOQPCAT']))
           csvdata += ('%s\t'%(log['SCORE']))         
           csvdata += ('%s\t'%(log['CWQSO']))
           csvdata += ('%s\t'%(log['PHQSO']))
           csvdata += ('%s\t'%(log['RYQSO']))
           csvdata += ('%d\t'%(qsocount))
           csvdata += ('%s\t'%(log['MULTS']))         
           csvdata += ('%s\t'%(log['QSOSCORE']))         
           csvdata += ('%s\t'%(log['W0MABONUS']))         
           csvdata += ('%s\t'%(log['K0GQBONUS']))         
           csvdata += ('%s\t'%(log['CABBONUS']))         
           csvdata += ('%s\t'%(log['VHFQSO']))
           csvdata += ('%s\t'%(log['VHF']))
           csvdata += ('%s\t'%(log['DIGITAL']))
           csvdata += ('%s\t'%(log['ROOKIE']))
           csvdata += ('%s\t'%(log['CATSTATION']))
           csvdata += ('%s\t'%(log['CATOPERATOR']))
           csvdata += ('%s\t'%(log['CATPOWER']))
           csvdata += ('%s\t'%(log['CATMODE']))
           csvdata += ('%s\t'%(log['CATOVERLAY']))

       else:
          csvdata = None
       return csvdata

    def parseReport(self, mydb, sumdata):
        if (sumdata):
            thisSum = sumdata
            header=mydb.read_pquery(\
                        'SELECT * FROM LOGHEADER WHERE ID=%s',
                                            [sumdata['LOGID']])
            #print(header)
            if (len(header) > 0):
                header=header[0]
                thisSum['CALLSIGN']=header['CALLSIGN']
                thisSum['CATASSISTED']=header['CATASSISTED']
                thisSum['CATBAND']=header['CATBAND']
                thisSum['CATOPERATOR']=header['CATOPERATOR']
                thisSum['CATOVERLAY']=header['CATOVERLAY']
                thisSum['CATPOWER']=header['CATPOWER']
                thisSum['CATSTATION']=header['CATSTATION']
                thisSum['CATXMITTER']=header['CATXMITTER']
                thisSum['OPERATORS']=header['OPERATORS']
                thisSum['CATMODE']=header['CATMODE']
                thisSum['LOCATION']=header['LOCATION']
            else:
                thisSum['CALL']='NO HEADER FOR LOGID %s, SUMMARY ID %s'\
                                             %(sumdata['LOGID'], sumdata['ID'])
                thisSum['CATASSISTED']=''
                thisSum['CATBAND']=''
                thisSum['CATOPERATOR']=''
                thisSum['CATOVERLAY']=''
                thisSum['CATPOWER']=''
                thisSum['CATSTATION']=''
                thisSum['CATXMITTER']=''
                thisSum['OPERATORS']=''
                thisSum['CATMODE']=''
                print('%s'%(thisSum['CALL']))
                exit()
        return thisSum
        
    def processOneSum(self, mydb, call):
        csvList = ['No log for %s'%(call)]
        thisStation = mydb.fetchLogSummary(call)
        if (thisStation):
            thisreport = self.parseReport(mydb, thisStation)
            csvdata = self.exportcsvsumdata(thisreport, False)
            csvList.append(COLUMNHEADERS)
            csvList.append(csvdata)
        return csvList
            
    def processSums(self, mydb):
        csvList=[]
        reportList = []
        sumdata = mydb.read_query('SELECT * FROM SUMMARY '+\
              'ORDER BY MOQPCAT ASC, SCORE DESC, LOCATION ASC')
        if (sumdata):
            csvList.append(COLUMNHEADERS)
            for thisStation in sumdata:
                #print('ID=%s'%(thisStation['ID']))
                thisreport = self.parseReport(mydb, thisStation)
                reportList.append(thisreport)
                csvdata = self.exportcsvsumdata(thisreport, False)
                if (csvdata): 
                    csvList.append(csvdata)
        return csvList
    
    def showReport(self, csvdata):
      if (csvdata):
        for csvLine in csvdata:
          print(csvLine)

    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata=self.processSums(mydb)
       else:
           csvdata = self.processOneSum(mydb, callsign)
           #print(csvdata)
       self.showReport(csvdata)

class MOQPHtmlReport(MOQPDBCatReport):

    def __init__(self, callsign):
        if (callsign):
            self.appMain(callsign)
            
    def makeCell(self, cdata):
        return '<td>%s</td>'%(cdata)
            
    def formatStationData(self, ranking, stationData):
        retData = '<tr>\n'
        if ranking<3:
            retData += self.makeCell(ranking)
        else:
            retData += '<td></td>'
        retData +='\n'
        retData += '</td>\n'
        retData += self.makeCell(stationData['CALLSIGN']) + '\n'
        retData += self.makeCell(stationData['OPERATORS']) + '\n'
        retData += self.makeCell(stationData['CWQSO']) + '\n'
        retData += self.makeCell(stationData['PHQSO']) + '\n'
        retData += self.makeCell(stationData['RYQSO']) + '\n'
        retData += self.makeCell(stationData['MULTS']) + '\n'
        retData += self.makeCell(stationData['W0MABONUS']) + '\n'
        retData += self.makeCell(stationData['K0GQBONUS']) + '\n'
        retData += self.makeCell(stationData['CABBONUS']) + '\n'
        retData += self.makeCell(stationData['SCORE']) + '\n'
        return retData

    def processCat(self, mydb, catName):
        stationList = []
        sumdata = mydb.read_pquery(\
           'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
           'LOGHEADER.OPERATORS, SUMMARY.* '+\
           'FROM LOGHEADER INNER JOIN SUMMARY ON '+\
           'LOGHEADER.ID=SUMMARY.LOGID '+\
           'WHERE SUMMARY.MOQPCAT=%s ' +\
           'ORDER BY SCORE DESC, LOCATION ASC',
              [catName])

        stationList.append(\
                '<P>\n<table>' +\
                ('<caption><h2><strong>%s</strong></h2></caption>'%(catName)) +\
                '<tbody>\n' +\
                HEADERLINE)

        rank = 0
        for station in sumdata:
            rank += 1
            thiStation = self.formatStationData(rank, station)
            stationList.append(thiStation)
        stationList.append('</tbody>\n</table>\n</P>\n')

        return stationList   
            
    def processSums(self, mydb):
        htmlList=[]
        reportList = []
        sumdata = mydb.read_query('SELECT DISTINCT MOQPCAT '+\
              'FROM SUMMARY ORDER BY MOQPCAT ASC')
        #sumdata = mydb.read_query('SELECT * FROM SUMMARY '+\
        #      'ORDER BY MOQPCAT ASC, SCORE DESC, LOCATION ASC')
        #print ('sumdata = %s'%(sumdata))
        if (sumdata):
            htmlList = []
            for thisCat in sumdata:
                category = {'NAME': thisCat['MOQPCAT'],
                            'STATIONS': []}
                category['STATIONS'] = \
                    self.processCat(mydb, thisCat['MOQPCAT'])
                htmlList.append(category)
        return htmlList
        
    def displayDoc(self, htmlDoc):
       PAGETITLE = '{} Missouri QSO Party Scores by Category'\
                         .format(YEAR)
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
       for htmlCat in htmlDoc:
           for station in htmlCat['STATIONS']:
               wholePage += station
       wholePage += '</body></html>'
       print(wholePage)
            
    def appMain(self, callsign):
       htmldata = '<p>No Data.</p>'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'HTML'):
           htmldata=self.processSums(mydb)
       self.displayDoc(htmldata)
