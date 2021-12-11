#!/usr/bin/python
"""
MOQPMults    - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file for the ARRL Missouri QSO Party.
               Inherits from ContestMults() class.
Update History:
* Fri Jan 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
* Thu Sep 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.2 - Adding code to capture last new county worked.
* Fri Sep 11 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3
- Added code to track the last new county worked,
- saving the county abbreviation and date/time. This was
- added to resolve a tie situation in the Most Counties Worked
- Award.
"""

from cabrilloutils.contestmults import *
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from cabrilloutils.qsoutils import QSOUtils


VERSION = '0.1.0'

MULTFILES = ['shared/multlists/moqp-counties.csv']

COLUMNHEADERS = 'CALLSIGN\tOPS\tLOCATION\tCOUNTY COUNT\t '+\
                'COUNTY NAMES\tLAST COUNTY WORKED/TIME\n'

class MOQPDBCountyMults(ContestMults):
    """
    This class inherits from the class ContestMults
    to create a Missouri QSO Party specific object to
    track and record contest mults.

    1. Creates a list of Missouri County boolean objects in
       the dictionary MULTS. Each entry name is the same as
       the 3 character Missouri County. The files passed to
       method readmultlists(...) are used to create the mults
       dictionary. The __init__ method is set to use the 
       standard list of Missouri Counties defined in MULTFILES.
       each list item is an integer that will be zero if that
       county has not been worked, or the QSO ID of the first
       QSO with a station in that county.

    
    2. Also creates last_new_county to track the last new
       county worked with date/time to support resolving
       a tie for the "Most Counties Worked" award.
    """
    def __init__(self, callsign=None):
       self.mults = self.readmultlists(MULTFILES)
       #print(self.multlist, mult, multval, date, time)
       self.last_new_county = None
       self.lnc_time = None
       if (callsign):
           self.appMain(callsign)

    def getVersion(self):
       return VERSION

    def create_mult_dict(self, indexList):
       multDict = dict()
       for i in indexList:
          multkey = i.upper().strip()
          multDict[multkey] = 0
       return multDict

    def setMult(self, mult, multval, logtime):
       retval = False
       if (mult in self.mults.keys()):
          """Save only the earliest QSO with this county""" 
          if (self.mults[mult] == 0):
              # First time worked, save it for "last new county"
              self.mults[mult] = multval
              self.last_new_county = mult
              self.lnc_time = logtime
          retval = True
       return retval

    def getMultList(self):
        returnList = ''
        for multname in self.mults:
            if (self.mults[multname]):
                returnList += ('%s '%(multname))
        return returnList

class MOQPDBCountyRpt():
    """
    Scans the callsign log QSOs:
     1. Tracks and persists the number of Missouri Counties 
        worked.
     2. Tracks "last new county worked" and persists the 
        3 char county abreviation and time.
     3. Generates a list of county abreviations to create
        a summary.
    
    Writes summary to COUNTY table.
    
    Also displays/prints a report csv report.
    """
    def __init__(self, callsign=None):
       if (callsign):
           self.appMain(callsign)

    def updateDB(self, db, logid, ctycount, ctylist,
                           last_county_worked, time):
        did = None
        # Does record exist already?
        did = db.read_pquery("SELECT ID FROM COUNTY WHERE LOGID=%s",[logid])
        if (did):
            #update existing
            did = did[0]['ID']
            db.write_pquery(\
                "UPDATE COUNTY SET LOGID=%s,COUNT=%s,NAMES=%s, "+\
                "LASTWORKED=%s, LWTIME=%s "+\
                "WHERE ID=%s",
                [logid, ctycount, ctylist, last_county_worked, time, did])
        else:
            #insert new
            did=db.write_pquery(\
                "INSERT INTO COUNTY "+\
                "(LOGID, COUNT, NAMES, LASTWORKED, LWTIME) "+\
                "VALUES (%s, %s, %s, %s, %s)", 
                [logid,ctycount,ctylist,last_county_worked, time])
        return did

    def processOne(self, mydb, callsign, Headers = True):
        csvData = None
        #qu=QSOUtils()
        logID = mydb.CallinLogDB(callsign)
        ctys=MOQPDBCountyMults()
        #print(ctys.mults)
        countycount = 0
        countylist = ''
        if (logID):
            # Get valid QSO list for call
            log = mydb.fetchValidLog(callsign)
            # Loop through QSOS and set mults(counties)
            # present in this log
            if (len(log['QSOLIST']) > 0):
                for qso in log['QSOLIST']:
                    #logtime = qu.qsotimeOBJ(qso['DATE'], qso['TIME'])
                    logtime = qso['DATETIME']
                    ctys.setMult(qso['URQTH'], qso['ID'], logtime)
                #print(ctys.mults,ctys.last_new_county,ctys.lnc_date,ctys.lnc_time)
                countycount = ctys.sumMults()
                countylist = ctys.getMultList()
                #print(countycount, countylist)
            # Build report for this log
            if (Headers):
                csvData = COLUMNHEADERS
            else:
                csvData = ''
            csvData += ('%s\t%s\t%s\t'%(callsign,
                                   log['HEADER']['OPERATORS'], 
                                   log['HEADER']['LOCATION']))
            # Get total county count
            csvData += ('%d\t'%(ctys.sumMults())) 
            # Get list of counties worked
            csvData += ('%s\t'%(ctys.getMultList()))
            csvData += ('%s/%s UTC'%(ctys.last_new_county,
                                      ctys.lnc_time))
            #print(csvData)
            self.updateDB(mydb, logID, 
                                countycount, 
                                countylist,
                                ctys.last_new_county,
                                ctys.lnc_time)
        return csvData
           
    def processAll(self, mydb):
        csvdata = []
        #LOGID, COUNT, NAMES, LASTWORKED, LWTIME
        mydb.write_query('DROP TABLE IF EXISTS COUNTY;')
        mydb.write_query('CREATE TABLE COUNTY ('+\
          'ID int NOT NULL AUTO_INCREMENT, '+\
          'LOGID int NULL, '+\
          'COUNT int NULL, '+\
          'NAMES VARCHAR(600), '+\
          'LASTWORKED VARCHAR(6), '+\
          'LWTIME DATETIME, '+\
          'PRIMARY KEY (ID));')
        headers = True
        loglist = mydb.fetchLogList()
        if (loglist):
            Headers = True
            for nextlog in loglist:
                #print(nextlog)
                csvd=self.processOne(mydb, 
                               nextlog['CALLSIGN'], Headers)
                csvdata.append(csvd)
                Headers = False
            #print(csvdata)
        return csvdata
    
    def appMain(self, callsign):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (callsign == 'allcalls'):
           csvdata = self.processAll(mydb)
           for csvLine in csvdata:
               print(csvLine)
       else:
           csvdata = self.processOne(mydb, callsign)
           print(csvdata)

