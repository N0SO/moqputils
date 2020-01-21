#!/usr/bin/env python3
import os.path
import sys

DEVMODPATH = ['moqputils', 'cabrilloutils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
print('Python path = %s'%(sys.path))

#import mysql.connector
import MySQLdb

from moqpdbconfig import *

mydb = MySQLdb.connect (
  host=HOSTNAME,
  user=USER,
  passwd=PW,
  database=DBNAME
)

#mycursor = mydb.cursor()
mycursor = mydb.cursor(MySQLdb.cursors.DictCursor)

mycursor.execute("SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1")

all_logs = mycursor.fetchall()

for thislog in all_logs:
  print('thislog = %s'%(thislog))
  query= ("SELECT * FROM `QSOS` WHERE `LOGID` = %d"%(thislog['ID']) )
  print(query)
  mycursor.execute(query)
  thislogqsos = mycursor.fetchall()
  nextID = None
  for qso in thislogqsos:
    for nextlog in all_logs:
        if (nextlog['CALLSIGN'] == qso['URCALL']):
            nextID = nextlog['ID']
            query= ("SELECT * FROM `QSOS` WHERE `LOGID` = %d"%(nextID) )
            mycursor.execute(query)
            qslqsos = mycursor.fetchall()
            for qsl in qslqsos:
                if qsl['URCALL'] == thislog['CALLSIGN']:
                    print('%s\n%s'%(qsl, qso))
    if (nextID):
        print('Fetching QSOs for %s, LOGID %d'%(qso['URCALL'], nextID))
        break
    else:
        print('%s not in database.'%(qso['URCALL']))
    #query = ("SELECT * FROM `QSOS` WHERE `URCALL` IN (`%s`)"%(thislog['CALLSIGN']) )
    query = ("SELECT * FROM `QSOS` WHERE `LOGID` = %d"%(thislog['ID']) )
  break 
   

