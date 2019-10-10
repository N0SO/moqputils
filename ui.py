#!/usr/bin/python
"""
gui_csv2cab - GUI "front end" for csv2cab

csv2cab - Process a .csv file from MSExcel (or other spreadsheets)
          and make it a .CAB file by removing all commas, blank
          QSO: lines, etc. Usually used to clean a file submitted
          using AA0CL's MOQP_log.xls form.
          
          
          V0.0.1 - 2018-09-19
          First interation
          
"""
#!/usr/bin/env python
import sys
python_version = sys.version_info[0]
if (python_version == 2):
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog   import askopenfilename
    from tkFileDialog   import askdirectory
    from tkFileDialog   import asksaveasfilename
else:
    from tkinter import *
    from tkinter.messagebox import showinfo
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter.filedialog import asksaveasfilename
import os.path
from csv2cab import csv2CAB
from common import common

VERSION = '0.0.1'

class gui_csv2cab(csv2CAB):

    def __init__(self, RUN=True):
        if (RUN):
            self.appMain()
      
    def __version__(self):
        return VERSION

    def NewFile(self):
        print "New File!"

    def OpenFile(self):
        csvfilename = askopenfilename(title = "Select input log file:",
                                      filetypes=[("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(csvfilename))
        if os.path.isfile(csvfilename):
            with open(csvfilename,'r') as f:
                csvtext = f.readlines()
            self.LogText.delete(1.0, END)
            self.LogText.insert(END, ('CSV File: %s\n'%(csvfilename)))
            for line in csvtext:
                self.LogText.insert(END, line.strip()+'\n')
            cabtext = r""
            cabtext = self.processcsvData(csvtext)
            print cabtext
            if (cabtext):
                filestuff = os.path.splitext(csvfilename)
                cabfile = filestuff[0] + '.log'
                cablines = cabtext.splitlines()
                self.LogText.insert(END,
                        """
                        \n==============================
                        \nCabrillo Data:
                        \n==============================\n""")
                for line in cablines:
                    self.LogText.insert(END, line.strip()+'\n')

                filename = asksaveasfilename(initialdir = "./",
                                  title = "Save user log file...",
                                  initialfile = cabfile,
                                  filetypes = [("log files","*.csv"),
                                               ("text files","*.txt"),
                                               ("all files","*.*")])

                if (filename):
                    with open(filename,'w') as f:
                        f.write(cabtext)
                    showinfo('CAB File created and saved', 'Saved as CAB file:\n'+cabfile)

    def sum(self):
        print "Function sum() called..."

    def About(self):
        print ('About...')
        commons = common()
        pythonversion = sys.version.splitlines()
        from __init__ import VERSION
        infotext = \
        'csv2cab - Version ' + VERSION + '\n' + \
        'Utility to convert .csv logfiles to CABRILLO format.\n' \
        + commons.__get_app_version__() + '\n' \
        + 'Python ' + pythonversion[0]
        showinfo('DMRCONTACTS', infotext)


        #showinfo('GUI_CSV2CAB', 'GUI_CSV2CAB - Version ' + VERSION + '\n' + 'Utility to convert .csv logfiles to CABRILLO format.')
        
    def appMain(self):
        root = Tk()
        S = Scrollbar(root)
        self.LogText = Text(root, height=10, width=120)
        S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=S.set)

        root.title("MOQP CSV to CAB File Converter")
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.NewFile)
        filemenu.add_command(label="Open...", command=self.OpenFile)
        filemenu.add_separator()
        filemenu.add_command(label="Summary", command=self.sum)
        filemenu.add_command(label="Exit", command=root.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        mainloop()