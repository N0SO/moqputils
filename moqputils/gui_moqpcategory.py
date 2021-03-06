#!/usr/bin/python
"""
gui_moqpcategory.py - GUI "front end" for moqpcategory.py

          V0.0.1 - 2019-05-10
          First interation
          
"""
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
import argparse
from moqpcategory import MOQPCategory, COLUMNHEADERS

VERSION = '0.0.3'
FILELIST = './'

class gui_MOQPCategory(MOQPCategory):

    # Define settings upon initialization. Here you can specify
    def __init__(self):
    
        self.master = Tk()
    
        self.master.geometry("400x300")
        
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        self.appMain()

    #Creation of init_window
    def client_exit(self):
        print("Exiting...")
        exit()

    def init_window(self):
        root = self.master
        root.title("MOQP Category")
        self.LogText = self.makeSumWindow(root)
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="New", command=self.NewFile)
        #filemenu.add_command(label="Convert CSV to CAB...", command=self.OpenFile)
        #filemenu.add_separator()
        filemenu.add_command(label="Categorize single log file...", command=self.SumFile)
        filemenu.add_command(label="Categorize directory of logs...", command=self.SumDir)
        #filemenu.add_separator()
        filemenu.add_command(label="Callsign from DB to Categorize...", command=self.sumCall)
        filemenu.add_command(label="Categorize all logs from DB...", command=self.sumAll)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.client_exit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

    def NewFile(self):
        print("New File!")

    def sumCall(self):
        print('Sum single callsign from MOQP database.')

    def sumAll(self):
        print('Sum all callsigns from MOQP database.')

    def About(self):
        showinfo('GUI_MOQPCATEGORY', 'GUI_MOQPCATEGORY - Version ' + VERSION + '\n' + \
              'Utility to help categorize Missouri QSO Party logfiles in CABRILLO format.')

    def _sumfile(self, logfileName):
        print('File name selected: %s'%(logfileName))
        
        self.fillLogTextfromFile(logfileName, self.LogText, clearWin=True)
        
        logsum = self.parseLog(logfileName)
        
        #print(logsum['ERRORS'])

        win = Toplevel()
        win.title(os.path.basename(logfileName))
        logtext = self.makeSumWindow(win)
        logtext.delete(1.0, END)
        logtext.insert(END, ('Log Summary for Station %s\n'%(logsum['HEADER']['CALLSIGN'])))
        self.showsummary(logtext, logsum, colheader=True)


    def SumFile(self):
        logfileName = askopenfilename(title = "Select input log file:",
                                      filetypes=[ \
                                                 ("LOG files","*.log"),
                                                 ("LOG files","*.LOG"),
                                                 ("CSV files","*.csv"),
                                                 ("CSV files","*.CSV"),
                                                 ("Text files","*.txt"),
                                                 ("Text files","*.TXT"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(logfileName))
        
        if(logfileName):
            self._sumfile(logfileName)
        
    def SumDir(self):
        logpathName = askdirectory()
        print('Directory name selected: %s'%logpathName)
        for (dirName, subdirList, fileList) in os.walk(logpathName, topdown=True):
           if (fileList != ''):
              for logfileName in fileList: 
                  if ( (not logfileName.startswith('.')) and \
                                 (logfileName.endswith('.LOG')) ):
                      self._sumfile(dirName+'/'+logfileName)

    def makeSumWindow(self, win):
        S = Scrollbar(win)
        Logwin = Text(win, height=10, width=220)
        S.pack(side=RIGHT, fill=Y)
        Logwin.pack(side=LEFT, fill=Y)
        S.config(command=Logwin.yview)
        Logwin.config(yscrollcommand=S.set)
        return Logwin
        
    def showsummary(self, window, log, colheader=False):
        if (colheader):
            window.insert(END, COLUMNHEADERS)
        window.insert(END, ('%s\t'%(log['HEADER']['CALLSIGN'])))
        window.insert(END, ('%s\t'%(log['HEADER']['OPERATORS'])))
        window.insert(END, ('%s\t'%(log['HEADER']['CATEGORY-STATION'])))
        window.insert(END, ('%s\t'%(log['HEADER']['CATEGORY-OPERATOR'])))
        window.insert(END, ('%s\t'%(log['HEADER']['CATEGORY-POWER'])))
        window.insert(END, ('%s\t'%(log['HEADER']['CATEGORY-MODE'])))
        window.insert(END, ('%s\t'%(log['HEADER']['LOCATION'])))
        window.insert(END, ('%s\t'%(log['HEADER']['CATEGORY-OVERLAY'])))
        window.insert(END, ('%s\t'%(log['QSOSUM']['CW'])))
        window.insert(END, ('%s\t'%(log['QSOSUM']['PH'])))
        window.insert(END, ('%s\t'%(log['QSOSUM']['DG'])))
        window.insert(END, ('%s\t'%(log['QSOSUM']['QSOS'])))
        window.insert(END, ('%s\t'%(log['QSOSUM']['VHF'])))
        window.insert(END, ('%s\t'%(log['MULTS'])))         
        window.insert(END, ('%s\t'%(log['SCORE'])))        
        window.insert(END, ('%s\t'%(log['MOQPCAT']['MOQPCAT'])))
        window.insert(END, ('%s\t'%(log['MOQPCAT']['DIGITAL'])))
        window.insert(END, ('%s\t'%(log['MOQPCAT']['VHF'])))
        window.insert(END, ('%s\n'%(log['MOQPCAT']['ROOKIE'])))
        
        for r in log['ERRORS']:
            if ( r != [] ):
                print (r)
                window.insert(END, r)
        
        """
        qsoErrors = self.qsolist_valid(log['QSOLIST'])
        for r in qsoErrors:
            window.insert(END, ('Error in QSO %d:\n'%(r[0])) )
            for e in r[1]:
                window.insert(END, ('\t%s\n'%(e)) )
        """

    def OpenFile(self):
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
            print(csvtext)
            cabfile = csvfilename + ".log"
            with open(cabfile,'w') as f:
                f.write(cabtext)
            showinfo('CAB File created and saved', 'Saved as CAB file:\n'+cabfile)

    def fillLogTextfromData(self, Data, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        for line in Data:
            textWindow.insert(END, line.strip()+'\n')

    def fillLogTextfromFile(self, filename, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           self.fillLogTextfromData(retText, textWindow, clearWin)
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText
        
    def appMain(self):
        #mainloop 
        self.master.mainloop()     
        
if __name__ == '__main__':
   ARGS = get_args()
   if ARGS.args.inputpath == None:
      """
      root = Tk()

      root.geometry("400x300")
      """
      #creation of an instance
      app = guiMOQPCategory()

      #mainloop 
      #root.mainloop()     
   
   else:
      app = guiMOQPCategory(ARGS.args.inputpath)

        
