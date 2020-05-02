#!/usr/bin/env python3
"""
MOQPLoadLogs - Inherits code from MOQPLogCheck.
Enhances QSO and header verification and will write
log header, QSO list and status of the CABRILLO Bonus 
to the database. The same reports and file sorting 
available in moqplogcheck may be printed, but the 
results are NOT save to the database.

Update History:
* Thu Apr 29 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Retired code from 2019 QSO Party
- and added enhanced log header/QSO checking
- by inheriting from MOQPLogCheck
"""
from moqplogcheck import MOQPLogcheck
import os
from moqpdbconfig import *
from moqpdbutils import *
#from bothawards import BothAwards
#import MySQLdb


VERSION = '0.1.0' 


class MOQPLoadLogs(MOQPLogcheck):

    def __init__(self, filename = None, 
                       errcopypath = None,
                       cabbonus = False):
        if (filename):
           if (filename):
              self.appMain(filename, errcopypath, cabbonus)


    def loadToDB(self, log, cabBonus):
        sucsess = False
        call = log['HEADER']['CALLSIGN']
        if (log['ERRORS'] == []):
            mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            if (mydb):
                mydb.setCursorDict()
                testID = mydb.CallinLogDB(call)
                if (testID):
                    print('Log for %s already exists as ID %s - use UPDATE to load new log data'%(call, testID))
                else:
                    newLogID = mydb.write_header(log['HEADER'], cabBonus)
                    print('New log ID = %d -- writing QSOS...'%(newLogID))
                    mydb.write_qsolist(newLogID, log['QSOLIST'])
            else: 
                print('Error opening database - log %s data not written to database.'%(callsig))
        else: # Log has errors 
            print('Log %s has errors - data not written to database.'%(callsig))
        return sucsess
    

    def processOneFile(self, filename, headers=True, cabBonus=False):   
       csvdata = None        
       if (os.path.isfile(filename)):
          log = self.checkLog(filename)
          if (log):
              self.loadToDB(log, cabBonus)
          else:
              csvdata = ( \
               'True\tFile %s is not in MOQP Cabrillo format.\n'\
                                                     %(filename))
       return csvdata 

    def appMain(self, pathname, errcopypath, cabbonus):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.processOneFile(pathname, 
                                        errcopypath, 
                                        cabbonus)
       else:
          csvdata = self.processFileList(pathname, errcopypath)
       if (csvdata):
          print('%s'%(csvdata))

if __name__ == '__main__':
    app = MOQPLoadLogs()
    print('Class MOQPLoadLogs() Version %s'%(app.getVersion))

