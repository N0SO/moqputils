#!/usr/bin/env python3
"""
MOQPLogcheck  - Check logs submitted for the ARRL Missouri
QSO Party and determine if the file will load correctly into
the MOQP SQL database. Look for the following:
    1. Verify the file is a CABRILLO file.
    2. Look for the following CABRILLO header tags:
        A) CALLSIGN: is populated.
        B) EMAIL: is populated.
        C) LOCATION: is populated and valid.
        D) The CATEGORY- fields have enough info
           to determine the MOQP category:
                i) - STATION:
               ii) - OPERATOR:
              iii) - POWER:
               iv) - MODE:
    3. Review QSO: lines and verify:
         A) QSO Date / time fall within contest times.
         B) FREQUENCY / BAND is in-band.
         C) MYCALL matches CALLSIGN:
         D) MYREPORT is valid
         E) MYQTH matches LOCATION:
                i) - 3 char county code for MO stations
               ii) - State, Provinance or DX for non-MO
         F) URCALL is populated.
         G) URREPORT is valid
         H) URQTH is a 3 char county code, state, prov or DX.
    4. DUPE checks.
    5. Determine contacts with BONUS stations.
    6. Summarize QSOS and compute perliminary score.
    7. Determine SHOWME and MISSOURI certificate status.

Update History:
* Tue Apr 14 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
- Same basic funtion as moqpcategory.py
* Thu Apr 16 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Added enhanced log header verification.
- Steps 1 & 2 above.
* Thu Apr 17 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3 - Added DUPE and BONUS checks.
* Mon Apr 27 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.4 - Added ERROR flags for sorting of files with errors.
* Mon Apr 29 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.5 - Added Added option to move logs with errors to
- another folder.
* Sun May 10 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.6 - Added CABRILLO bonus processing and improved 
- error handling.
* Wed May 20 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.7 - Added QTH checks to qso_valid. Marked
- QSOs that fail checks as errors.
- Moved common definitions of counties, state, modes, etc.
- to moqpdefs.py. 
- Began consolidation of qso_valid code ( we had three 
- methods with that name).
* Tue Feb 16 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.8 - Made qso date / time a datetime object instead of
-          separate strings for date and time.
* Wed Feb 17 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.9 - Updated to use MOQPQSOUtils as parent cllass
* Sat Feb 20 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Updated getMOQPLog to add raw log text to the
-          dict object log it returns as key RAWTEXT.
* Mon Feb 22 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 
- Removed code duplicated in MOQPCategory and MOQPQSOUtils
* Tue Feb 23 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.2
- Moved the more up-to-date file processing code out of
- MOQPLogCheck to the parent class MOQPCategory for
- efficiency and consistancy:
-        checkLog()
-        headerReview()
-        errCopy()
-        
* Fri Feb 26 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.3
- Removed redundant definition of QSOTAGS

"""

from moqputils.moqpcategory import MOQPCategory
from moqputils.bonusaward import BonusAward

import os, shutil

from moqputils.moqpdefs import *

class MOQPLogcheck(MOQPCategory):
    """
    QSOTAGS = ['FREQ', 'MODE', 'DATETIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH', 'NOTES']
    """
    def __init__(self, filename = None, 
                       acceptedpath = None,
                       cabbonus = None):
        self.VERSION = '0.1.3'
        self.cabbonus = cabbonus
        if (filename):
           if (filename):
              self.appMain(filename, acceptedpath, cabbonus)

    def getVersion(self):
       return self.VERSION

    def processOneFile(self, filename, 
                             headers=True, 
                             acceptedMovePath=None,
                             cabbonus=False): 
       dupecount = None
       errorcount = None
       logAccepted = False              
       if (os.path.isfile(filename)):
          print(filename)
          log = self.checkLog(filename, cabbonus)
          if (log):
             call = log['HEADER']['CALLSIGN']
             dupecount = log['QSOSUM']['DUPES']
             #print('MOQPLogCheck.processOneFile: qsosummary = \n{}\n\nHeader status=\n{}'.format(log['QSOSUM'], log['HEADERSTAT']))
             #errorcount = len(log['ERRORS'])
             #print("errorcount = %d, DUPE count = %d, PATH = %s"%(errorcount, dupecount, acceptedMovePath))
             #if ( (errorcount == dupecount) and (): logAccepted = True
             if ( log['HEADERSTAT']['STAT'] and
                   (log['QSOSUM']['QSOS'] > 0) and
                   (log['QSOSUM']['INVALID'] == log['QSOSUM']['DUPES']) ):
                logAccepted = True
             csvdata = self.exportcsv(log, headers)
             print('{} Log accepted = \t{}'.format(call, logAccepted))
             #print ('csvdata = ',csvdata)
             
             if (csvdata == None):
                csvdata = ('True\tFile %s is not in MOQP Cabrillo format Dude.\n'\
                         %(filename))
          else:
             csvdata = ('True\tFile %s is not in MOQP Cabrillo format.\n'\
                         %(filename))
       else:
          csvdata = ('True\tLog File %s does not exist\n'% \
                          (filename))
       if (logAccepted and acceptedMovePath): 
          if (os.path.exists(acceptedMovePath)):
              # Move to accepted logs folder 
              try:
                 dest = shutil.move(filename, acceptedMovePath)
                 print('mv %s %s'%(filename, acceptedMovePath))
              except Exception as e:
                 print('Move of %s to %s failed\n%s!'% \
                                             (filename,
                                              acceptedMovePath,
                                              e.args))

       return csvdata 

    def processFileList(self, pathname, 
                              acceptedPath=None,
                              cabbonus=False):
        csvdata = ''
        for (dirName, subdirList, fileList) in  \
                      os.walk(pathname, topdown=True):
           if (fileList != ''): 
              Headers = True
              for fileName in fileList:
                 if (fileName.startswith('.')):
                     pass
                 else:
                     fullPath = ('%s/%s'%(dirName, fileName))
                     thislog = self.processOneFile(fullPath, 
                                                   Headers,
                                                   acceptedPath,
                                                   cabbonus)
                     csvdata += thislog
                     Headers = False
           else: 
              csvdata += ('True\tLog File %s does not exist\n'% \
                          (fileName))
        return csvdata

    def appMain(self, pathname, acceptedpath, cabbonus):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.processOneFile(pathname, 
                                        True, 
                                        acceptedpath,
                                        cabbonus)
       else:
          csvdata = self.processFileList(pathname, 
                                         acceptedpath,
                                         cabbonus)
       if (csvdata):
          print('%s'%(csvdata))
