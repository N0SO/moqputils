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
from moqpcategory import MOQPCategory

VERSION = '0.0.1'
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
        S = Scrollbar(root)
        self.LogText = Text(root, height=10, width=120)
        S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=S.set)

        root.title("MOQP Category")
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="New", command=self.NewFile)
        #filemenu.add_command(label="Convert CSV to CAB...", command=self.OpenFile)
        #filemenu.add_separator()
        filemenu.add_command(label="Log File to Categorize...", command=self.SumFile)
        #filemenu.add_command(label="Sum directory of logs...", command=self.SumDir)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.client_exit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

    def NewFile(self):
        print("New File!")


    def About(self):
        showinfo('GUI_MOQPCATEGORY', 'GUI_MOQPCATEGORY - Version ' + VERSION + '\n' + \
              'Utility to help categorize Missouri QSO Party logfiles in CABRILLO format.')

    def SumDir(self):
        logpathName = filedialog.askdirectory()
        print('Directory name selected: %s'%logpaathName)

    def SumFile(self):
        logfileName = askopenfilename(title = "Select input log file:",
                                      filetypes=[("LOG files","*.LOG"),
                                                 ("log files","*.log"),
                                                 ("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(logfileName))
        
        self.fillLogTextfromFile(logfileName, self.LogText, clearWin=True)
        
        logsum = self.exportcsvfiledict(logfileName)
        print(logsum.viewkeys())
        print('MOQP Summary:\n%s\nQSO Summary:\n%s'% \
                    (logsum['MOQPCAT'],
                     logsum['QSOSUM']))
        """                     
        print('MOQP Category:\n%s %s %s %s %s %s'% (\
                      logsum['MOQPSUM']['LOCATION'],
                      logsum['MOQPSUM']['CATEGORY-STATION'],
                      logsum['MOQPSUM']['CATEGORY-OPERATOR'],
                      logsum['MOQPSUM']['CATEGORY-POWER'],
                      logsum['MOQPSUM']['CATEGORY-MODE'],
                      logsum['MOQPSUM']['CATEGORY-OVERLAY']))
        loglines = logsum.splitlines()
        #self.fillLogTextfromData(loglines, self.LogText, clearWin=True)
        
        #print(loglines)
        win = Toplevel()
        win.title('MOQP Category of logfile: '+logfileName)
        r=0
        for line in loglines:
            print(line)
            lineparts = line.split(',')
            c=0
            for cell in lineparts:
               if (cell.strip() == ''):
                   reltext = 'flat'
               else:
                   reltext = 'solid'
               Label(win, text=cell,
                     borderwidth=3,
                     relief=reltext).grid(row=r,column=c)
               c+=1
            r+=1
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
      root = Tk()

      root.geometry("400x300")

      #creation of an instance
      app = guiMOQPCategory(root)

      #mainloop 
      root.mainloop()     
   
   else:
      app = guiMOQPCategory(ARGS.args.inputpath)

        
