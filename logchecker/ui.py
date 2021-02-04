#!/usr/bin/python
import gi, os, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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

class my_file_open(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Select MOQP Log File to Check")
        self.fileName=None
        
    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.fileName = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("CAB files")
        filter_text.add_pattern("*.LOG")
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("CSV files")
        filter_text.add_pattern("*.CSV")
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

class runLogCheck():

    def __init__(self, filename = None, 
                       acceptedpath = None,
                       cabbonus = None,
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
                
            check = runLogCheck(file1.fileName)
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

