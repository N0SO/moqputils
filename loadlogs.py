#!/usr/bin/python
"""
loadlogs - Load cabrillo log files into SQL database.
                
Update History:
* Wed Nov 05 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1
- Inital file creation.
"""
import sys
import os.path
import argparse
#import subprocess

VERSION = '0.0.1'

DEVMODPATH = ['cabrilloutils', 'moqputils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
#print('Python path = %s'%(sys.path))

DESCRIPTION = \
"""loadlogs  - Load cabrillo format MOQP log files into 
               SQL database
"""

EPILOG = \
"""
Running with no parameters will launch the GUI.
"""

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(\
                               description = DESCRIPTION,
                                           epilog = EPILOG)
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputpath", default=None,
            help="Specifies the path to the folder that contains the log files to summarize.")
        return parser.parse_args()

if __name__ == '__main__':
   args = get_args()
   
   if (args.args.inputpath):
       from moqploadlogs import MOQPLoadLogs
       app = MOQPLoadLogs(args.args.inputpath)
   else:
       from moqploadlogs_ui import UI
       app=UI()
