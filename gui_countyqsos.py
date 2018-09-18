from Tkinter import *
import countyqsos
from tkFileDialog   import askopenfilename
import os.path


def NewFile():
    print "New File!"
    
def OpenFile():
    name = askopenfilename(title = "Select input log file:",
                           filetypes=[("LOG Files","*.log"),
                                      ("CSV files","*.csv"),
                                      ("Text files","*.txt"),
                                      ("All Files","*.*")])
    print('File name selected: %s'%(name))
    if os.path.isfile(name):
        with open(name,'r') as f:
            logtext = f.read()
        LogText.insert(END, logtext)
       
    
def About():
    print "This is a simple example of a menu"
    print logtext
    
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