#!/usr/bin/env python3
"""
MOQPLoadLogs - Inherits code from MOQPLogCheck.
Enhances QSO and header verification and will write
log header, QSO list and status of the CABRILLO Bonus 
to the database. The same reports and file sorting 
available in moqplogcheck may be printed, but the 
results are NOT save to the database.

Update History:
* Thu Apr 29 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Retired code from 2019 QSO Party
- and added enhanced log header/QSO checking
- by inheriting from MOQPLogCheck
* Tue May 08 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Handle CABRILLO Bonus.
- Accept logs with errors beyond DUPES.
- Allow updating (replacing) an existing log.
* Sun May 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.2 - Added:
-     CABRILLO bonus processing and improved 
-     Accept errors processing
-     Update existing log processing
-     Improved error handling.
* Fri Feb 05 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.3 - Added:
-     Updated module path for new structure.
-     Minor tweaks to support working with GUI
* Fri Feb 16 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.4 - Added:
-     Moved common QSO processing methods to module
-     moqpcategory for better sharing between functions.
* Tue Feb 23 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.5 - Added:
-     Moved common QSO processing methods to module
-     moqpqsoutils for better sharing between functions.
* Wed Mar 10 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.6
- Updates to method processFileList() to process only
- the top level directory and skip sub-directories.


"""
import os, shutil
import MySQLdb
from moqputils.moqplogcheck import MOQPLogcheck
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpdbutils import *
#from cabrilloutils.qsoutils import QSOUtils
#from moqputils.bothawards import BothAwards




class MOQPLoadLogs(MOQPLogcheck):

    def __init__(self, filename = None, 
                       acceptedpath = None,
                       cabbonus = False,
                       errorsOK = False,
                       updateOK = False):
        self.VERSION = '0.1.5' 
        if (filename):
           if (filename):
              self.appMain(filename, 
                           acceptedpath, 
                           cabbonus,
                           errorsOK,
                           updateOK)

    def getVersion(self):
        return self.VERSION

    def loadToDB(self, log, errorsOK, updateOK):
        sucsess = False
        #print(log)
        #exit()
        call = log['HEADER']['CALLSIGN']
        dupecount = log['QSOSUM']['DUPES']
        #errorcount = len(log['ERRORS'])
        errorcount = log['QSOSUM']['INVALID']
        cabBonus = log['BONUS']['CABRILLO']
        if (cabBonus):
            print('Applying CABRILLO Bonus to %s'%(call))
        if ( errorsOK or log['HEADERSTAT']['STAT'] and  \
                    ( (errorcount == 0) or \
                      (errorcount == dupecount) ) ):
            """ Errors allowed from command line options OR
                no errors exist OR errors are only DUPES. Load
                this log.""" 
            mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            if (mydb):
                mydb.setCursorDict()
                testID = mydb.CallinLogDB(call)
                if (testID ):
                    if (updateOK):
                        mydb.delete_log(call)
                    else:
                        print('Log for %s already exists as ID %s - use UPDATE to load new log data'% \
                        (call, testID))
                        return sucsess
                #else:
                #print(log['HEADER'])
                newLogID = mydb.write_header(log['HEADER'], cabBonus)
                if (newLogID):
                        #print('New log ID = %d for %s -- writing QSOS...'%(newLogID, call))
                        result = mydb.write_qsolist(newLogID, log['QSOLIST'])
                        if (result):
                            sucsess = True
                        else:
                            print("Error writing QSO list for call %s to database."%(call))
                            #exit()
                            
                else:
                        print("Error writing log header for call %s"%(call))
                        #exit()
            else: 
                print('Error opening database - log %s data not written to database.'%(callsig))
        else: # Log has errors 
            print('Log %s has errors - data not written to database.'%(call))
        return sucsess
    

    def processOneFile(self, filename, 
                             destpath = False,
                             cabBonus=False,
                             errorsOK=False,
                             updateOK=False):
       #qutil = QSOUtils()   
       csvdata = ''       
       if (os.path.isfile(filename)):
          log = self.checkLog(filename, cabBonus)
          if (log):
              if ( self.loadToDB(log,errorsOK, updateOK)):
                  print('File %s  successfully loaded to database.'%(filename))
                  if (destpath): 
                     if (os.path.exists(destpath)):
                        try:
                          dest = shutil.move(filename, destpath)
                          print('mv %s %s'%(filename, destpath))
                        except Exception as e:
                          print('Move of %s to %s failed\n%s!'% \
                                                     (filename,
                                                      destpath,
                                                      e.args))

              else:
                  print("1\tLog File Errors - %s data NOT written to database."%(filename))
          else:
              csvdata = ( \
               '1\tFile %s is not in MOQP Cabrillo format.\n'\
                                                     %(filename))
       return csvdata 

    def processFileList(self, pathname, 
                              destpath=None, 
                              cabBonus=False,
                              errorsaccepted=False,
                              updatelog=False):
        csvdata = ''
        for (dirName, subdirList, fileList) in  \
                      os.walk(pathname, topdown=True):
           if (fileList != ''): 
              #print (fileList)
              for fileName in fileList:
                 #print(fileName)
                 if (fileName.startswith('.')):
                     pass
                 else:
                     fullPath = ('%s/%s'%(dirName, fileName))
                     thislog = self.processOneFile(fullPath, 
                                           destpath,
                                           cabBonus,
                                           errorsaccepted,
                                           updatelog)
                     csvdata += thislog
              break # Only process top level files, not sub directorioes
           else: 
              csvdata += ('1\tNo files in folder'% \
                          (pathName))
        return csvdata


    def appMain(self, pathname, 
                      acceptedpath, 
                      cabbonus,
                      errorsOK,
                      updateOK):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.processOneFile(pathname, 
                                        acceptedpath, 
                                        cabbonus,
                                        errorsOK,
                                        updateOK)
       else:
          csvdata = self.processFileList(pathname, 
                                         acceptedpath,
                                         cabbonus,
                                         errorsOK,
                                         updateOK)
       if (csvdata):
          print('%s'%(csvdata))

if __name__ == '__main__':
    app = MOQPLoadLogs()
    print('Class MOQPLoadLogs() Version %s'%(app.getVersion()))

