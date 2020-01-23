#!/usr/bin/env python3
import MySQLdb
import os.path
import sys
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

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
from generalaward import GenAward

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

    def padtime(self, timestg):
        count = len(timestg)
        if (count < 4):
            pads = 4 - count
            padtime =''
            for i in range(pads):
                padtime += '0'
            padtime += timestg
        elif (count > 4):
            padtime = timestg[:3]
        else:
            padtime = timestg
        return padtime

        
    def qsoqslCheck(self, myqso, urqso):
        qslstat = None
        gutil = GenAward()
        """
        TBD - compare date/time, BAND, MODE, REPORT, QTH
        """

        count = len(myqso['TIME'])
        if (count != 4):
            newtime = self.padtime(myqso['TIME'])
            print('Time string wrong length - changing %s to %s...'%(myqso['TIME'], newtime))
            myqso['TIME'] = newtime
            
        count = len(urqso['TIME'])
        if (count != 4):
            newtime = self.padtime(urqso['TIME'])
            print('Time string wrong length - changing %s to %s...'%(urqso['TIME'], newtime))
            urqso['TIME'] = newtime
            
        myqtime = self.logtimes(myqso['DATE'], myqso['TIME'])
        urqtime = self.logtimes(urqso['DATE'], urqso['TIME'])
        myqband = gutil.getBand(myqso['FREQ'])
        urqband = gutil.getBand(urqso['FREQ'])
        
        if (myqtime > urqtime):
            timediff = myqtime - urqtime
        else:
            timediff = urqtime - myqtime
        
        print(timediff)
        print(timedelta(minutes=45))
        
        if ( (timediff < timedelta(minutes=30) ) and \
             (myqband == urqband) and \
             (myqso['MODE'] == urqso['MODE']) and \
             (myqso['URCALL'] == urqso['MYCALL']) and \
             (myqso['URQTH'] == urqso['MYQTH']) and \
             (myqso['URREPORT'] != '') ):
            qslstat = True
        
        return qslstat
        
    def logqslCheck(self, call, loglist = None):
        statList = None

        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
            all_logs = self.read_query(query)
        
        callID = self.CallinLogs(call, all_logs)
        
        if (callID):
            myqsos = self.fetchlogQSOS(callID)
            if (myqsos):
                statList = []
                for qso in myqsos:
                    qsostat = dict()
                    nextCall = qso['URCALL']
                    nextID = self.CallinLogs(nextCall, all_logs)
                    if (nextID):
                        print('Fetching QSOs for %s, LOGID %d'%(qso['URCALL'], nextID))
                        query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(nextID, call) )
                        print(query)
                        urqsos = mydb.read_query(query)
                        if (urqsos):
                            print('Source QSO from %s:\n%s'%(call, qso))
                            print('Possible QSLs from %s:\n%s'%(qso['URCALL'], urqsos))
                            """
                            Code to determine/mark QSLs and set QSO VALID status goes here.
                            Need to determine: Is QSO already QSL? - mark valid if so
                            verify DATE/TIME, BAND, MODE, REPORT, QTH - mark QSL and valid if match
                            Mark invalid if no match
                            """
                            qslstatus = None
                            qslIndex = 0
                            while ( (qslstatus == None) and \
                                    (qslIndex < len(urqsos)) ):
                                qslstatus = self.qsoqslCheck(qso,
                                                urqsos[qslIndex])
                                if (qslstatus):
                                    qsostat['STATUS']='QSL'
                                    qsostat['MYQSO'] = qso
                                    qsostat['URQSO'] = urqsos[qslIndex]
                                    statList.append(qsostat)
                                #else:
                                #    qsostat['STATUS']='BUSTED'
                                
                                qslIndex += 1
                                    
                        else: #(if urqsos)
                            """
                            No qsos for nextCall in database.log for QSO with station qso['URCALL']
                            """
                            print('For %s QSO %d, No matching QSOS for station %s in database.'%(call, qso['ID'], nextCall))
                            qsostat['STATUS']='NO URCALL QSOS'
                            qsostat['MYQSO'] = qso
                            qsostat['URQSO'] = None
                            statList.append(qsostat)
                        
                        
                    else: #(if nextID)
                        """
                        No log for QSO with station qso['URCALL']
                        """
                        print('For %s QSO %d, No log for station %s in database.'%(call, qso['ID'], nextCall))
                        qsostat['STATUS']='NO URCALL LOG'
                        qsostat['MYQSO'] = qso
                        qsostat['URQSO'] = None
                        statList.append(qsostat)
            
            else: #(if myqsos)
                """
                The call for supplier parameter call is in
                the database, but no QSOs are recorded.
                Return None for status
                """
                print('No QSOS for %s in database.'%(call))
        
        else: #(if callID)   
            """
            No log for supplied parameter call in the database.
            Return None status
            """
            print('%s not in database.'%(call))
            
        return statList
        
        
    def CallinLogs(self, call, loglist):
        nextID = None
        for nextlog in loglist:
          if (nextlog['CALLSIGN'] == call):
            nextID = nextlog['ID']
            break
        return nextID

    def logtimes(self, logdate, logtime):
       datefmts = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%m-%d-%Y', '%m/%d/%Y']
       timefmts = ['%H%M', '%H:%M', '%H %M']
       logtimeobj = None

       #Date
       d=0
       while (d<5):
           try:
               datefstg = datefmts[d]
               dateobj=datetime.strptime(logdate, datefstg)
               #print(dateobj)
               d=5
           except:
               #print('Format %s did not work for date %s.'%(datefstg, logdate))
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
              #print('Format %s did not work for time %s.'%(timefstg, logtime))
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
    
    mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
    mydb.setCursorDict()
    
    """
    query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
    all_logs = mydb.read_query(query)
    #print(all_logs)

    for thislog in all_logs:
        qslresult = mydb.logqslCheck(thislog['CALLSIGN'], 
                                                    all_logs)
    """
    qslresult = mydb.logqslCheck('W0S')
    if (qslresult):
#            print('STATION %s, LOGID %d:'%(thislog['CALLSIGN'],
#                                           thislog['ID'] ))
            for qsl in qslresult:
#                print('STATUS: %s\tMYQSO: %s\tURQSO: %s'% \
#                       (qsl['STATUS'],
#                        qsl['MYQSO'],
#                        qsl['URQSO'] ))
                print('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%( \
                             qsl['MYQSO']['ID'],
                             qsl['MYQSO']['FREQ'],                             
                             qsl['MYQSO']['MODE'],
                             qsl['MYQSO']['DATE'],
                             qsl['MYQSO']['TIME'],
                             qsl['MYQSO']['MYCALL'],
                             qsl['MYQSO']['MYREPORT'],
                             qsl['MYQSO']['MYQTH'],
                             qsl['MYQSO']['URCALL'],
                             qsl['MYQSO']['URREPORT'],
                             qsl['MYQSO']['URQTH'],
                             qsl['STATUS']))
                if (qsl['STATUS'] == 'QSL'):
                    print('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%( \
                             qsl['URQSO']['ID'],
                             qsl['URQSO']['FREQ'],                             
                             qsl['URQSO']['MODE'],
                             qsl['URQSO']['DATE'],
                             qsl['URQSO']['TIME'],
                             qsl['URQSO']['MYCALL'],
                             qsl['URQSO']['MYREPORT'],
                             qsl['URQSO']['MYQTH'],
                             qsl['URQSO']['URCALL'],
                             qsl['URQSO']['URREPORT'],
                             qsl['URQSO']['URQTH']))
                else:
                    print('%s\n'%(qsl['STATUS'])) 


