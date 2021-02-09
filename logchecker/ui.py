#!/usr/bin/python
import gi, os, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from logchecker.treesample import TreeViewFilterWindow
from logchecker.filedialogs import my_file_open
from moqputils.moqploadlogs import MOQPLoadLogs

VERSION = '0.0.1'

class About1():
    def __init__(self):
        gtkvers='Gtk V%d.%d.%d'%(\
	         Gtk.MAJOR_VERSION,
	         Gtk.MINOR_VERSION,
	         Gtk.MICRO_VERSION)
        pyvers = 'Python V%d.%d.%d'%(\
	         sys.version_info.major,	
	         sys.version_info.minor,	
	         sys.version_info.micro)	
        verinfo = "%s\n%s"%(gtkvers, pyvers)
	
        #print(gtkvers, pyvers, verinfo) 
    
        about = Gtk.AboutDialog()
        about.set_program_name("Missouri QSO Party Log Checker")
        about.set_version('V%s'%(VERSION))
        about.set_authors(["Mike, N0SO"])
        about.set_copyright("(c) BEARS-STL")
        about.set_comments("\n%s"%(verinfo))
        about.set_website("http://n0so.net")
        about.run()
        about.destroy()

class runLogCheck(MOQPLoadLogs):

    def __init__(self, filename = None, 
                       cabbonus = None,
                       acceptedpath = None,
                       loadlog = False):
        MOQPLoadLogs.__init__(self, None, 
                       acceptedpath,
                       cabbonus)
               
        self.logName = filename
        self.acceptedPath = acceptedpath
        self.cabBonus = cabbonus  
        self.loadLog = loadlog
        """
        if (self.loadLog):
            from moqputils.moqploadlogs import MOQPLoadLogs
            self.App = MOQPLoadLogs()
        else:
            from moqputils.moqplogcheck import MOQPLogcheck
            self.App = MOQPLogcheck()
        """    
    def processData(self, logName=None):
        csvData = self.App.processOneFile(self.logName,
                                          True,
                                          self.acceptedPath,
                                          self.cabBonus)
        return csvData
         
    def showLog(self, log):
        print (dir(log))
        print(log.keys())
        keys = log.keys()
        for key in keys:
            print('log[%s] - %s'%(key, log[key]))

        #print(Data_to_Show)
        #lines = Data_to_Show.splitlines()
        #llines = lines[1].split('\t')
        #show = TreeViewFilterWindow([llines])

