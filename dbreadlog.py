#!/usr/bin/env python3
#import MySQLdb
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
        
    def fetchIDQSOSwithCall(self,logID, call):
        thislogqsos = None
        query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(logID, call) )
        print(query)
        thislogqsos = self.read_query(query)
        return thislogqsos
        
    def fetchCallQSOSwithCall(self, mycall, 
                                      urcall, 
                                      loglist = None):
        thislogqsos = None
        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
            all_logs = self.read_query(query)
        
        myID = self.CallinLogDB(mycall, loglist)
        
        if (myID): 
            thislogqsos = self.fetchIDQSOSwithCall(myID, urcall)
        return thislogqsos

    def fetchQSOList(self, qsolist):
        theseqsos = None
        query= ("SELECT * FROM `QSOS` WHERE ( `ID` IN ('%s') )"%(qsolist) )
        print query
        theseqsos = self.read_query(query)
        return theseqsos

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
        qslstat = False
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
        
        #print(timediff)
        #print(timedelta(minutes=45))
        
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
        
        callID = self.CallinLogDB(call, all_logs)
        
        if (callID):
            myqsos = self.fetchlogQSOS(callID)
            if (myqsos):
                statList = []
                for qso in myqsos:
                    qsostat = dict()
                    nextCall = qso['URCALL']
                    nextID = self.CallinLogDB(nextCall, all_logs)
                    if (nextID):
                        print('Fetching QSOs for %s, LOGID %d'%(qso['URCALL'], nextID))
                        #query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(nextID, call) )
                        #print(query)
                        #urqsos = mydb.read_query(query)
                        urqsos = mydb.fetchIDQSOSwithCall(nextID, call):
                        if (urqsos):
                            print('Source QSO from %s:\n%s'%(call, 
                                               self.ahowQSO(qso)))
                            print('Possible QSLs from %s:\n'%(qso['URCALL']))
                            for nq in urqsos:
                                print(self.showQSO(nq))
                            """
                            Code to determine/mark QSLs and set QSO VALID status goes here.
                            Need to determine: Is QSO already QSL? - mark valid if so
                            verify DATE/TIME, BAND, MODE, REPORT, QTH - mark QSL and valid if match
                            Mark invalid if no match
                            """
                            qslstatus = None
                            qslIndex = 0
                            urqsoCount = len(urqsos)
                            while ( (qslstatus == None) and \
                                    (qslIndex < urqsoCount) ):
                                qslstatus = self.qsoqslCheck(qso,
                                                urqsos[qslIndex])
                                if (qslstatus):
                                    qsostat['STATUS']='QSL'
                                    qsostat['MYQSO'] = qso
                                    qsostat['URQSO'] = urqsos[qslIndex]
                                    statList.append(qsostat)
                                
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
        
    def recordQSOStatus(self, qsostat):
        success = None
        qsorec = { 'QSOID': qsostat['MYQSO']['ID'],
                   'QSL': 0,
                   'NOLOG': False,
                   'NOQSOS': False,
                   'VALID': False }
               
        if qsostat['STATUS'] == 'QSL':
            """
            QSL - Save matching QSO ID and set VALID flag
            """
            qsorec['QSL'] = qsostat['URQSO']['ID']
            qsorec['VALID'] = True
        elif: qsostat['STATUS'] == 'NO URCALL QSOS':
            """
            Log for other station exists, but no QSO matching
            this one was found - CLEAR VALID flag
            """
            qsorec['VALID'] = False
            qsorec['NOQSOS'] = True
        elif: qsostat['STATUS'] == 'NO URCALL LOG':
            """
            No Log for other station exists. Give beneit of doubt
            and SET VALID flag
            """
            qsorec['VALID'] = True
            qsorec['NOLOG'] = True
            
            keys = str(testdict.keys())[9:].replace('[', '').replace(']','')
            vals = str(testdict.values())[11:].replace('[','').replace(']','')

            query = ('INSERT INTO QSOSTATUS %s VALUES %s' % (keys, vals))   
            print('Writing QSO status:\n%s'%(query))
            #success = self.write_query(query)
            
            return success
            
        
        
    def CallinLogDB(self, call, loglist=None):
        logID = None
        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
            all_logs = self.read_query(query)
        for nextlog in all_logs:
          if (nextlog['CALLSIGN'] == call):
            logID = nextlog['ID']
            break
        return logID
        
    def showQSO(self, qso):
        fmt = '%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'
        qsoLine = (fmt %( qso['ID'],
                          qso['LOGID'],
                          qso['FREQ'],                             
                          qso['MODE'],
                          qso['DATE'],
                          qso['TIME'],
                          qso['MYCALL'],
                          qso['MYREPORT'],
                          qso['MYQTH'],
                          qso['URCALL'],
                          qso['URREPORT'],
                          qso['URQTH']))
        return qsoLine

    def showQSLdetails(self, qsl):
        reportData = []
        nextLine = self.showQSO(qsl['MYQSO'])
        reportData.append(nextLine)
        if (qsl['STATUS'] == 'QSL'):
            nextLine = self.showQSO(qsl['URQSO'])
            nextLine += '\tQSL'
        else:
            nextLine = ('NO CORROSPONDING QSO DATA AVAILABLE: %s'%(qsl['STATUS'])) 
        reportData.append(nextLine)
        return reportData
    
    def showQSLs(self, qslList):
        reportData = []
        for qsl in qslList:
            nextQSL = self.showQSLdetails(qsl)
            reportData.append(nextLine)
        return reportData
    
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
    testqso1 = { 'ID': 100,
                 'LOGID' : 10,
                 'FREQ' :  '7000',                            
                 'MODE' :  'CW',
                 'DATE' :  '2020/01/23',
                 'TIME' :  '1600',
                 'MYCALL' : 'N0SO', 
                 'MYREPORT' : '599',
                 'MYQTH' :  'STC',
                 'URCALL' : 'K0BX',
                 'URREPORT' : '599',
                 'URQTH' : 'SLC' }
                 
    testqso3 = { 'ID': 102,
                 'LOGID' : 11,
                 'FREQ' :  '7000',                            
                 'MODE' :  'CW',
                 'DATE' :  '2020/01/23',
                 'TIME' :  '1600',
                 'MYCALL' : 'K0BX', 
                 'MYREPORT' : '599',
                 'MYQTH' :  'SLC',
                 'URCALL' : 'N0SO',
                 'URREPORT' : '599',
                 'URQTH' : 'STC' }
    testqso2 = { 'ID': 101,
                 'LOGID' : 10,
                 'FREQ' :  '7000',                            
                 'MODE' :  'CW',
                 'DATE' :  '2020/01/23',
                 'TIME' :  '1558',
                 'MYCALL' : 'N0SO', 
                 'MYREPORT' : '599',
                 'MYQTH' :  'STC',
                 'URCALL' : 'AD0WX',
                 'URREPORT' : '599',
                 'URQTH' : 'SLC' }
                 
    testqso4 = { 'ID': 103,
                 'LOGID' : 12,
                 'FREQ' :  '7000',                            
                 'MODE' :  'CW',
                 'DATE' :  '2020/01/23',
                 'TIME' :  '1627',
                 'MYCALL' : 'AD0WX', 
                 'MYREPORT' : '599',
                 'MYQTH' :  'SLC',
                 'URCALL' : 'N0SO',
                 'URREPORT' : '599',
                 'URQTH' : 'STC' }

    qsl1 = {'STATUS': 'QSL',
            'MYQSO': testqso1,
            'URQSO': testqso2 }
            
    qsl2 = {'STATUS': 'QSL',
            'MYQSO': testqso2,
            'URQSO': testqso1}
    
    mydb = MOQPDBUtils()
    #print(mydb.showQSO(testqso4))
    
    result = mydb.qsoqslCheck(testqso2, testqso4)
    print(result)
    
    """
    qreport = mydb.showQSLdetails(qsl2)
    for line in qreport:
        print(line)
    """
    """
    testobj = mydb.logtimes('2019-04-06', '14:00')
    
    print(testobj)
    exit()
    """
    
    #mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
    #mydb.setCursorDict()
    
    """
    query =  "SELECT `ID`, `CALLSIGN` FROM `logheader` WHERE 1"
    all_logs = mydb.read_query(query)
    #print(all_logs)

    for thislog in all_logs:
        qslresult = mydb.logqslCheck(thislog['CALLSIGN'], 
                                                    all_logs)
    qslresult = mydb.logqslCheck('W0S')
    if (qslresult):
        qslreport = mydb.showQSLs(qslresut)
        for (line in qslreport):
            print line
    """
            
