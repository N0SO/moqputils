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
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
import os.path
import csv2cab

VERSION = '0.0.1'


def NewFile():
    print "New File!"
    
def OpenFile():
    csvfilename = askopenfilename(title = "Select input log file:",
                                  filetypes=[("CSV files","*.csv"),
                                             ("Text files","*.txt"),
                                             ("All Files","*.*")])
    print('File name selected: %s'%(csvfilename))
    if os.path.isfile(csvfilename):
        with open(csvfilename,'r') as f:
            csvtext = f.readlines()
        for line in csvtext:
            LogText.insert(END, line.strip()+'\n')
        app = csv2cab.csv2CAB()
        cabtext = r""
        cabtext = app.processcsvData(csvtext)
        print csvtext
        cabfile = csvfilename + ".log"
        with open(cabfile,'w') as f:
            f.write(cabtext)
        showinfo('CAB File created and saved', 'Saved as CAB file:\n'+cabfile)
       
def sum():
    print "Function sum() called..."
       
    
def About():
    showinfo('GUI_CSV2CAB', 'GUI_CSV2CAB - Version ' + VERSION + '\n' + 'Utility to convert .csv logfiles to CABRILLO format.')

root = Tk()
S = Scrollbar(root)
LogText = Text(root, height=10, width=120)
S.pack(side=RIGHT, fill=Y)
LogText.pack(side=LEFT, fill=Y)
S.config(command=LogText.yview)
LogText.config(yscrollcommand=S.set)

root.title("MOQP CSV to CAB File Converter")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Summary", command=sum)
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

mainloop()