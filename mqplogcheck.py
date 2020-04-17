#!/usr/bin/env python3
"""
mqplogcheck  - Check logs submitted for the ARRL Missouri
QSO Party and determine if the file will load correctly into
the MOQP SQL database. Look for the following:
    1. Verify the file is a CABRILLO file.
    2. Look for the following CABRILLO header tags:
        A) CALLSIGN: is populated.
        B) EMAIL: is populated.
        C) LOCATION: is populated and valid.
        D) The CATEGORY- fields have enough info
           to determine the MOQP category:
                i) - STATION:
               ii) - OPERATOR:
              iii) - POWER:
               iv) - MODE:
    3. Review QSO: lines and verify:
         A) QSO Date / time fall within contest times.
         B) FREQUENCY / BAND is in-band.
         C) MYCALL matches CALLSIGN:
         D) MYREPORT is valid
         E) MYQTH matches LOCATION:
                i) - 3 char county code for MO stations
               ii) - State, Provinance or DX for non-MO
         F) URCALL is populated.
         G) URREPORT is valid
         H) URQTH is a 3 char county code, state, prov or DX.
    4. DUPE checks.
    5. Determine contacts with BONUS stations.
    6. Summarize QSOS and compute perliminary score.
    7. Determine SHOWME and MISSOURI certificate status.

        


Update History:
* Tue Apr 14 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
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
"""moqchecklogs  - Initial Check of logfiles submitted for the 
                   ARRL Missouri QSO Party.
                
                   Based on 2020 MOQP Rules
"""

EPILOG = \
"""
Running with no parameters will launch the GUI.
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
        
class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(\
                               description = DESCRIPTION,
                                           epilog = EPILOG)
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        #parser.add_argument('-c', '--callsign', default=None,
        #    help='CALLSIGN in MOQP database to summarize. Entering allcalls = all calls in database')
        #parser.add_argument('-d', '--digital', default=None,
        #    help='Summarize digital QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in database')
        #parser.add_argument('-U', '--vhf', default=None,
        #    help='Summarize VHF QSOs only for CALLSIGN in MOQP database. Entering allcalls = all calls in database')
        #parser.add_argument('-C', '--county', default=None,
        #    help='Summarize MISSOURI COUNTIES only for CALLSIGN in MOQP database. Entering allcalls = all calls in database')
        parser.add_argument('-i', '--inputpath', default=None,
            help='Specifies the path to the folder that contains the log files to summarize.')
        return parser.parse_args()


if __name__ == '__main__':
   args = get_args()
   
   if (args.args.inputpath):
       #print(args.args.inputpath)
       from moqplogcheck import MOQPLogcheck
       app = MOQPLogcheck(args.args.inputpath)
   #elif (args.args.callsign):
   #    from moqpdbcategory import MOQPDBCategory
   #    app = MOQPDBCategory(args.args.callsign)
   #elif (args.args.digital):
   #    from moqpdbdigital import MOQPDBDigital
   #    app = MOQPDBDigital(args.args.digital)
   #elif (args.args.vhf):
   #    from moqpdbvhf import MOQPDBVhf
   #    app = MOQPDBVhf(args.args.vhf)
   #elif (args.args.county):
   #    from moqpdbcountyrpt import MOQPDBCountyRpt
   #    app = MOQPDBCountyRpt(args.args.county)
   else:
       from gui_moqpcategory import gui_MOQPChecklog
       app=gui_MOQPChecklog()

