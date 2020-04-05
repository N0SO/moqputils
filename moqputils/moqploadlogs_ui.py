#!/usr/bin/python
"""
moqploadlogs_ui - GUI front end for moqploadloags.
                
Update History:
* Wed Nov 05 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1
- Inital file creation.
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
import subprocess
import argparse

VERSION = '0.0.1'

DEVMODPATH = ['cabrilloutils', 'moqputils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
#print('Python path = %s'%(sys.path))