class MostCounties():
    """
    Same as MOQPDBCountyRpt() except data is read from
    the COUNTY table.
    """
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsvsumdata(self, log):
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
           csvdata += ('%d\t'%(log['COUNT']))
           csvdata += ('%s\t'%(log['NAMES']))
           if(log['LASTWORKED']):         
               csvdata += ('%s/%s UTC'%(log['LASTWORKED'],
                                        log['LWTIME']))         

       return csvdata

    def fetchSummary(self, mydb, call='allcalls'):
        sumdata = None
        query = 'SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, '+\
                'LOGHEADER.LOCATION, '+\
                'LOGHEADER.OPERATORS, COUNTY.* '+\
                'FROM COUNTY INNER JOIN LOGHEADER ON '+\
                'LOGHEADER.ID=COUNTY.LOGID '
        if (call != 'allcalls'):
            query += 'WHERE CALLSIGN=\'%s\' '%(call)
        else:
            query += 'ORDER BY COUNTY.COUNT DESC, LWTIME ASC'
        sumdata = mydb.read_query(query)
        return sumdata
        
    def ProcessData(self, call):
       ReportList = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       if (call == 'html'):
           tcall='allcalls'
       else:
           tcall=call
       data = self.fetchSummary(mydb, tcall)
       if (data):
           if (call == 'html'):
               #print('html export')
               Report = self.htmlExport(data)
               ReportList = [Report]
           else:
               ReportList = []
               for ent in data:
                   ReportList.append(self.exportcsvsumdata(ent))
       return ReportList

    def htmlExport(self, data):
        from htmlreports import HTMLReports
        html=HTMLReports('Most Counties Worked')
        html.doc += """
           <style>
              table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
               }

              th {
                font-family: consolas, helvetica, sans-serif;
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
                background-color: #99ccff;
              }

              td {
                font-family: consolas, helvetica, sans-serif;
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
              }


              tr:nth-child(even) {
                background-color: #dddddd;
              }
           </style>
           """
        html.headerend()
        html.bodystart()
        html.doc += """
        <h1>2020 Missouri QSO Party Most Counties Worked</h1>
        <p> 
        <table>
        <caption>MOST COUNTIES</caption>
        <tbody>
        <tr>
        <th><strong>RANK</strong></th>
        <th><strong>CALLSIGN</strong></th>
        <th><strong>OPERATORS</strong></th>
        <th><strong>LOCATION</strong></th>
        <th><strong>COUNTY <br /></strong><strong>COUNT</strong></th>
        <th><strong>COUNTY NAMES</strong></th>
        <th><strong>LAST COUNTY WORKED /TIME</strong></th>
        </tr>
        """       
        if (data):
           rank = 0
           for ent in data:
               rank += 1
               rankstg = ' '
               if (rank < 3):
                   rankstg = '%d'%(rank)
               lwcText=' '
               if(ent['LASTWORKED']):         
                   lwcText = '%s/%s UTC'%(ent['LASTWORKED'],
                                          ent['LWTIME'])

               html.tablerow([ [rankstg, ''],
                               [ent['CALLSIGN'],''],
                               [ent['OPERATORS'],''],
                               [ent['LOCATION'],''],
                               [ent['COUNT'],''],
                               [ent['NAMES'],''],
                               [lwcText,'']
                             
                             ], '')                               
           
        html.doc += """
        </tbody>
        </table>
        </p>
        """
        html.bodyend()
        html.docEnd()
        #html.showDoc
        return html.doc

    def appMain(self, callsign):
       csvdata = 'No Data.'
       csvList = self.ProcessData(callsign)
       if (csvList):
           if(callsign != 'html'):
               print(COLUMNHEADERS)
           for line in csvList:
               print(line)

