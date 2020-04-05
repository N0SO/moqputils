#!/usr/bin/env python3
"""
moqpdbclubreport - Fetches a list of logs that have something
                   other than NULL in the Cabrillo Header field
                   CLUB. The log SUMMARY table entries for the
                   corrosponding logs is fetched and displayed
                   in the same format as MOQPDBCatReport, with
                   the CLUB field added. The result is output
                   in .csv format for further refinement in a
                   spreadsheet program such as Excel or
                   libreoffice.

                   Inherits from MOQPDBCatReport

                   Based on 2019 MOQP Rules.
                  
Update History:
* Fri Jan 31 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

from moqpdbcatreport import *


VERSION = '0.0.1' 
"""
COLUMNHEADERS = 'CALLSIGN\tOPS\tSTATION\tOPERATOR\t' + \
                'POWER\tMODE\tLOCATION\tOVERLAY\tCLUB\t' + \
                'CW QSO\tPH QSO\tRY QSO\tQSO COUNT\tVHF QSO\t' + \
                'MULTS\tQSO SCORE\tW0MA BONUS\tK0GQ BONUS\t' + \
                'CABFILE BONUS\tSCORE\tMOQP CATEGORY\t' +\
                'DIGITAL\tVHF\tROOKIE\n'
"""
COLUMNHEADERS = 'CALLSIGN\tOPS\tCLUB\tSCORE\n'

class MOQPDBClubReport(MOQPDBCatReport):
           
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
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-STATION']))
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OPERATOR']))
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-POWER']))
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-MODE']))
           #csvdata += ('%s\t'%(log['HEADER']['LOCATION']))
           #csvdata += ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY']))
           csvdata += ('%s\t'%(log['HEADER']['CLUB']))
           # csvdata += ('%s\t'%(log['SUMMARY']['CWQSO']))
           #csvdata += ('%s\t'%(log['SUMMARY']['PHQSO']))
           #csvdata += ('%s\t'%(log['SUMMARY']['RYQSO']))
           #csvdata += ('%d\t'%(qsocount))
           #csvdata += ('%s\t'%(log['SUMMARY']['VHFQSO']))
           #csvdata += ('%s\t'%(log['SUMMARY']['MULTS']))         
           #csvdata += ('%s\t'%(log['SUMMARY']['QSOSCORE']))         
           #csvdata += ('%s\t'%(log['SUMMARY']['W0MABONUS']))         
           #csvdata += ('%s\t'%(log['SUMMARY']['K0GQBONUS']))         
           #csvdata += ('%s\t'%(log['SUMMARY']['CABBONUS']))         
           csvdata += ('%s\t'%(log['SUMMARY']['SCORE']))         
           #csvdata += ('%s\t'%(log['SUMMARY']['MOQPCAT']))
           #csvdata += ('%s\t'%(log['SUMMARY']['DIGITAL']))
           #csvdata += ('%s\t'%(log['SUMMARY']['VHF']))
           #csvdata += ('%s\t'%(log['SUMMARY']['ROOKIE']))

       else:
          csvdata = ('No log data in databas for .'%callsign)
       return csvdata

    def processAll(self, mydb):
        csvdata = []
        headers = True
        loglist = mydb.read_query( \
               "SELECT ID, CALLSIGN FROM logheader WHERE CLUB!='' ORDER BY CLUB ASC")
        #loglist = mydb.fetchLogList()
        #print(loglist)
        #print(len(loglist))
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
        else:
            print('No logs.')

    def appMain(self, callsign):
       csvdata = ['No Data.']
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       csvdata = self.processAll(mydb)
       for csvLine in csvdata:
           print(csvLine)

