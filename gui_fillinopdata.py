#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gui_fillinopdata.py - Read the awards.csv file and fill in
the missing name, address, e-mail address from the
cabrillo log files.
"""
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename, askdirectory
import os.path
import fillinopdata

VERSION = '0.0.2'
FIELDS = 'CSV list file', 'Logfile Directory'

class MyAPP():
    def __init__(self):
        root = Tk()
        root.geometry('440x290')
        self.inpFile, self.logDir, self.LogText = self. makeForm(root)
        self.root = root
        self.main()
        
    def NewFile(self):
        print "New File!"

    def OpenFile(self):
        csvfilename = askopenfilename(title = "Select input log file:",
                      filetypes=[("Text files","*.txt"),
                             ("CSV files","*.csv"),
                             ("All Files","*.*")])
        print('File name selected: %s'%(csvfilename))

        self.inpFile.delete(0, END)
        self.inpFile.insert(len(csvfilename), csvfilename)

    def FillIn(self):
        csvfilename = self.inpFile.get().strip()
        dirPath = self.logDir.get().strip()
        print('FillIn:\n%s\n%s'%(csvfilename, dirPath))
        if os.path.isfile(csvfilename):
            with open(csvfilename,'r') as f:
                csvtext = f.readlines()
            for line in csvtext:
                self.LogText.insert(END, line.strip()+'\n')
            app = fillinopdata.FillInOpData(csvtext, dirPath)
            optext = r""
            optext = app.return_data
            #print csvtext
            OpData=Text(self.root, height=10, width = 50)
            OpData.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            S = Scrollbar(self.root)
            S.config(command=OpData.yview)
            OpData.config(yscrollcommand=S.set)
            S.grid(row=4, column=3, sticky='NS')
            filledinFile = csvfilename + "-filled.txt"
            f = open(filledinFile,'w')
            for line in optext:
                OpData.insert(END, line.strip()+'\n')
                f.writelines(line.strip())
            f.close()

            #with open(filledinFile,'w') as f:
            #    f.writelines(optext)
            showinfo('File with Op Datat from logs created and saved', 'Saved:\n'+filledinFile)
    
    def OpenDir(self):
        csvlogdirname = askdirectory(title = "Select input log file:")
        print('Log File directory selected: %s'%(csvlogdirname))
        self.logDir.delete(0, END)
        self.logDir.insert(len(csvlogdirname), csvlogdirname)

    def About(self):
        showinfo('GUI_CSV2CAB', 'GUI_CSV2CAB - Version ' + VERSION + '\n' + 'Utility to convert .csv logfiles to CABRILLO format.')

    def winSize(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print ('Width = %d\nHeight = %s\n'%(screen_width, screen_height))
        print self.root.geometry()

    def makeForm(self, root):
        root.title("MOQP Fill In Operator Data")

        Button(root, width=15, text='Select Input File ', command=self.OpenFile).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        e1 = Entry(root, width=40)
        e1.grid(row=0, column = 1, sticky='E')

        Button(root, width=15, text='Select Log Directory', command=self.OpenDir).grid(row=1, column=0, sticky=W, padx=5, pady=5)
        e2 = Entry(root, width=40)
        e2.grid(row=1, column = 1, sticky='E')

        Button(root, width=15, text='Fill', command=self.FillIn).grid(row=2, column=0, sticky=W, padx=5, pady=5)

        LogText = Text(root, height=10, width = 50)
        LogText.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        S = Scrollbar(root)
        S.config(command=LogText.yview)
        LogText.config(yscrollcommand=S.set)
        S.grid(row=3, column=3, sticky='NS')

        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.NewFile)
        filemenu.add_command(label="Open Input File...", command=self.OpenFile)
        filemenu.add_command(label="Select Log File Directory...", command=self.OpenDir)
        filemenu.add_separator()
        filemenu.add_command(label="Window Size", command=self.winSize)
        filemenu.add_command(label="Exit", command=self.winSize)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        return e1, e2, LogText
        
    def main(self):
        mainloop()
 

myapp = MyAPP()
