#!/usr/bin/python
"""
gui_moqputils.py - GUI "front end" for moqp utilities

          V0.0.1 - 2019-05-10
          First interation
          
          V0.0.2 - 2019-05-10
          Renamed to guiMOQPUtils since it now has options
          for several other MOQP utilities.
          
          
          
"""
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory

import os.path
import argparse
from csv2cab import csv2CAB
from moqpcategory import MOQPCategory
#from onexonesummary import 

VERSION = '0.0.3'
FILELIST = './'

class guiMOQPUtils(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def client_exit(self):
        print "Exiting..."
        exit()

    def init_window(self):
        root = self.master
        S = Scrollbar(root)
        self.LogText = Text(root, height=10, width=120)
        S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=S.set)

        root.title("MOQP Utilities")
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.NewFile)
        filemenu.add_command(label="Convert CSV to CAB...", command=self.OpenFile)
        filemenu.add_separator()
        filemenu.add_command(label="Log File summary...", command=self.SumFile)
        filemenu.add_command(label="Sum directory of logs...", command=self.SumDir)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.client_exit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        #mainloop()

    def NewFile(self):
        print "New File!"


    def About(self):
        showinfo('GUI_MOQPCATEGORY', 'GUI_MOQPCATEGORY - Version ' + VERSION + '\n' + \
              'Utility to help categorize Missouri QSO Party logfiles in CABRILLO format.')

    def SumOneXOnes(self):
        logpathName = askdirectory()
        print('Directory name selected: %s'%logpathName)
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvflist(logpathName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logpathName + "logsummaryreport.txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)

    def SumDir(self):
        logpathName = askdirectory()
        print('Directory name selected: %s'%logpathName)
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvflist(logpathName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logpathName + "logsummaryreport.txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)
        
        
        

    def SumFile(self):
        logfileName = askopenfilename(title = "Select input log file:",
                                      filetypes=[("LOG files","*.log"),
                                                 ("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(logfileName))
        
        logdata = self.fillLogTextfromFile(logfileName, self.LogText)
        
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvfile(logfileName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logfileName + ".txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)
        
        
        
    def fillLogTextfromFile(self, filename, textWindow):
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           for line in retText:
              textWindow.insert(END, line.strip()+'\n')
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText

    def OpenFile(self):
        csvfilename = askopenfilename(title = "Select input log file:",
                                      filetypes=[("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(csvfilename))
        if os.path.isfile(csvfilename):
            csvtext = self.fillLogTextfromFile(csvfilename, self.LogText)
            app = csv2CAB()
            cabtext = r""
            cabtext = app.processcsvData(csvtext)
            #print csvtext
            for line in cabtext:
               self.LogText.insert(END, line.strip()+'\n')
            cabfile = csvfilename + ".log"
            with open(cabfile,'w') as f:
                f.write(cabtext)
            showinfo('CAB File created and saved', 'Saved as CAB file:\n'+cabfile)
        
    def appMain(self, pathname):
       #import moqpcategory
       mqpcat = MOQPCategory()
       
       if (os.path.isfile(pathname)):
          mqpcat.exportcsvfile(pathname.strip())
       else:
          mqpcat.exportcsvflist(pathname.strip())
        
if __name__ == '__main__':
      root = Tk()

      root.geometry("900x300")

      #creation of an instance
      app = guiMOQPUtils(root)

      #mainloop 
      root.mainloop()     
   
        
:
