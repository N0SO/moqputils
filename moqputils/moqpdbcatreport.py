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
* Sat Jun 18 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Relase and..
-          Added code to use htmlDoc class for html reports.
-          Added code to order score categories by what is
-          defined in moqpawardefs.py AWARDLIST. This was done
-          for both CSV/TSV and HTML reports.
* Mon Jul 04 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.1 - Changed RY QSOs to DIG QSOs in HTML reports
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import AWARDLIST


VERSION = '1.0.1' 

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

    def processOneCat(self, mydb, cati):
        csvList = []
        cat=cati.strip()
        csvList.append(cat)
        sumdata = mydb.read_query(\
              """SELECT * from SUMMARY 
                 WHERE MOQPCAT='{}'
                 ORDER BY SCORE DESC, LOCATION ASC""".format(cat))
        if (sumdata):
            csvList.append(COLUMNHEADERS)
            for thisStation in sumdata:
                #print('ID=%s'%(thisStation['ID']))
                thisreport = self.parseReport(mydb, thisStation)
                csvdata = self.exportcsvsumdata(thisreport, False)
                if (csvdata): 
                    csvList.append(csvdata)
        else:
            csvList.append('NO ENTRY')
            
        return csvList

    def processCatSums(self, mydb, catlist=AWARDLIST):
        csvList = []
        reportList = [] 
        for cati in catlist:
           cat=cati.strip()

           csvList.append(cat)
           sumdata = mydb.read_query(\
              """SELECT * from SUMMARY 
                 WHERE MOQPCAT='{}'
                 ORDER BY SCORE DESC, LOCATION ASC""".format(cat))
           if (sumdata):
                csvList.append(COLUMNHEADERS)
                for thisStation in sumdata:
                    #print('ID=%s'%(thisStation['ID']))
                    thisreport = self.parseReport(mydb, thisStation)
                    reportList.append(thisreport)
                    csvdata = self.exportcsvsumdata(thisreport, False)
                    if (csvdata): 
                        csvList.append(csvdata)
           else:
               csvList.append('NO ENTRY')
            
        return csvList
            
    
    def showReport(self, csvdata):
      if (csvdata):
        for csvLine in csvdata:
          print(csvLine)

    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'ALLCALLS'):
           csvdata=self.processSums(mydb)
       elif (callsign == 'ALLCATS'):
           csvdata=self.processCatSums(mydb)
       else:
           csvdata = self.processOneSum(mydb, callsign)
           #print(csvdata)
       self.showReport(csvdata)

class MOQPHtmlReport(MOQPDBCatReport):

    def __init__(self, callsign):
        if (callsign):
            self.appCat(callsign)

    def appCat(self, callsign, catList=AWARDLIST):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       from htmlutils.htmldoc import htmlDoc   
       d = htmlDoc()
       d.openHead('{} Missouri QSO Party Scores by Category'.format(YEAR),
                  './styles.css')
       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party Scores by Category</h2>
""".format(YEAR))

       for cati in catList:
           cat=cati.strip()

           sumdata = mydb.read_pquery(\
            """SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN,
               LOGHEADER.OPERATORS, SUMMARY.*
               FROM LOGHEADER INNER JOIN SUMMARY ON 
               LOGHEADER.ID=SUMMARY.LOGID
               WHERE SUMMARY.MOQPCAT=%s
               ORDER BY SCORE DESC, LOCATION ASC""",
              [cat])
           tableData=['RANK\tCALLSIGN\tOPERATORS\tSCORE\t'+\
                        'CW QSOs\tPH QSOs\tDIG QSOs\tMULTS\t'+\
                        'W0MA BONUS\tK0GQ BONUS\tCAB BONUS']
           if (len(sumdata) == 0): #No data
               tableData.append('\t\t\t\t\tNO ENTRY\t\t\t\t\t')
                  
           rank = 0
           for station in sumdata:
               rank += 1
               if (rank < 3):
                   tableData.append(\
                    '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'\
                    .format(rank,
                        station['CALLSIGN'],
                        station['OPERATORS'],
                        station['SCORE'],
                        station['CWQSO'],
                        station['PHQSO'],
                        station['RYQSO'],
                        station['MULTS'],
                        station['W0MABONUS'],
                        station['K0GQBONUS'],
                        station['CABBONUS']))
               else:
                   tableData.append(\
                    '\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'\
                    .format(\
                        station['CALLSIGN'],
                        station['OPERATORS'],
                        station['SCORE'],
                        station['CWQSO'],
                        station['PHQSO'],
                        station['RYQSO'],
                        station['MULTS'],
                        station['W0MABONUS'],
                        station['K0GQBONUS'],
                        station['CABBONUS']))

           d.addTable(tdata=d.tsvlines2list(tableData),
                  header=True,
                  caption='<h3>{}</h3>'.format(cat))

       d.closeBody()
       d.closeDoc()

       d.showDoc()
       d.saveAndView('scoresbycat.html')

