import os
from moqputils.moqploadlogs import MOQPLoadLogs

class runLogCheck(MOQPLoadLogs):

    def __init__(self, filename, 
                       widget,
                       cabbonus,
                       loadLogs,
                       acceptErrors,
                       replaceExisting):
        self.logName = filename
        self.sw_cabBonus = cabbonus
        self.sw_loadLogs = loadLogs
        self.sw_acceptErrors = acceptErrors
        self.sw_replaceExisting = replaceExisting
        self.widget = widget

    def showDebugLog(self, log):
        print (dir(log))
        print(log.keys())
        keys = log.keys()
        for key in keys:
            print('log[%s]:\n%s'%(key, log[key]))
            
    def displayRawLog(self):
        """ 
        Display raw log file data in main window
        """
        textbuffer=self.widget.get_buffer()
        end_iter = textbuffer.get_end_iter()
        textbuffer.insert(end_iter, 'LOG HEADER:\n') 
        """
        Show HEADER
        """
        data = self.log['RAWTEXT']
        k = 0
        while ( data[k].upper().startswith('QSO:') != True ):
            end_iter = textbuffer.get_end_iter()
            line = 'H%s - %s'%(k+1, data[k])
            textbuffer.insert(end_iter, line) 
            k+=1
        """
        Show QSOs
        """
        j=1
        end_iter = textbuffer.get_end_iter()
        textbuffer.insert(end_iter, '\nLOG QSOs:\n') 
        while (k < len(data)):
            line = 'Q%s - %s'%(j, data[k])
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, line) 
            k+=1
            j+=1
        """
        Show errors
        """
        #print('Header Errors: %s'%(log['HEADER']['ERRORS']))
        end_iter = textbuffer.get_end_iter()
        textbuffer.insert(end_iter, '\nLOG ERRORS:\n') 
        k=1
        for errs in self.log["ERRORS"]:
            line = 'E%s - %s\n'%(k, errs)
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, line) 
            k += 1
    
    def processAndDisplay(self, log,):
        result = None
        self.log = None
        #log = self.checkLog(self.logName, self.sw_cabBonus)
        if (log):
            self.log = log
            #print (log['RAWTEXT'])
            self.displayRawLog()
            fileOnly = os.path.basename(self.logName)
            Result = 'File %s summary displayed'%(fileOnly)
            if (len(log['ERRORS']) >0 ):
                Result += ' - ERRORS DETECTED'
            if (self.sw_loadLogs):
            
                status = self.loadToDB(log,
                            self.sw_acceptErrors,
                            self.sw_replaceExisting)
                Result += '\nFile %s loaded to database = %s'%(fileOnly, status)
        else:
            Result = 'File %s is not a valid MOQP log file'\
                                          %(self.logName)
        return Result
