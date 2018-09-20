from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
import os.path
import countyqsos

VERSION = '0.0.3'


def NewFile():
    print "New File!"
    
def OpenFile():
    name = askopenfilename(title = "Select input log file:",
                           filetypes=[("log Files","*.log"),
                                      ("LOG Files","*.LOG"),
                                      ("CSV files","*.csv"),
                                      ("Text files","*.txt"),
                                      ("All Files","*.*")])
    print('File name selected: %s'%(name))
    if os.path.isfile(name):
        with open(name,'r') as f:
            logtext = f.readlines()
        for line in logtext:
            LogText.insert(END, line)
        app = countyqsos.theApp(logtext)
        ShowSum(app)

def ShowSum(app):
    LogText.insert(END,'==== Summary ====\n')
    LogText.insert(END,('QSO Summary:\n%d CW QSOs + %d PHONE QSOs + %d DIGITAL QSOs = %d Total QSOS\n'%(app.cw,
                                                                                                        app.ph,                                                                                                             
                                                                                                        app.dg,
                                                                                                        app.cw+app.ph+app.dg
                                                                                                        )))
    LogText.insert(END,('MULT Summary:\nCounties worked:%d\nUS States worked:%d\nCanada worked:%d\nDX worked:%d\n'%(app.counties, 
                                                                                                                    app.states, 
                                                                                                                    app.provs, 
                                                                                                                    app.dx
                                                                                                                    )))
    LogText.insert(END,('\nTotal Score: %d\n'%(app.totalscore(app.counties, app.states, app.provs, app.dx, app.cw, app.ph, app.dg))))
    LogText.insert(END,('List of MULTS:\n %s\n'%(app.summary)))

      
    
def About():
    showinfo('GUI_COUNTYQSOS', 'GUI_COUNTYQSOS - Version ' + VERSION + '\n' + 'Display summary of Missouri QSO Party log file.')

root = Tk()
S = Scrollbar(root)
LogText = Text(root, height=10, width=120)
S.pack(side=RIGHT, fill=Y)
LogText.pack(side=LEFT, fill=Y)
S.config(command=LogText.yview)
LogText.config(yscrollcommand=S.set)

root.title("MOQP County QSO Summary")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

mainloop()