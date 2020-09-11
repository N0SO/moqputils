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
"""

from contestmults import *
from moqpdbutils import *
from moqpdbconfig import *

VERSION = '0.0.2'

MULTFILES = ['shared/multlists/moqp-counties.csv']

COLUMNHEADERS = 'CALLSIGN\tOPS\tLOCATION\tCOUNTY COUNT\t '+\
                'COUNTY NAMES\tLAST COUNTY WORKED/TIME\n'

class MOQPDBCountyMults(ContestMults):
    def __init__(self, callsign=None):
       self.mults = self.readmultlists(MULTFILES)
       #print(self.multlist, mult, multval, date, time)
       self.last_new_county = ''
       self.lnc_date = ''
       self.lnc_time = ''
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

    def setMult(self, mult, multval, date = None, time = None):
       retval = False
       if (mult in self.mults.keys()):
          if (self.mults[mult] == 0):
              """Save only the first QSO""" 
              self.mults[mult] = multval
              self.last_new_county = mult
              self.lnc_date = date
              self.lnc_time = time
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
    Scans the callsign log QSOs counts number of 
    Missouri Counties worked and generates a list of
    county abreviations to create a summary.
    
    Writes summary to COUNTY table.
    
    Also displays/prints a report csv report.
    """
    def __init__(self, callsign=None):
       if (callsign):
           self.appMain(callsign)

    def updateDB(self, db, logid, ctycount, ctylist,
                           last_county_worked, date, time):
        did = None
        # Does record exist already?
        did = db.read_pquery("SELECT ID FROM COUNTY WHERE LOGID=%s",[logid])
        if (did):
            #update existing
            did = did[0]['ID']
            db.write_pquery(\
                "UPDATE COUNTY SET LOGID=%s,COUNT=%s,NAMES=%s, "+\
                "LASTWORKED=%s,DATE=%s,TIME=%s "+\
                "WHERE ID=%s",
                [logid, ctycount, ctylist, last_county_worked, date, time, did])
        else:
            #insert new
            did=db.write_pquery(\
                "INSERT INTO COUNTY "+\
                "(LOGID, COUNT, NAMES, LASTWORKED, DATE, TIME) "+\
                "VALUES (%s, %s, %s, %s, %s, %s)", 
                [logid,ctycount,ctylist,last_county_worked, date, time])
        return did

    def processOne(self, mydb, callsign, Headers = True):
        csvData = None
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
                    ctys.setMult(qso['URQTH'], qso['ID'],
                                 qso['DATE'], qso['TIME'])
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
            csvData += ('%s - %s %s UTC'%(ctys.last_new_county,
                                      ctys.lnc_date,
                                      ctys.lnc_time))
            #print(csvData)
            self.updateDB(mydb, logID, 
                                countycount, 
                                countylist,
                                ctys.last_new_county,
                                ctys.lnc_date,
                                ctys.lnc_time)
        return csvData
           
    def processAll(self, mydb):
        csvdata = []
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
           csvdata += ('%s - %s %s'%(log['LASTWORKED'],
                                     log['DATE'],
                                     log['TIME']))         

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
            query += 'ORDER BY COUNTY.COUNT DESC'
        sumdata = mydb.read_query(query)
        return sumdata
        
    def ProcessData(self, call):
       ReportList = None
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       data = self.fetchSummary(mydb, call)
       if (data):
           ReportList = []
           for ent in data:
               ReportList.append(self.exportcsvsumdata(ent))
       return ReportList

    def appMain(self, callsign):
       csvdata = 'No Data.'
       #mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       #mydb.setCursorDict()
       csvList = self.ProcessData(callsign)
       if (csvList):
           print(COLUMNHEADERS)
           for line in csvList:
               print(line)

