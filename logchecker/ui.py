#!/usr/bin/python
import gi, os, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from logchecker.filedialogs import my_file_open
from moqputils.moqploadlogs import MOQPLoadLogs
from logchecker.__init__ import VERSION

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
        about.set_copyright("(c) BEARS-STL 2021")
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
    
    def showLog(self, log):
        print (dir(log))
        print(log.keys())
        keys = log.keys()
        for key in keys:
            print('log[%s]:\n%s'%(key, log[key]))

class Handler():

    def __init__(self):
        #print('Handler starting...')
        #print("I'm a %s."%(type(self)))
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
     
    def on_win_show(self, args = None):
        print('on_win_show called...')
        
    def childview(self, parent):
        try:
            childlist = parent.get_children()
        except:
            childlist = []
        print('%s has %d children...'%(parent.get_name(), len(childlist)))
        for child in childlist:
            self.childview(child)

    def on_win_destroy(self, args):
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

    def on_New1_activate(self, args=None):
        print('on_New1_activate called')
        self.fileButton_text = None
        self.status1_text = None
        self.status2_text = None
        self.sw_cabBonus = False
        self.sw_loadLogs = False
        self.sw_acceptErrors = False
        self.sw_replaceExisting = False
        self.log = None
        self.logstatusCallback = None
        texwin = self.get_descendant(args,'textWindow')
        buffer = texwin.get_buffer()
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
        filebutton = self.get_descendant(args,'fileButton')
        self.set_Button_label(filebutton)
        stat1 = self.get_descendant(args,'status1')
        self.set_status1(stat1)

    def clear_list_store(self, liststore):
        if (type(liststore) is gi.overrides.Gtk.ListStore):
            liststore.clear()   

    def on_Open1_activate(self, args=None):
        print('on_Open1_activate called -')  
        self.on_fileButton_clicked(args)  
        liststore = self.get_descendant(args,'liststore1',0,True)
        
    def on_Open1_activate_item(self, args=None):
        print('on_Open1_activate_item called')    

    def on_about1_activate(self, args=None):
        about = About1()
        
    def on_Quit1_activate(self, widget=None):
        print('on_Quit1_activate called')    
        self.on_win_destroy(widget)	

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
            """
            Show HEADER
            """
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
            Check log for errors
            """       
            check = runLogCheck(file1.fileName, self.sw_cabBonus)
            log = check.checkLog(file1.fileName, self.sw_cabBonus)
            self.log = log
            """
            Show errors
            """
            print('Header Errors: %s'%(log['HEADER']['ERRORS']))
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, '\nLOG ERRORS:\n') 
            k=1
            for errs in log["ERRORS"]:
                line = 'E%s - %s\n'%(k, errs)
                end_iter = textbuffer.get_end_iter()
                textbuffer.insert(end_iter, line) 
                k += 1
            #check.showLog(log)
        else:
            self.status1_text = None
        print('on_fileButton1_cliscked is complete.')
            
    def set_Button_label(self, button):
        if (self.status1_text != None):
            fileOnly = os.path.basename(self.status1_text)
        else:
            fileOnly = 'Select Input File (None)'
        while len(fileOnly) < 70 :
            fileOnly += ' '
        button.set_label(fileOnly)

        
    def set_status1(self, stat1):
        if (self.status1_text != None):
            fileOnly = os.path.basename(self.status1_text)
            stat1.set_text(fileOnly)
        else:
            stat1.set_text('status1')  
        
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
           
 

    def get_descendant(self, widget, child_name, level=0, doPrint=False):
      if widget is not None:
        buildableName = Gtk.Buildable.get_name(widget)
        if buildableName == None: buildableName = 'None'
        widgetName = widget.get_name()
        #print(buildableName, widgetName)
        if doPrint: print('+'*level + '>' + buildableName + ' :: ' + widgetName)
        
        #if doPrint: print("-"*level + Gtk.Buildable.get_name(widget) + " :: " + widget.get_name())
      else:
        if doPrint:  print("-"*level + "None")
        return None
      #/*** If it is what we are looking for ***/
      if(Gtk.Buildable.get_name(widget) == child_name): # not widget.get_name() !
        return widget;
      #/*** If this widget has one child only search its child ***/
      if (hasattr(widget, 'get_child') and callable(getattr(widget, 'get_child')) and child_name != ""):
        child = widget.get_child()
        if child is not None:
          return self.get_descendant(child, child_name,level+1,doPrint)
      # /*** It might have many children, so search them ***/
      elif (hasattr(widget, 'get_children') and callable(getattr(widget, 'get_children')) and child_name !=""):
        children = widget.get_children()
        # /*** For each child ***/
        found = None
        for child in children:
          if child is not None:
            found = self.get_descendant(child, child_name,level+1,doPrint) # //search the child
            if found: return found 
        
class gui_MOQPLogCheck():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/logchecker.ui")
        builder.connect_signals(Handler())
        self.appMain(builder)
   
    def appMain(self, builder):
        window = builder.get_object("win")
        MlogsumTree1 = builder.get_object("liststore1")
        MlogsumTree2 = builder.get_object("liststore2")
        MlogsumTree3 = builder.get_object("liststore3")       
        window.show_all()
        Gtk.main()    

if __name__ == '__main__':
    app = gui_MOQPLogCheck()
 

