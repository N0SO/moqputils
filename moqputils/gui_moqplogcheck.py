#!/usr/bin/python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

VERSION = '0.0.1'

class Handler():
     
    def on_LogScanner_destroy(self, *args):
        #print('args type = %s\nargs Directory:\n%s'%(args, dir(args)))
        Gtk.main_quit()
        
class gui_MOQPLogCheck():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/logscanner.ui")
        builder.connect_signals(Handler())
        self.appMain(builder)
   
    def appMain(self, builder):
       window = builder.get_object("LogScanner")
       window.show_all()
       Gtk.main()    

if __name__ == '__main__':
    app = gui_MOQPLogCheck()

