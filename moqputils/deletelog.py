#!/usr/bin/env python3
"""
deleLog - 

Update History:
* Thu May 07 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start tracking revs.
"""

VERSION = '0.0.1' 

from moqpdbutils import *
#from CabrilloUtils import CabrilloUtils
from moqpdbconfig import *

class deleteLog():

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def appMain(self, callsign):
       print('Delete log for %s from MOQP database %s:'%(callsign, DBNAME))
       if (callsign):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           #log = mydb.get_log_parts(callsign)
           #print(log)
           mydb.delete_log(callsign)

