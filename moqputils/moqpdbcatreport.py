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
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *


VERSION = '0.1.0' 

COLUMNHEADERS = \
     'CALLSIGN\tOPS\tLOCATION\tMOQP CATEGORY\t'+\
     'SCORE\tCW QSO\tPH QSO\tRY QSO\tQSO COUNT\t'+\
     'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t'+\
     'CABFILE BONUS\tVHF QSO\tVHF\tDIGITAL\tROOKIE\t'+\
     'STATION\tOPERATOR\tPOWER\tMODE\tOVERLAY\t'
                

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
  
    def showReport(self, csvdata):
        if (csvdata):
            html=self.wrapStringInHTMLMac('MOQP-Scores-By-Category',
                                     'Missouri QSO Party Scores by Category',
                                     csvdata)
        print(html)
    """
    Given name of calling program, a url and a string to wrap,
    output string in html body with basic metadata and open in Firefox tab.
    """
    def wrapStringInHTMLMac(self, program, url, body):
        import datetime
        from webbrowser import open_new_tab

        now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        filename = program + '.html'
        tbody = self.makehtmlTable(body)
        wrapper = """<html>
            <head>
            <title>%s output - %s</title>
            <link href="./styles.css" rel="stylesheet" type="text/css" />
            </head>
            <body><p>URL: <a href=\"%s\">%s</a></p><p>%s</p>
            </body>
            </html>"""

        whole = wrapper % (program, now, url, url, tbody)
        with open(filename,'w') as f:
            f.writelines(whole)
            f.close()

        #Change the filepath variable below to match the location of your directory
        #filename = 'file:///./' + filename

        open_new_tab(filename)
        
        return whole
        
    """
    Convert Tab Separated Variables line to HTML table
    """     
    def makehtmlTable(self, tdata, headers = True):
        tbody ="<table>"
        for l in tdata: 
            tbody +='<tr>'
            tl = l.split('\t')
            for td in tl:
              if(headers): 
                tbody+='<th>%s</th>'%(td)
              else:
                tbody+='<td>%s</td>'%(td)
            headers = False
            tbody +='</tr>'
        tbody += '</table>'
        return tbody
        
  
