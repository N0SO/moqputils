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
"""

from moqpdbutils import *


VERSION = '0.0.1' 

COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\t' + \
                'CW QSO\tPH QSO\tRY QSO\tQSO COUNT\tVHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\t' +\
                'DIGITAL\tVHF\tROOKIE\n'

class MOQPDBCatReport():
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def exportcsvdata(self, log, Headers=True):
       """
       This method processes a single log file passed in filename
       and returns the summary ino in .CSV format to be printed
       or saved to a .CSV file.
    
       If the Headers option is false, it will skip printing the
       csv header info.
       """
       csvdata = None

       if (log):
       
           if (Headers): 
               csvdata = COLUMNHEADERS
               
           else:
               csvdata = ''
               
           cw = int(log['SUMMARY']['CWQSO'])
           ph = int(log['SUMMARY']['PHQSO'])
           ry = int(log['SUMMARY']['RYQSO'])
           qsocount = cw + ph + ry

           csvdata += ('%s\t'%(log['HEADER']['CALLSIGN']))
           csvdata += ('%s\t'%(log['HEADER']['OPERATORS']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-STATION']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OPERATOR']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-POWER']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-MODE']))
           csvdata += ('%s\t'%(log['HEADER']['LOCATION']))
           csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY']))
           csvdata += ('%s\t'%(log['SUMMARY']['CWQSO']))
           csvdata += ('%s\t'%(log['SUMMARY']['PHQSO']))
           csvdata += ('%s\t'%(log['SUMMARY']['RYQSO']))
           csvdata += ('%d\t'%(qsocount))
           csvdata += ('%s\t'%(log['SUMMARY']['VHFQSO']))
           csvdata += ('%s\t'%(log['SUMMARY']['MULTS']))         
           csvdata += ('%s\t'%(log['SUMMARY']['QSOSCORE']))         
           csvdata += ('%s\t'%(log['SUMMARY']['W0MABONUS']))         
           csvdata += ('%s\t'%(log['SUMMARY']['K0GQBONUS']))         
           csvdata += ('%s\t'%(log['SUMMARY']['CABBONUS']))         
           csvdata += ('%s\t'%(log['SUMMARY']['SCORE']))         
           csvdata += ('%s\t'%(log['SUMMARY']['MOQPCAT']))
           csvdata += ('%s\t'%(log['SUMMARY']['DIGITAL']))
           csvdata += ('%s\t'%(log['SUMMARY']['VHF']))
           csvdata += ('%s\t'%(log['SUMMARY']['ROOKIE']))

       else:
          csvdata = ('No log data in databas for .'%callsign)
       return csvdata

    def getLog(self, mydb, call):
        log = dict()
        logdata = mydb.fetchValidLog(call)
        log['HEADER']= logdata['HEADER']
        log['QSOLIST'] = logdata['QSOLIST']
        logdata = mydb.fetchLogSummary(call)
        log['SUMMARY'] = logdata
        return log
       
        
    def processOne(self, mydb, callsign, Headers = True):
        csvData = None
        logID = mydb.CallinLogDB(callsign)
        if (logID):
            log = self.getLog(mydb, callsign)
            csvData = self.exportcsvdata(log, Headers)
            #print(csvData)
        else:
           csvData = ('No log data for call %s.'%(callsign))
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
