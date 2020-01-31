#!/usr/bin/env python3
"""
moqpreports  - Utility to generate MOQP reports
               for eval and publishing
                
               Based on 2019 MOQP Rules

Update History:
* Thu Jan 30 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 -First interation
"""

import os.path
import sys
import argparse
VERSION = '0.0.1'
ARGS = None

DEVMODPATH = ['moqputils', 'cabrilloutils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
#print('Python path = %s'%(sys.path))
        
DESCRIPTION = \
"""moqpreports  - Generate reports for MOQP
                  from database.
                
                   Based on 2019 MOQP Rules
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
        parser.add_argument('-c', '--callsign', default='allcalls',
            help="CALLSIGN in MOQP database to summarize. "+ \
                 "Entering 'ALLCALLS' will run the report "+ \
                 "on all calls in the database.")
        args = parser.parse_args()
        #print(args)
        return args

if __name__ == '__main__':
   args = get_args()
   
   if (args.args.callsign):
       from moqpdbcatreport import MOQPDBCatReport
       app = MOQPDBCatReport(args.args.callsign)
   else:
       from gui_reports import reports_ui
       app=gui_reports()
        
