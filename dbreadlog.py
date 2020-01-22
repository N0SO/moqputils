#!/usr/bin/env python3
import MySQLdb
import os.path
import sys
from datetime import datetime

VERSION = '0.0.2' 

DEVMODPATH = ['moqputils', 'cabrilloutils']
# If the development module source paths exist, 
# add them to the python path
for mypath in DEVMODPATH:
    if ( os.path.exists(mypath) and \
                       (os.path.isfile(mypath) == False) ):
        sys.path.insert(0,mypath)
#print('Python path = %s'%(sys.path))

from moqpdbconfig import *

class MOQPDBUtils():

    def __init__(self, host = None, 
                       user = None, 
                       passwd = None, 
                       database = None):
       if (host):
           self.mydb = self.connectDB(host, 
                                      user, 
                                      passwd, 
                                      database)
           self.setCursor()
       self.cursor = None
          
    def connectDB(self, host, 
                        user, 
                        passwd, 
                        database):
        try:                 
            mydb = MySQLdb.connect(
              host=HOSTNAME,
              user=USER,
              passwd=PW,
              database=DBNAME
            )
        except Exception as e:
            print ("Error connecting to database %s: %s"%\
                                           (database,e.args))    
                       
        return mydb

    def setCursor(self):
        self.cursor = self.mydb.cursor()

    def setCursorDict(self):
        self.cursor = self.mydb.cursor(MySQLdb.cursors.DictCursor)
        
    def write_query(self, query):
        qstat = None
        #if (db == None): db = self.mydb
        try:
            self.cursor.execute(query)
            self.mydb.commit()
            qstat = self.cursor.lastrowid
            #qresult = self.cursor.fetchall()
            #print(qresult)
        except Exception as e:
            print ("write_query Error %s executing query: %sn"%\
                                           (e.args,query))  
        return qstat
        
    def read_query(self, query):
        qresult = None
        qstat = self.write_query(query)
        try:
            qresult = self.cursor.fetchall()
        except Exception as e:
            print( \
            "read_query Error %s reading results from query:\n %s"%\
                                              (e.args,query))
        return qresult

    def fetchlogQSOS(self, callID):
        thislogqsos = None        
        query= ("SELECT * FROM `QSOS` WHERE `LOGID` = %d"%(callID) )
        thislogqsos = self.read_query(query)

        return thislogqsos

    def logtimes(self, logdate, logtime):
       datefmts = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']
       timefmts = ['%H%M', '%H:%M', '%H %M']
       logtimeobj = None

       #Date
       d=0
       while (d<2):
           try:
               datefstg = datefmts[d]
               dateobj=datetime.strptime(logdate, datefstg)
               #print(dateobj)
               d=3
           except:
               print('Format %s did not work for date %s.'%(datefstg, logdate))
               d += 1

       #time
       t=0
       while (t<2):
           try:
               timefstg = timefmts[t]
               timeobj=datetime.strptime(logtime, timefstg)
               #print(timeobj)
               t=3
           except:
              print('Format %s did not work for time %s.'%(timefstg, logtime))
              t += 1

       logtimeobj = datetime.strptime(logdate+' '+logtime, datefstg+' '+timefstg)
       return logtimeobj

if __name__ == '__main__':
    """
    mydb = MOQPDBUtils()
    testobj = mydb.logtimes('2019-04-06', '14:00')
    
    print(testobj)
    exit()
    """
    """
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
    !!!PUT TRIPLETICKS HERE!!!
    """
    
    mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
    mydb.setCursorDict()
    
    query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
    all_logs = mydb.read_query(query)
    #print(all_logs)

    for thislog in all_logs:
        #print('thislog = %s'%(thislog))
        thislogqsos = mydb.fetchlogQSOS(thislog['ID'])
        #print(thislogqsos)
        #exit()
        nextID = None
        for qso in thislogqsos:
            for nextlog in all_logs:
              if (nextlog['CALLSIGN'] == qso['URCALL']):
                nextID = nextlog['ID']
                query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(nextID, thislog['CALLSIGN']) )
                print(query)
                qslqsos = mydb.read_query(query)
                print(qso)
                print(qslqsos)
                exit()

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