class Handler():

    def __init__(self):
        self.fileButton_text = None
        self.status1_text = None
        self.status2_text = None
        self.sw_cabBonus = False
        self.sw_loadLogs = False
        self.sw_acceptErrors = False
        self.sw_replaceExisting = False
        self.log = None
        self.logstatusCallback = None
        
    def set_logstatusCallback(self, callback):
        self. logstatusCallback = callback
     
    def on_win_show(self, args):
        print('on_win_show called...')

    def on_win_destroy(self, args):
        #print('args type = %s\nargs Directory:\n%s'%(args, dir(args)))
        Gtk.main_quit()
        
    def on_cabBonus_activate(self, widget):
        print('on_cabBonus_activate called...')
	
    def on_cabBonus_state_set(self, widget, state):
        print('on_cabBonus_state_set called...')
        print('widget = %s\nstate=%s\n'%(widget, state))
        self.sw_cabBonus = state
	
    def on_loadLog_state_set(self, widget, state):
        print('on_loadload_state_set called...')
        print('widget = %s\nstate=%s\n'%(widget, state))
        self.sw_loadLogs = state
        
    def on_loadLog_state_set_accept(self, widget, state):
        if (self.sw_loadLogs):
            widget.set_visible(True)
        else:
            widget.set_visible(False)
        print('on_loadLog_enable_accept called - Setting Accept Errors sw %s'%(self.sw_loadLogs))

    def on_loadLog_state_set_acceptlbl(self, widget, state):
        if (self.sw_loadLogs):
            widget.set_visible(True)
        else:
            widget.set_visible(False)
        print('on_loadLog_enable_acceptlbl called - Setting Accept Errors sw %s'%(self.sw_loadLogs))
	
    def on_loadLog_state_set_replace(self, widget, state):
        if (self.sw_loadLogs):
            widget.set_visible(True)
        else:
            widget.set_visible(False)
        print('on_loadLog_enable_replace called - Setting replace log sw %s'%(self.sw_loadLogs))

    def on_loadLog_state_set_replacelbl(self, widget, state):
        if (self.sw_loadLogs):
            widget.set_visible(True)
        else:
            widget.set_visible(False)
        print('on_loadLog_enable_replacelbl called - Setting replace log lable %s'%(self.sw_loadLogs))
        
    def on_acceptErrs_state_set(self, widget, state):
        print('on_acceptErrs_state_set called...')
        print('widget = %s\nstate=%s\n'%(widget, state))
        self.sw_acceptErrors = state
                
    def on_replaceLog_state_set(self, widget, state):
        print('on_replaceLog_state_set called...')
        print('widget = %s\nstate=%s\n'%(widget, state))
        self.sw_replaceExisting = state

    def on_AboutMenuItem_activate(self, args=None):
        about = About1()
	
    def on_fileButton_clicked(self, widget):
        #print('File Button Clicked!')  
        file1=my_file_open()
        file1.on_file_clicked(widget)

        #print('My File selected: %s'%(file1.fileName))
        if file1.fileName != None:
            self.status1_text = file1.fileName
            data = None
            try:
                with open(file1.fileName, 'r') as thisfile:
                    data = thisfile.readlines()
            except:
                data = 'Error reading file %s'%(file1.fileName)
            #self.set_label(file1.fileName)
            
            """ 
            Display raw log file data in main window
            """
            textbuffer=widget.get_buffer()
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, 'LOG HEADER:\n') 

            k = 0
            while ( data[k].upper().startswith('QSO:') != True ):
                end_iter = textbuffer.get_end_iter()
                line = 'H%s - %s'%(k+1, data[k])
                textbuffer.insert(end_iter, line) 
                k+=1
            j=1
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, '\nLOG QSOs:\n') 
            while (k < len(data)):
                line = 'Q%s - %s'%(j, data[k])
                end_iter = textbuffer.get_end_iter()
                textbuffer.insert(end_iter, line) 
                k+=1
                j+=1
                   

            check = runLogCheck(file1.fileName, self.sw_cabBonus)
            log = check.checkLog(file1.fileName, self.sw_cabBonus)
            self.log = log
            """
            if (log):
                textbuffer=widget.get_buffer()
                keys = log['HEADER'].keys()
                for key in keys:
                    linestg = ('%s %s\n'%(key, log['HEADER'][key]))
                    end_iter = textbuffer.get_end_iter()
                    textbuffer.insert(end_iter, linestg)
                k=0
                for qso in log['QSOLIST']:
                    k += 1
                    line = ('%s - '%(k))
                    keys = qso.keys()
                    for key in keys:
                        line += ('%s '%(qso[key]))
                    end_iter = textbuffer.get_end_iter()
                    textbuffer.insert(end_iter,('%s \n'%(k)) + line)
                
            """    
            #check_result = check.processData(file1.fileName)
            check.showLog(log)
            
    def set_Button_label(self, button):
        fileOnly = os.path.basename(self.status1_text)
        while len(fileOnly) < 70 :
            fileOnly += ' '
        button.set_label(fileOnly)     
        
    def set_status1(self, status1):
        fileOnly = os.path.basename(self.status1_text)
        status1.set_text(fileOnly)  
        
    def set_logstatus1(self, widget, log=None):
        if (log == None): 
            header=self.log['HEADER']
        else:
            header=log['HEADER']
            
        #print(dir(header))
        widget.append([header['CONTEST'],
                       header['CALLSIGN'],
                       header['CATEGORY-STATION'],
                       header['CATEGORY-OPERATOR'],
                       header['CATEGORY-POWER'],
                       header['CATEGORY-MODE'],
                       header['OPERATORS']])
           
    def set_logstatus2(self, widget, log=None):
        if (log == None): 
            qsosum=self.log['QSOSUM']
            bonus=self.log['BONUS']
        else:
            qsosum=log['QSOSUM']
            bonus=log['BONUS']
        #score=self.log['SCORE']   
        #print('Score = %s'%(score))
        widget.append(['%s'%(qsosum['QSOS']),
                       '%s'%(qsosum['CW']),
                       '%s'%(qsosum['PH']),
                       '%s'%(qsosum['DG']),
                       '%s'%(qsosum['VHF']),
                       '%s'%(qsosum['DUPES']),
		       '%s'%(self.log['SCORE']),
		       '%s'%(bonus['CABRILLO']),
		       '%s'%(bonus['W0MA']),
		       '%s'%(bonus['K0GQ']),
		       '%s'%(self.log['MULTS'])])
           
    def set_logstatus3(self, widget, log=None):
        if (log == None): 
            moqpcat=self.log['MOQPCAT']
        else:
            moqpcat=log['MOQPCAT']
            
        #print(dir(header))
        widget.append([moqpcat['MOQPCAT'],
                       moqpcat['LOCATION'],
                       moqpcat['VHF'],
                       moqpcat['DIGITAL'],
                       moqpcat['ROOKIE']])
           
        
class gui_MOQPLogCheck():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/logchecker.ui")
        builder.connect_signals(Handler())
        self.appMain(builder)
   
    def appMain(self, builder):
       window = builder.get_object("win")
       window.show_all()
       self.logsumTree = builder.get_object("liststore1")
       #window.Handler.set_logstatusCallback(self.logsumTree)
       #self.cNametxt = builder.get_object('cNametxt')
       #print (dir(self.logsumTree), dir(self.cNametxt))
       #self.logsumTree.append(['test1', 'test2', 'test3'])
       Gtk.main()    

if __name__ == '__main__':
    app = gui_MOQPLogCheck()

