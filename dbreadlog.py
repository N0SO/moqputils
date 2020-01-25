#!/usr/bin/env python3
import os.path
import sys
"""
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
"""
VERSION = '0.1.' 

DEVMODPATH = ['moqputils', 'cabrilloutils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
#print('Python path = %s'%(sys.path))

from moqpdbutils import *
       
if __name__ == '__main__':
    
    mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
    mydb.setCursorDict()

    qslresult = mydb.logqslCheck('N0SO')

    if (qslresult):
        qslreport = mydb.showQSLs(qslresult)
        for qreport in qslreport:
                print(qreport[0])
                print(qreport[1])
                print()
                

            
