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

    def processAndDisplay(self):
        log = self.checkLog(self.logName, self.sw_cabBonus)
        if (log):
            self.log = log
            #print (log['RAWTEXT'])
        else:
            data = ('File %s is not a valid MOQP log file'\
                                          %(self.logName))
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
        for errs in log["ERRORS"]:
            line = 'E%s - %s\n'%(k, errs)
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, line) 
            k += 1
        #check.showLog(log)
        if (self.sw_loadLogs):
            #local=MOQPLoadLogs()
            
            result = self.loadToDB(log,
                            self.sw_acceptErrors,
                            self.sw_replaceExisting)
            print('Load to database = %s'%(result))
        
        return log
