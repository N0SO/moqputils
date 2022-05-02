#!/usr/bin/env python3
"""
fixoldloggers   - Utility to remove the sequence / serial number
                  fields from MOQP file created with old versions
                  of writelog
                
Update History:
* Wed Apr 27 2022 Mike Heitmann, N0SO <n0so@arrl.net>
-V0.0.1 - Just getting started
"""

from moqputils.moqplogfile import MOQPLogFile

class fixOldLoggers(MOQPLogFile):

    BADLOGGERS = ['WRITELOG V11']

    """ 
    Over ride method initLog to add room for the updated
    log file (FIXEDLOG)
    """
    def initLog(self):
        #Initialize RAWLOG, HEADER and QSOLIST
        MOQPLogFile.initLog(self) 
        """Add FIXEDLOG - should hold new log with 
        extra fields removed."""
        self.FIXEDLOG = None 
    """ 
    Two new methods:
    fixQSO - fixes a single QSO line removing the extra
             sequence fields,
    
    fixQSOList - Removes the extra fields from all qsos in a 
                 list of QSOs by calling fixQSO for each record.  
                 
    isLoggerObsolete - Takes one parameter: The string from the 
                       log header CREATED-BY: tag. the string
                       will be compared to known obsolete versions
                       of logging software that still insert seq.
                       numbers in QSO field# 7 and 11 and return
                       True if the string matches, or False if not.
                      
    """          
    def fixQSO(self, qso):
        newQSO = None
        qso = qso.upper()
        #Split off the 'QSO:' text
        tagpos = qso.find('QSO:')
        qsoData=self.packLine(qso[tagpos+4:])
        """
        linesplit = qso.split(':')
        lineparts = len(linesplit)
        #print('%d Split data items: %s, %s'%(lineparts, linesplit[0],linesplit[1].strip()))
        qsoTag=linesplit[0].strip()
        qsoData = linesplit[1].strip()
        """
        temp = qsoData.replace(':','')
        qsoParts = temp.split(' ')
        qsoLen = len(qsoParts)
        
        """7th [6] and 11th [10] fields are seq numbers in
        obsolete log - skip them."""
        if (qsoLen >= 12):
            newQSO = 'QSO: %s %s %s %s %s %s %s %s %s %s'%(\
                                                      qsoParts[0],
                                                      qsoParts[1],
                                                      qsoParts[2],
                                                      qsoParts[3],
                                                      qsoParts[4],
                                                      qsoParts[5],
                                                      qsoParts[7],
                                                      qsoParts[8],
                                                      qsoParts[9],
                                                      qsoParts[11])
        
         
        return newQSO
        
    def fixQSOList(self, qsolist):
        newList = []
        for qso in qsolist:
            newList.append(self.fixQSO(qso))
        return newList
        
    def isLoggerObsolete(self, createdBy):
        loggerIsObsolete = False
        logApp = createdBy.strip().upper()
        for v in self.BADLOGGERS:
            if (v in logApp):
               loggerIsObsolete = True
               break
        return loggerIsObsolete
    

    """
    Over ride method buildLog() to insert (or tack on)
    the code to detect and remove extra fields.
    """
    def buildLog(self, Log=None, Persist = True):
        logF = None # Returned if errors happen!
        """
        Call the parent and let it create the data
        with errors. Make sure to set Persist = True
        so the RAWLOG and HEADER variables get populated.
        QSOLIST will be as well, bit it will be replaced
        with our data if sequence fields exist in the log
        """
        log=MOQPLogFile.buildLog(self, Log, Persist=True)
        """
        print('RAWLOG={}\n\nHEADER={}\n\nQSOLIST={}'.format(\
          self.RAWLOG,
          log['HEADER'], 
          log['QSOLIST']))"""
        
        """Now we have the log - was it created by one of the
        old logging programs we know about?"""        
        if (self.isLoggerObsolete(log['HEADER']['CREATED-BY'])):
            #Yes, obsolete - remove seq fields if they exist.
            #print('Obsolete logger detected!')
            #Get a fresh copy of the QSO list
            #print('RAWLOG = '.format(self.RAWLOG))
            loglist = self.getLogList(self.RAWLOG)
            tlog = self.getLogdictData(self.RAWLOG)
            """Remove extra fields from QSO list and
               build list of dict indexed qsos."""
            fixedQList = self.fixQSOList(tlog['QSOLIST'])
            fixedDictList = self.buildQSOList(fixedQList)

            """
            Populate FIXEDLOG as a LIST of lines (no dict 
            objects) representing the adjusted log file.
            """
            self.FIXEDLOG = self.buildFixedList(loglist, 
                                                 fixedQList)
            """
            Build new log to return
            """
            logF = dict()
            logF['HEADER'] = log['HEADER']
            if ('SOAPBOX' in logF['HEADER']):
                logF['HEADER']['SOAPBOX'] += \
                'Obsolte Sequence numbers removed by fixoldloggers.py.'
            logF['QSOLIST'] = fixedDictList
        else:
            #Nothing to do, return log provided by parent.
            logF = log
            
        return logF
        
    def buildFixedList(self, header, newqsos):
        newLogList = []

        hIndex = 0
        while not(header[hIndex].strip().upper().startswith('QSO:')):
            newLogList.append(header[hIndex])
            hIndex += 1

        newLogList.append(\
        'SOAPBOX: Obsolte Sequence numbers removed by fixoldloggers.py.')
        
        for line in newqsos:
            newLogList.append(line)
            
        return newLogList