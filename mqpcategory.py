#!/usr/bin/python
#!/usr/bin/env python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules

Update History:
* Fri May 10 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - 2019-05-10 -First interation

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
        
ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputpath", default=None,
            help="Specifies the path to the folder that contains the log files to summarize.")
        return parser.parse_args()


if __name__ == '__main__':
   args = get_args()
   
   if (args.args.inputpath):
       print(args.args.inputpath)
       from moqpcategory import MOQPCategory
       app = MOQPCategory(args.args.inputpath)
   else:
       from gui_moqpcategory import gui_MOQPCategory
       app=gui_MOQPCategory()

        