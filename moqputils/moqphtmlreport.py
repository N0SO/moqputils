#!/usr/bin/env python3
"""
moqphtmlreport - Same features as moqpdbcategory, except
                   generate HTML report for the web.
                   
                   Based on 2019 MOQP Rules.
                  
Update History:
* Sat Sep 05 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Wed Dec 15 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - DEVMODPATH updates.
"""
from moqputils.moqpdbcatreport import *
#from moqpdbutils import *
#from moqpdbconfig import *


VERSION = '0.0.2' 

HEADERLINE = \
    '<tr>\n'+\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>RANK</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>CALLSIGN</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>OPERATORS</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>CW QSOs</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>PH QSOs</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>RY QSOs</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>MULTS</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>W0MA BONUS</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>K0GQ BONUS</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>CABRILLO BONUS</strong></td>\n' +\
    '<td class="xl63" style="background-color: #99ccff; border: 1px solid #000000;"><strong>SCORE</strong></td>\n' +\
    '</tr>\n'

TBOARDER='<td style="border: 1px solid #000000;">'

class MOQPHtmlReport(MOQPDBCatReport):

    def __init__(self, callsign):
        if (callsign):
            self.appMain(callsign)
            
    def formatStationData(self, ranking, stationData):
        retData = '<tr>\n'
        retData += TBOARDER
        if ranking<3:
            retData += ('%s'%ranking)
        retData += '</td>\n'
        retData += TBOARDER +\
            stationData['CALLSIGN'] + '</td>\n'
        retData += TBOARDER +\
            stationData['OPERATORS'] + '</td>\n'
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['CWQSO']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['PHQSO']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['RYQSO']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['MULTS']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['W0MABONUS']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['K0GQBONUS']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['CABBONUS']))
        retData += TBOARDER +\
            ('%d</td>\n'%(stationData['SCORE']))
        retData += '</td>\n'
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
                '<P>\n<table border="0" style="border: 1px solid #000000; margin-left: auto; margin-right: auto;" cellpadding="0">' +\
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
            #print(htmlList)
            #exit()
        return htmlList
        
    def displayDoc(self, htmlDoc):
       for htmlCat in htmlDoc:
           for station in htmlCat['STATIONS']:
               print(station)
           #print(htmlLine['STATIONS'])
           #print(type(htmlLine))
           #print(dir(htmlLine))
            
    def appMain(self, callsign):
       htmldata = '<p>No Data.</p>'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'HTML'):
           htmldata=self.processSums(mydb)
       #print(htmldata)
       self.displayDoc(htmldata)
       """
       for csvLine in csvdata:
           print(csvLine)
       """
