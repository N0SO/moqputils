#!/usr/bin/env python3
"""
Update History:
* Thu Apr 29 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Retired code from 2019 QSO Party
- and added enhanced log header/QSO checking
- by inheriting from MOQPLogCheck
"""

import MySQLdb
import os.path
import sys
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

VERSION = '0.1.0' 
"""
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
from CabrilloUtils import CabrilloUtils
"""


class MOQPDBUtils():

    def __init__(self, host = None, 
                       user = None, 
                       passwd = None, 
                       database = None):
       if (host):
           #print('Attempting connection to: %s as:%s pw:%s db:%s'%(host, user, passwd, database))
           self.mydb = self.connectDB(host, 
                                  user, 
                                  passwd, 
                                  database)
           if (self.mydb):
               self.setCursor()
               #self.cursor = None
           else:
               print("Error connecting to %s database %s:\n%s"%(host, database, e))
          
    def connectDB(self, host, 
                        user, 
                        passwd, 
                        database):
        mydb = None
        try:                 
            mydb = MySQLdb.connect(
              host,
              user,
              passwd,
              database
            )
        except Exception as e:
            print ("Error connecting to database %s: %s"%\
                                           (database,e.args))    
                       
        return mydb

    def setCursor(self):
        self.cursor = self.mydb.cursor()

    def setCursorDict(self):
        self.cursor = self.mydb.cursor(MySQLdb.cursors.DictCursor)
        
    def write_query(self, query, commit = True):
        qstat = None
        #if (db == None): db = self.mydb
        try:
            self.cursor.execute(query)
            if (commit):
                self.mydb.commit()
                qstat = self.cursor.lastrowid
                #qresult = self.cursor.fetchall()
                #print(qresult)
        except Exception as e:
            print ("write_query Error %s executing query:\n %s"%\
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
        
    def fetchLogList(self):
        """
        Return a list o all calls in database with LOGID.
        """
        loglist = None
        loglist = self.read_query( \
               "SELECT ID, CALLSIGN FROM LOGHEADER WHERE 1")
        return loglist

    def fetchlogQSOS(self, callID):
        thislogqsos = None        
        query= ("SELECT * FROM `QSOS` WHERE `LOGID` = %d"%(callID) )
        thislogqsos = self.read_query(query)

        return thislogqsos
        
    def fetchIDQSOSwithCall(self,logID, call):
        thislogqsos = None
        query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(logID, call) )
        #print(query)
        thislogqsos = self.read_query(query)
        return thislogqsos
        
    def fetchCallQSOSwithCall(self, mycall, 
                                      urcall, 
                                      loglist = None):
        thislogqsos = None
        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `LOGHEADER` WHERE 1"
            all_logs = self.read_query(query)
        
        myID = self.CallinLogDB(mycall, loglist)
        
        if (myID): 
            thislogqsos = self.fetchIDQSOSwithCall(myID, urcall)
        return thislogqsos

    def fetchQSOList(self, qsolist):
        theseqsos = None
        query= ("SELECT * FROM `QSOS` WHERE ( `ID` IN ('%s') )"%(qsolist) )
        #print(query)
        theseqsos = self.read_query(query)
        return theseqsos

    def fetchLogHeader(self, call):
        header = None
        logID = self.CallinLogDB(call)
        if (logID):
            header = self.read_query( \
                "SELECT * FROM `LOGHEADER` WHERE ID=%d"%(logID))
        return header

    def fetchCABHeader(self, call):
        """ 
        Fetch log file header for call from database.
        """
        header = None
        dheader = None
        dbheader = self.fetchLogHeader(call)
        if dbheader:
            cab = CabrilloUtils()
            header = cab.makeHEADERdict()
            header['START-OF-LOG'] = dbheader[0]['START']
            header['CALLSIGN'] = dbheader[0]['CALLSIGN']
            header['CREATED-BY'] = dbheader[0]['CREATEDBY']
            header['LOCATION'] = dbheader[0]['LOCATION']
            header['CONTEST'] = dbheader[0]['CONTEST']
            header['NAME'] = dbheader[0]['NAME']
            header['ADDRESS'] = dbheader[0]['ADDRESS']
            header['ADDRESS-CITY'] = dbheader[0]['CITY']
            header['ADDRESS-STATE-PROVINCE'] = dbheader[0]['STATEPROV']
            header['ADDRESS-POSTALCODE'] = dbheader[0]['ZIPCODE']
            header['ADDRESS-COUNTRY'] = dbheader[0]['COUNTRY']
            header['EMAIL'] = dbheader[0]['EMAIL']
            header['CATEGORY-ASSISTED'] = dbheader[0]['CATASSISTED']
            header['CATEGORY-BAND'] = dbheader[0]['CATBAND']
            header['CATEGORY-MODE'] = dbheader[0]['CATMODE']
            header['CATEGORY-OPERATOR'] = dbheader[0]['CATOPERATOR']
            header['CATEGORY-OVERLAY'] = dbheader[0]['CATOVERLAY']
            header['CATEGORY-POWER'] = dbheader[0]['CATPOWER']
            header['CATEGORY-STATION'] = dbheader[0]['CATSTATION']
            header['CATEGORY-TRANSMITTER'] = dbheader[0]['CATXMITTER']
            header['CATEGORY-TIME'] = ''
            header['CERTIFICATE'] = dbheader[0]['CERTIFICATE']
            header['OPERATORS'] = dbheader[0]['OPERATORS']
            header['CLAIMED-SCORE'] = dbheader[0]['CLAIMEDSCORE']
            header['CLUB'] = dbheader[0]['CLUB']
            header['IOTA-ISLAND-NAME'] = dbheader[0]['IOTAISLANDNAME']
            header['OFFTIME'] = dbheader[0]['OFFTIME']
            header['SOAPBOX'] = dbheader[0]['SOAPBOX']
        return header

    def fetchValidQSOS(self, call):
        thislogqsos = None
        logID = self.CallinLogDB(call)
        query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID`=%d) AND (VALID=1) )"%(logID) )
        #print(query)
        thislogqsos = self.read_query(query)
        return thislogqsos
        
    def fetchValidLog(self, call):
        """
        Fetch log header with a list of valid QSOs.
        returns a log dictionary objetct:
           { HEADER: logheader (in dict() format)
           { OQSOLIST: qsos - A list of valid QSOs 
        """
        header = self.fetchCABHeader(call)
        qsos = self.fetchValidQSOS(call)
        return { 'HEADER':header, 'QSOLIST':qsos }

    def fetchLogSummary(self, call):
        logsum = None
        logID = self.CallinLogDB(call)
        query = "SELECT * FROM SUMMARY WHERE LOGID=%s"%(logID)
        logsum = self.read_query(query)
        return logsum[0]
 
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
        logerrors = []
        gutil = GenAward()
        cabutil = CabrilloUtils()
        """
        TBD - compare date/time, BAND, MODE, REPORT, QTH
        """

        count = len(myqso['TIME'])
        if (count != 4):
            newtime = self.padtime(myqso['TIME'])
            print('QSO %d: Time string wrong length - changing %s to %s...'%(myqso['ID'], myqso['TIME'], newtime))
            myqso['TIME'] = newtime
            
        count = len(urqso['TIME'])
        if (count != 4):
            newtime = self.padtime(urqso['TIME'])
            print('QSO %d: Time string wrong length - changing %s to %s...'%(urqso['ID'], urqso['TIME'], newtime))
            urqso['TIME'] = newtime
            
        myqtime = self.logtimes(myqso['DATE'], myqso['TIME'])
        urqtime = self.logtimes(urqso['DATE'], urqso['TIME'])
        myqband = gutil.getBand(myqso['FREQ'])
        urqband = gutil.getBand(urqso['FREQ'])
        urqsomycall = cabutil.stripCallsign(urqso['MYCALL'])
        myqsourcall = cabutil.stripCallsign(myqso['URCALL'])

        if (myqtime > urqtime):
            timediff = myqtime - urqtime
        else:
            timediff = urqtime - myqtime
        
        #print('MYQSO: %s\nURQSO: %s'%(myqso, urqso))
        #print('Time difference: %s, MYCALL: %s, URCALL:%s'%(timediff, myqsourcall, urqsomycall))
        
        if ( (timediff < timedelta(minutes=30) ) and \
             (myqband == urqband) and \
             (myqso['MODE'] == urqso['MODE']) and \
             (myqsourcall == urqsomycall) and \
             (myqso['URQTH'] == urqso['MYQTH']) and \
             (myqso['URREPORT'] != '') ):
            qslstat = True
            #print('QSL!\n')
        else:
            logerrors.append('%s...'%(self.showQSO(urqso)))
            #logerrors.append('for MYQSO %d, tried URQSO: %d...'%(myqso['ID'], urqso['ID']))
            if (timediff > timedelta(minutes=30)):
                logerrors.append('Log time diff: %s > than 30 min.'%(timediff))
            if (myqband != urqband):
                logerrors.append('BAND does not match')
            if (myqsourcall != urqsomycall):
                logerrors.append('CALLSIGN %s in URREPORT does not match CALLSIGN %s in MYREPORT.'%(myqsourcall, urqsomycall))
            if (myqso['URQTH'] != urqso['MYQTH']):
                logerrors.append('QTH %s in URREPORT does not match QTH %s in MYREPORT'%(myqso['URQTH'], urqso['MYQTH']))
            if (myqso['URREPORT'] == ''):
                logerrors.append('REPORT %s looks bogus'%(myqso['URREPORT']))
        if (logerrors == []):
            logerrors = None
        return { 'QSLSTAT':qslstat,
                 'QSLERR':logerrors }
        
    def logqslCheck(self, call, loglist = None):
        statList = None

        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `LOGHEADER` WHERE 1"
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
                        #print('Fetching QSOs for %s, LOGID %d'%(qso['URCALL'], nextID))
                        #query= ("SELECT * FROM `QSOS` WHERE ( (`LOGID` = %d) AND (`URCALL` IN ('%s')) )"%(nextID, call) )
                        #print(query)
                        #urqsos = mydb.read_query(query)
                        urqsos = self.fetchIDQSOSwithCall(nextID, call)
                        if (urqsos):
                            
                            print('Source QSO from %s:\n%s'%(call, 
                                               self.showQSO(qso)))
                            print('Possible QSLs from %s:\n'%(qso['URCALL']))
                            for nq in urqsos:
                                print(self.showQSO(nq))
                            
                            qslstatus = False
                            qslIndex = 0
                            urqsoCount = len(urqsos)
                            urqsoerrors = []
                            while ( (qslstatus == False) and \
                                    (qslIndex < urqsoCount) ):
                                #print('Checking:\n%s\n%s\n\n'%(qso, urqsos[qslIndex]))
                                qsostatus = self.qsoqslCheck(qso,
                                                urqsos[qslIndex])
                                qslstatus = qsostatus['QSLSTAT']
                                if (qslstatus):
                                    qsostat['STATUS']='QSL'
                                    qsostat['MYQSO'] = qso
                                    qsostat['URQSO'] = urqsos[qslIndex]
                                    statList.append(qsostat)
                                else: # Save reason for no match this QSO
                                    for ln in qsostatus['QSLERR']:
                                        urqsoerrors.append(ln)
                                qslIndex += 1
                                #print(qslIndex, qslstatus)

                            if (qslstatus == False):
                                """
                                QSOs with URCALL found, but none 
                                match this QSO - Busted?
                                """
                                qsostat['STATUS']='BUSTED'
                                qsostat['MYQSO'] = qso
                                qsostat['URQSO'] = urqsoerrors
                                statList.append(qsostat)
                                    
                        else: #(if urqsos)
                            """
                            No qsos for nextCall in database.log for QSO with station qso['URCALL']
                            """
                            #print('For %s QSO %d, No matching QSOS for station %s in database.'%(call, qso['ID'], nextCall))
                            qsostat['STATUS']='NO URCALL QSOS'
                            qsostat['MYQSO'] = qso
                            qsostat['URQSO'] = None
                            statList.append(qsostat)
                        
                        
                    else: #(if nextID)
                        """
                        No log for QSO with station qso['URCALL']
                        """
                        #print('For %s QSO %d, No log for station %s in database.'%(call, qso['ID'], nextCall))
                        qsostat['STATUS']='NO URCALL LOG'
                        qsostat['MYQSO'] = qso
                        qsostat['URQSO'] = None
                        statList.append(qsostat)

                    self.recordQSOStatus(qsostat)            

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
                   'VALID': False,
                   'NOTE': ' '}
               
        if qsostat['STATUS'] == 'QSL':
            """
            QSL - Save matching QSO ID and set VALID flag
            """
            qsorec['QSL'] = qsostat['URQSO']['ID']
            qsorec['VALID'] = True
        elif qsostat['STATUS'] == 'BUSTED':
            """
            QSOS with URCALL found, but no match
            to this QSO
            """
            qsorec['VALID'] = False
        elif qsostat['STATUS'] == 'NO URCALL QSOS':
            """
            Log for other station exists, but no QSO matching
            this one was found - CLEAR VALID flag
            """
            qsorec['VALID'] = False
            qsorec['NOQSOS'] = True
        elif qsostat['STATUS'] == 'NO URCALL LOG':
            """
            No Log for other station exists. Give beneit of doubt
            and SET VALID flag
            """
            qsorec['VALID'] = True
            qsorec['NOLOG'] = True
            
        """
        keys = str(qsorec.keys())[9:].replace('[', '').replace(']','')
        vals = str(qsorec.values())[11:].replace('[','').replace(']','')
        query = 'INSERT INTO QSOSTATUS %s VALUES %s' % (keys, vals)
        """
        
        query="UPDATE QSOS SET QSL=%d, VALID=%s, NOLOG=%s, NOQSOS=%s WHERE ID=%s" % \
                 (qsorec['QSL'], qsorec['VALID'], qsorec['NOLOG'],
                                 qsorec['NOQSOS'], qsorec['QSOID'])

        #print('Writing QSO status:\n%s'%(query))
        success = self.write_query(query)
            
        return success
        
    def CallinLogDB(self, call, loglist=None):
        logID = None
        if (loglist):
            all_logs = loglist
        else:
            query =  "SELECT `ID`, `CALLSIGN` FROM `LOGHEADER` WHERE 1"
            all_logs = self.read_query(query)
        if(all_logs):
            for nextlog in all_logs:
               #print(call, nextlog['CALLSIGN'])
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
        #print(qsl)
        reportData = []
        nextLine = self.showQSO(qsl['MYQSO'])
        if (qsl['STATUS'] == 'QSL'): nextLine += '\tQSL'
        reportData.append(nextLine)
        if (qsl['STATUS'] == 'QSL'):
            nextLine = self.showQSO(qsl['URQSO'])
        else:
            if (qsl['STATUS'] == 'BUSTED'):
                """Show result of QSOs compared"""
                #print('BUSTED: %s'%(qsl['URQSO']))
                nextLine = ''
                for qsotry in qsl['URQSO']:
                    nextLine += qsotry +'\n'
                #print('BUSTEDP: %s'%(nextline))
            else:
                nextLine = ('NO CORROSPONDING QSO DATA AVAILABLE: %s'%(qsl['STATUS'])) 
        reportData.append(nextLine)
        return reportData
    
    def showQSLs(self, qslList):
        reportData = []
        for qsl in qslList:
            nextQSL = self.showQSLdetails(qsl)
            reportData.append(nextQSL)
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

    def writeSummary(self, log):
        sumID = None

        if (log['MOQPCAT']['DIGITAL'] == 'DIGITAL'):
            digital_log = 1
        else:
            digital_log = 0

        if (log['MOQPCAT']['VHF'] == 'VHF'):
            vhf_log = 1
        else:
            vhf_log = 0

        if (log['MOQPCAT']['ROOKIE'] == 'ROOKIE'):
            rookie_log = 1
        else:
            rookie_log = 0

        #Does a record for this log exist already?
        logID = self.CallinLogDB(log['HEADER']['CALLSIGN'])
        logsum = self.read_query("SELECT * FROM SUMMARY WHERE LOGID=%s"%(logID))
        #print('logsum=%s'%(logsum))
        if (logsum):
            sumID = logsum[0]['ID']
            #print('sumID=%s'%(sumID))
            #update totals and score
            query = 'UPDATE SUMMARY SET CWQSO=%s, PHQSO=%s, RYQSO=%s, VHFQSO=%s, MULTS=%s, QSOSCORE=%s WHERE ID=%s'% \
                    (log['QSOSUM']['CW'], log['QSOSUM']['PH'], log['QSOSUM']['DG'], 
                     log['QSOSUM']['VHF'], log['MULTS'], log['SCORE']['SCORE'], sumID)
            ures = self.write_query(query)
            #update bonus stats
            query = 'UPDATE SUMMARY SET W0MABONUS=%s, K0GQBONUS=%s, CABBONUS=%s, SCORE=%s WHERE ID=%s'% \
                    (log['SCORE']['W0MA'], log['SCORE']['K0GQ'], log['SCORE']['CABFILE'], log['SCORE']['TOTAL'], sumID)
            ures = self.write_query(query)
            query = "UPDATE SUMMARY SET MOQPCAT='%s', DIGITAL=%s, VHF=%s, ROOKIE=%s WHERE ID=%s"% \
                    (log['MOQPCAT']['MOQPCAT'], digital_log, vhf_log, rookie_log, sumID)
            ures = self.write_query(query)
        else:
            query = "INSERT INTO SUMMARY LOGID=%s, \
                                        CWQSO=%s, \
                                        PHQSO=%s, \
                                        RYQSO=%s, \
                                        VHFQSO=%s, \
                                        MULTS=%s, \
                                        QSOSCORE=%s, \
                                        W0MABONUS=%s, \
                                        K0GQBONUS=%s, \
                                        CABBONUS=%s, \
                                        MOQPCAT=%s, \
                                        DIGITAL=%s, \
                                        VHF=%s, \
                                        ROOKIE=%s" % \
                         (logID,
                         log['QSOSUM']['CW'],
                         log['QSOSUM']['PH'],
                         log['QSOSUM']['DG'],
                         log['QSOSUM']['VHF'],
                         log['MULTS'],
                         log['SCORE'],
                         w0mabonus,
                         k0gqbonus,
                         cabbonus,
                         log['MOQPCAT']['MOQPCAT'],
                         digital_log,
                         vhf_log,
                         rookie_log)
        #print('\n\n\n\nUpdating SUMMARY - query = %s'%(query))
        ures = self.write_query(query)
        return sumID

    def trimAndEscape(self, unsafeString, maxLen):
        badchars = '\"\''
        if (len(unsafeString) > maxLen):
            workString = unsafeString[:maxLen-1]
        else:
            workString = unsafeString
        for bad in badchars:
            workString = workString.replace(bad, ' ')
        return workString
        
       
    def write_header(self, header, cabBonus):
        logID = None
        header['CREATED-BY'] = \
                  self.trimAndEscape(header['CREATED-BY'], 50)
        header['CLUB'] = self.trimAndEscape(header['CLUB'], 50)
        header['SOAPBOX'] = \
                  self.trimAndEscape(header['SOAPBOX'], 120)
        header['NAME'] = self.trimAndEscape(header['NAME'], 40)
        header['ADDRESS'] = \
                  self.trimAndEscape(header['ADDRESS'], 120)
        header['ADDRESS-CITY'] = \
                  self.trimAndEscape(header['ADDRESS-CITY'], 40)
        header['ADDRESS-STATE-PROVINCE'] = \
          self.trimAndEscape(header['ADDRESS-STATE-PROVINCE'], 40)
        header['ADDRESS-POSTALCODE'] = \
          self.trimAndEscape(header['ADDRESS-POSTALCODE'], 12)
        header['ADDRESS-COUNTRY'] = \
          self.trimAndEscape(header['ADDRESS-COUNTRY'], 25)

        query = """INSERT INTO LOGHEADER(START,
                      CALLSIGN,
                      CREATEDBY,
                      LOCATION, 
                      CONTEST,
                      NAME,
                      ADDRESS,
                      CITY,
                      STATEPROV,
                      ZIPCODE,
                      COUNTRY,
                      EMAIL,
                      CATASSISTED,
                      CATBAND,
                      CATMODE,
                      CATOPERATOR,
                      CATOVERLAY,
                      CATPOWER,
                      CATSTATION,
                      CATXMITTER,
                      CERTIFICATE,
                      OPERATORS,
                      CLAIMEDSCORE,
                      CLUB,
                      IOTAISLANDNAME,
                      OFFTIME,
                      SOAPBOX,
                      ENDOFLOG,
                      CABBONUS)
                   VALUES(""" + \
                        ('"%s",'%(header['START-OF-LOG'])) +\
                        ('"%s",'%(header['CALLSIGN'])) +\
                        ('"%s",'%(header['CREATED-BY'])) +\
                        ('"%s",'%(header['LOCATION'])) +\
                        ('"%s",'%(header['CONTEST'])) +\
                        ('"%s",'%(header['NAME'])) +\
                        ('"%s",'%(header['ADDRESS'])) +\
                        ('"%s",'%(header['ADDRESS-CITY'])) +\
                        ('"%s",'%(header['ADDRESS-STATE-PROVINCE'])) +\
                        ('"%s",'%(header['ADDRESS-POSTALCODE'])) +\
                        ('"%s",'%(header['ADDRESS-COUNTRY'])) +\
                        ('"%s",'%(header['EMAIL'])) +\
                        ('"%s",'%(header['CATEGORY-ASSISTED'])) +\
                        ('"%s",'%(header['CATEGORY-BAND'])) +\
                        ('"%s",'%(header['CATEGORY-MODE'])) +\
                        ('"%s",'%(header['CATEGORY-OPERATOR'])) +\
                        ('"%s",'%(header['CATEGORY-OVERLAY'])) +\
                        ('"%s",'%(header['CATEGORY-POWER'])) +\
                        ('"%s",'%(header['CATEGORY-STATION'])) +\
                        ('"%s",'%(header['CATEGORY-TRANSMITTER'])) +\
                        ('"%s",'%(header['CERTIFICATE'])) +\
                        ('"%s",'%(header['OPERATORS'])) +\
                        ('"%s",'%(header['CLAIMED-SCORE'])) +\
                        ('"%s",'%(header['CLUB'])) +\
                        ('"%s",'%(header['IOTA-ISLAND-NAME'])) +\
                        ('"%s",'%(header['OFFTIME'])) +\
                        ('"%s",'%(header['SOAPBOX'])) +\
                        ('"%s",'%(header['END-OF-LOG'])) +\
                        ('"%d")'%(cabBonus))      
        logID = self.write_query(query)
        return logID
    
    def write_qsodata(self, logID, qsodata):
        qsoID = None
        query = """INSERT INTO QSOS(LOGID,
                                    FREQ,
                                    MODE,
                                    DATE,
                                    TIME,
                                    MYCALL,
                                    MYREPORT,
                                    MYQTH,
                                    URCALL,
                                    URREPORT,
                                    URQTH,
                                    DUPE)
                      VALUES(""" + \
                         ('"%d",'%(logID)) +\
                         ('"%s",'%(qsodata['FREQ'])) +\
                         ('"%s",'%(qsodata['MODE'])) +\
                         ('"%s",'%(qsodata['DATE'])) +\
                         ('"%s",'%(qsodata['TIME'])) +\
                         ('"%s",'%(qsodata['MYCALL'])) +\
                         ('"%s",'%(qsodata['MYREPORT'])) +\
                         ('"%s",'%(qsodata['MYQTH'])) +\
                         ('"%s",'%(qsodata['URCALL'])) +\
                         ('"%s",'%(qsodata['URREPORT'])) +\
                         ('"%s",'%(qsodata['URQTH'])) +\
                         ('"%s")'%(qsodata['DUPE']))

        qsoID = self.write_query(query)
        return qsoID

    def write_qsolist(self, logID, qsolist):
        success = False
        #qcount = 0
        qidlist = []
        #oqidlist = []

        for qso in qsolist:
            if (qso['DUPE'] > 0):
                di = qso['DUPE']
                if (di >= 1):
                    qso['DUPE'] = qidlist[di-1]
            qID = self.write_qsodata(logID, qso)
            if (qID):
                qidlist.append(qID)
                success = True
                #oqidlist.append(qso['DUPE'])
                #qcount += 1
            else:
                print('Error writing QSO data!')
                success = False
                break
        #print(oqidlist, qidlist)
        return success
       

if __name__ == '__main__':
    
    mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
    mydb.setCursorDict()

    qslresult = mydb.logqslCheck('N0SO')
    print(qslresult)
    if (qslresult):
        qslreport = mydb.showQSLs(qslresult)
        for qreport in qslreport:
                print(qreport[0])
                print(qreport[1])
                print()
                

            
