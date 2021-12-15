#!/usr/bin/env python3
"""
logreport - 

Update History:
* Sat Feb 15 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
* Thu May 07 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Updates for 2020 MOQP:
-          Read config data here instead of in moqpdbutils
-          Added DUPES field to QSO report.
-          Improved error handling.
* Sat Jun 20 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Adding HTML display options to support web apps.
* Wed Sept 01 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.2 - Fix for Isuue #30.
"""

VERSION = '0.1.2' 

from moqputils.moqpdbutils import *
from cabrilloutils.CabrilloUtils import CabrilloUtils
from moqputils.configs.moqpdbconfig import *

class LogReport():

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def processHeader(self, header, endhtml=False):
        cab = CabrilloUtils()
        if (endhtml):
            csvdata ='<p>'
            endstg ='<br>'
        else:
            csvdata = ''
            endstg = '\n'
        for tag in cab.CABRILLOTAGS:
            csvdata += ('%s: %s%s'%(tag, header[tag], endstg))
        if (endhtml):
            csvdata +='</p>'
        return csvdata

    def showQSO(self, qso, html=False):
        if (html):
            if ('DATETIME' in qso.keys()):
                fmt ="""<tr>
                    <td><a href='./qslcheck.php?qsoid=%d' target='_blank'>%d</a></td>
                    <td>%d</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td>
                    </tr>"""

                qsoLine = (fmt %( qso['ID'], qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATETIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH'],
                          qso['VALID'],
                          qso['QSL'],
                          qso['NOLOG'],
                          qso['DUPE'],
                          qso['NOQSOS'],
                          qso['NOTE']))

            else: #old format
                fmt ="""<tr>
                    <td><a href='./qslcheck.php?qsoid=%d' target='_blank'>%d</a></td>
                    <td>%d</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td>
                    </tr>"""

                qsoLine = (fmt %( qso['ID'],qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATE'],
                          qso['TIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH'],
                          qso['VALID'],
                          qso['QSL'],
                          qso['NOLOG'],
                          qso['DUPE'],
                          qso['NOQSOS'],
                          qso['NOTE']))

        else: # Not HTML
            if ('DATETIME' in qso.keys()):
                fmt = '%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'+\
                  '%s\t%s\t%s\t%s\t%s\n'

                qsoLine = (fmt %( qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATETIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH'],
                          qso['VALID'],
                          qso['QSL'],
                          qso['NOLOG'],
                          qso['DUPE'],
                          qso['NOQSOS'],
                          qso['NOTE']))
            
            else: # old format
                fmt = '%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'+\
                  '%s\t%s\t%s\t%s\t%s\n'
        
                qsoLine = (fmt %( qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATE'],
                          qso['TIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH'],
                          qso['VALID'],
                          qso['QSL'],
                          qso['NOLOG'],
                          qso['DUPE'],
                          qso['NOQSOS'],
                          qso['NOTE']))
        return qsoLine

    def processQSOs(self, qsolist, header=True):
        if (header):
            csvdata = 'QSOID\tLOGID\tFREQ\tMODE\tDATE\tTIME\t'+ \
                      'MYCALL\tMYREPORT\tMYQTH\t'+ \
                      'URCALL\tURREPORT\tURQTH\t'+ \
                      'VALID\tQSLID\tNOLOG\tDUPE\tNOQSOS\tNOTES\n'
            header = False
        else:
            csvdata = ''
        for qso in qsolist:
            csvdata += self.showQSO(qso)
        return csvdata

    def processOne(self, mydb, callsign):
        logID=mydb.CallinLogDB(callsign)
        if (logID):
            log=mydb.fetchValidLog(callsign)
         
            query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID`=%d) AND (VALID=0) )"%(logID) )
            #print(query)
            invalid_qsos = mydb.read_query(query)

            csvdata = self.processHeader(log['HEADER'])

            csvdata += self.processQSOs(log['QSOLIST'])

            csvdata +=\
                '----------------INVALID QSOS-------------\n'
            csvdata += self.processQSOs(invalid_qsos)
        else:
            csvdata = ('Call %s not in database.'%(callsign))
        
        return csvdata

    def processAll(self, mydb):
        csvdata = []
        headers = True
        #loglist = mydb.read_query( \
        #       "SELECT ID, CALLSIGN FROM logheader WHERE CLUB!='' ORDER BY CLUB ASC")
        loglist = mydb.fetchLogList()
        #print(loglist)
        #print(len(loglist))
        if (loglist):
            Headers = True
            for nextlog in loglist:
                #print(nextlog)
                csvd=self.processOne(mydb, 
                               nextlog['CALLSIGN'])
                csvdata.append(csvd)
                Headers = False
            #print(csvdata)
            return csvdata
            
    def showReport(self, csvdata):
       if(csvdata):
           for csvline in csvdata:
               print(csvline)
        

    def appMain(self, callsign):
       print('Log Report for %s:'%(callsign))
       csvdata = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata=self.processAll(mydb)
       else:
           csvdata = []
           csvdata.append(self.processOne(mydb, callsign))

       self.showReport(csvdata)
        
class HTML_LogReport(LogReport):
    
    def showReport(self, csvdata):
        if (csvdata):
            self.wrapStringInHTMLMac('test',
                                     'http://localhost/',
                                     csvdata)
           
    """
    Given name of calling program, a url and a string to wrap,
    output string in html body with basic metadata and open in Firefox tab.
    """
    def wrapStringInHTMLMac(self, program, url, body):
        import datetime
        from webbrowser import open_new_tab

        now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        filename = program + '.html'
        logparts = body[0].split('END-OF-LOG:')
        #print(logparts)
        theader=self.makehtmlTable(logparts[0])
        tbody = self.makehtmlTable(logparts[1])
        wrapper = """<html>
            <head>
            <title>%s output - %s</title>
            </head>
            <body><p>URL: <a href=\"%s\">%s</a></p><p>%s</p><p>%s</p>
            </body>
            </html>"""

        whole = wrapper % (program, now, url, url, theader, tbody)
        with open(filename,'w') as f:
            f.writelines(whole)
            f.close()

        #Change the filepath variable below to match the location of your directory
        #filename = 'file:///./' + filename

        open_new_tab(filename)
        
    """
    Convert Tab Separated Variables line to HTML table
    """     
    def makehtmlTable(self, tdata):
        bodyl = tdata.splitlines()
        tbody ="<table>"
        for l in bodyl: 
            tbody +='<tr>'
            tl = l.split('\t')
            for td in tl: 
                tbody+='<td>%s</td>'%(td)
            tbody +='</tr>'
        tbody += '</table>'
        return tbody
        
