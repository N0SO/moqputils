import gi, sys
from moqputils.moqpcategory import MOQPCategory

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

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
            #print("File selected: " + dialog.get_filename())
            self.fileName = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

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
        
class my_file_save(Gtk.Window):
    def __init__(self, log=None, logfile=None):
        self.log=log
        self.logfile = logfile
        if (log):
            self.callsign = log['HEADER']['CALLSIGN']
            self.fileName=self.callsign + '.txt'
        else:        
            self.callsign = None
            self.fileName=None

        title = "Save MOQP Log Summary to File "
        if (self.callsign): title += self.callsign
        Gtk.Window.__init__(self, title=title)
        #print(self.log.keys())
        #print(self.log['RAWTEXT'])
        #print(self.log['ERRORS'])
        
    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose or enter a file name:", 
            parent=self, action=Gtk.FileChooserAction.SAVE          
        )

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        
        textbuffer=widget.get_buffer()
        end_iter = textbuffer.get_end_iter()
        start_iter = textbuffer.get_start_iter()
        contents = textbuffer.get_text(start_iter, end_iter, True)
        
        contents += '\nLOG SUMMARY:'
        contents += 'CONTEST: %s\n'%(self.log['HEADER']['CONTEST'])
        contents += 'CALLSIGN USED: %s\n'%(self.log['HEADER']['CALLSIGN'])
        contents += 'OPERATORS: %s\n'%(self.log['HEADER']['OPERATORS'])
        contents += 'CATEGORY (from log header): %s\n'%(self.log['HEADER']['CATEGORY-STATION'])
        contents += 'STATION  (from log header): %s\n'%(self.log['HEADER']['CATEGORY-OPERATOR'])
        contents += 'POWER (from log header): %s\n'%(self.log['HEADER']['CATEGORY-POWER'])
        contents += 'MODE (from log header): %s\n'%(self.log['HEADER']['CATEGORY-MODE'])
        contents += 'LOCATION (from log header): %s\n'%(self.log['MOQPCAT']['LOCATION'])

        contents += 'TOTAL QSOS: %s\n'%(self.log['QSOSUM']['QSOS'])
        contents += '    CW: %s\n'%(self.log['QSOSUM']['CW'])
        contents += ' PHONE: %s\n'%(self.log['QSOSUM']['PH'])
        contents += '    RY: %s\n'%(self.log['QSOSUM']['DG'])
        contents += '   VHF: %s\n'%(self.log['QSOSUM']['VHF'])
        contents += ' MULTS: %s\n'%(self.log['MULTS'])
        contents += 'CABRILLO BONUS: %s\n'%(self.log['BONUS']['CABRILLO'])
        contents += '    W0MA BONUS: %s\n'%(self.log['BONUS']['W0MA'])
        contents += '    K0GQ BONUS: %s\n'%(self.log['BONUS']['K0GQ'])
        contents += 'SCORE: %s\n'%(self.log['SCORE'])
        contents += 'DUPES: %s\n'%(self.log['QSOSUM']['DUPES'])
        contents += 'TOTAL LOG ERROR COUNT: %s\n'%(len(self.log['ERRORS']))

        contents += 'CONTEST CATEGORY: %s\n'%(self.log['MOQPCAT']['MOQPCAT'])
        contents += 'VHF ENTRY: %s\n'%(self.log['MOQPCAT']['VHF'])
        contents += 'DIGITAL ENTRY: %s\n'%(self.log['MOQPCAT']['DIGITAL'])
        contents += 'ROOKIE ENTRY: %s\n'%(self.log['MOQPCAT']['ROOKIE'])
        contents += 'SHOWME CERTIFICATE: %s\n'%(self.log['BONUS']['SHOWME'])
        contents += 'MISSOURI CERTIFICATE: %s\n'%(self.log['BONUS']['MISSOURI'])

        if self.callsign is not None:
            print('setting file name to %s'%(self.fileName))
            dialog.set_current_name(self.fileName)
        print('callsign = %s'%(self.callsign))
        print('file name after default set = %s'%(dialog.get_filename()))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Save clicked")
            file_path = dialog.get_filename()

            print("File selected: " + file_path)
            self.fileName = file_path
            try:
                with open(file_path, "w") as f:
                    f.write(contents)           
            except:
                print('Error %s writing report for %s to %s.'%(sys.exc_info(),
                                                               self.callsign, file_path))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):

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

