#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gui_fillinopdata.py - Read the awards.csv file and fill in
the missing name, address, e-mail address from the
cabrillo log files.
"""
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
import os.path
import csv2cab

VERSION = '0.0.1'
FIELDS = 'CSV list file', 'Logfile Directory'


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

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries


root = Tk()
ents = makeform(root, FIELDS)
root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
S = Scrollbar(root)
LogText = Text(root, height=10, width=120)
S.pack(side=RIGHT, fill=Y)
LogText.pack(side=LEFT, fill=Y)
S.config(command=LogText.yview)
LogText.config(yscrollcommand=S.set)

root.title("MOQP Fill In Operator Data")
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