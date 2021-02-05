#!/usr/bin/python
import gi, os, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from logchecker.treesample import TreeViewFilterWindow
from logchecker.filedialogs import my_file_open

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

class runLogCheck():

    def __init__(self, filename = None, 
                       cabbonus = None,
                       acceptedpath = None,
                       loadlog = False):
        self.logName = filename
        self.acceptedPath = acceptedpath
        self.cabBonus = cabbonus  
        self.loadLog = loadlog
        if (self.loadLog):
            from moqputils.moqploadlogs import MOQPLoadLogs
            self.App = MOQPLoadLogs()
        else:
            from moqputils.moqplogcheck import MOQPLogcheck
            self.App = MOQPLogcheck()
            
    def processData(self, logName=None):
        csvData = self.App.processOneFile(self.logName,
                                          True,
                                          self.acceptedPath,
                                          self.cabBonus)
        return csvData
         
    def showData(self, Data_to_Show):
        print(Data_to_Show)
        lines = Data_to_Show.splitlines()
        llines = lines[1].split('\t')
        show = TreeViewFilterWindow([llines])

class Handler():

    def __init__(self):
        self.fileButton_text = None
        self.status1_text = None
        self.status2_text = None
        self.sw_cabBonus = False
        self.sw_loadLogs = False
        self.sw_acceptErrors = False
        self.sw_replaceExisting = False
     
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
	
    def on_AboutMenuItem_activate(self, args=None):
        about = About1()
	
    def on_fileButton_clicked(self, widget):
        #print('File Button Clicked!')  
        file1=my_file_open()
        file1.on_file_clicked(widget)

        print('My File selected: %s'%(file1.fileName))
        if file1.fileName != None:
            self.status1_text = file1.fileName
            data = None
            try:
                with open(file1.fileName, 'r') as thisfile:
                    data = thisfile.readlines()
            except:
                data = 'Error reading file %s'%(file1.fileName)
            #self.set_label(file1.fileName)
            textbuffer=widget.get_buffer()
            for line in data:
                end_iter = textbuffer.get_end_iter()
                textbuffer.insert(end_iter, line)
                
            check = runLogCheck(file1.fileName, self.sw_cabBonus)
            check_result = check.processData(file1.fileName)
            check.showData(check_result)
            
    def set_Button_label(self, button):
        fileOnly = os.path.basename(self.status1_text)
        while len(fileOnly) < 70 :
            fileOnly += ' '
        button.set_label(fileOnly)     
        
    def set_status1(self, status1):
        fileOnly = os.path.basename(self.status1_text)
        status1.set_text(fileOnly)     
        
class gui_MOQPLogCheck():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/logchecker.ui")
        builder.connect_signals(Handler())
        self.appMain(builder)
   
    def appMain(self, builder):
       window = builder.get_object("win")
       window.show_all()
       Gtk.main()    

if __name__ == '__main__':
    app = gui_MOQPLogCheck()

