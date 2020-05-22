#!/usr/bin/env python3
"""
Update History:
* Thu Apr 29 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Retired code from 2019 QSO Party
- and added enhanced log header/QSO checking
- by inheriting from MOQPLogCheck
* Thu May 07 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Added method delete_log
* Sat May 16 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.2 - Updates for 2020 MOQP changes

"""

import MySQLdb
import os.path
import sys, traceback
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

VERSION = '0.1.1' 

from CabrilloUtils import CabrilloUtils
from qsoutils import QSOUtils


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
            traceback.print_exc(file=sys.stdout) 
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
        
    def write_pquery(self, query, params, commit = True):
        qstat = None
        try:
            self.cursor.execute(query, params)
            if (commit):
                self.mydb.commit()
                qstat = self.cursor.lastrowid
        except Exception as e:
            print ("write_pquery Error %s executing query:\n %s %s'"%\
                                           (e.args,
                                            query,
                                            params))  
            traceback.print_exc(file=sys.stdout) 
        return qstat
        
    def read_pquery(self, query, params):
        qresult = None
        qstat = self.write_pquery(query, params)
        try:
            qresult = self.cursor.fetchall()
        except Exception as e:
            print( \
            "read_pquery Error %s reading results from query:\n %s"%\
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
            header = self.read_pquery( \
                "SELECT * FROM `LOGHEADER` WHERE ID=%s", [logID])
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
        #query = "SELECT * FROM SUMMARY WHERE LOGID=%s"%(logID)
        logsum = self.read_pquery(\
            "SELECT * FROM SUMMARY WHERE LOGID=%s", [logID])
        if (logsum): logsum = logsum[0]
        return logsum
 
        
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
            query = "UPDATE SUMMARY SET MOQPCAT='%s', DIGITAL=%s, VHF=%s, ROOKIE=%s, LOCATION='%s' WHERE ID=%s"% \
                    (log['MOQPCAT']['MOQPCAT'], digital_log, vhf_log, rookie_log, log['HEADER']['LOCATION'], sumID)
            ures = self.write_query(query)
        else:
            query = "INSERT INTO SUMMARY ("+\
                    "LOGID, "+\
                    "CWQSO, "+\
                    "PHQSO, "+\
                    "RYQSO, "+\
                    "VHFQSO, "+\
                    "MULTS, "+\
                    "QSOSCORE, "+\
                    "W0MABONUS, "+\
                    "K0GQBONUS, "+\
                    "CABBONUS, "+\
                    "SCORE, "+\
                    "MOQPCAT, "+\
                    "DIGITAL, "+\
                    "VHF, "+\
                    "ROOKIE, "+\
                    "LOCATION) "+\
                    "VALUES "+\
                    "(%s, %s, %s, %s, %s, %s, %s, %s, "+\
                    "%s, %s, %s, %s, %s, %s, %s, %s)"
            params = (   logID,
                         log['QSOSUM']['CW'],
                         log['QSOSUM']['PH'],
                         log['QSOSUM']['DG'],
                         log['QSOSUM']['VHF'],
                         log['MULTS'],
                         log['SCORE']['SCORE'],
                         log['SCORE']['W0MA'],
                         log['SCORE']['K0GQ'],
                         log['SCORE']['CABFILE'],
                         log['SCORE']['TOTAL'],
                         log['MOQPCAT']['MOQPCAT'],
                         digital_log,
                         vhf_log,
                         rookie_log,
                         log['HEADER']['LOCATION'] )
            #print('\n\n\n\nUpdating SUMMARY - query = %s\n%s\n%s,%s,%s'%(query, params,log['SCORE']['W0MA'],log['SCORE']['K0GQ'],log['SCORE']['CABFILE']))
            ures = self.write_pquery(query, params)
        return sumID
    """
    def trimAndEscape(self, unsafeString, maxLen):
        badchars = '\"\''
        if (len(unsafeString) > maxLen):
            workString = unsafeString[:maxLen-1]
        else:
            workString = unsafeString
        for bad in badchars:
            workString = workString.replace(bad, ' ')
        return workString
    """    
       
    def write_header(self, header, cabBonus):
        qutil = QSOUtils()
        logID = None
        header['CREATED-BY'] = \
                  qutil.trimAndEscape(header['CREATED-BY'], 50)
        header['CLUB'] = qutil.trimAndEscape(header['CLUB'], 50)
        header['SOAPBOX'] = \
                  qutil.trimAndEscape(header['SOAPBOX'], 120)
        header['NAME'] = qutil.trimAndEscape(header['NAME'], 40)
        header['ADDRESS'] = \
                  qutil.trimAndEscape(header['ADDRESS'], 120)
        header['ADDRESS-CITY'] = \
                  qutil.trimAndEscape(header['ADDRESS-CITY'], 40)
        header['ADDRESS-STATE-PROVINCE'] = \
          qutil.trimAndEscape(header['ADDRESS-STATE-PROVINCE'], 40)
        header['ADDRESS-POSTALCODE'] = \
          qutil.trimAndEscape(header['ADDRESS-POSTALCODE'], 12)
        header['ADDRESS-COUNTRY'] = \
          qutil.trimAndEscape(header['ADDRESS-COUNTRY'], 25)
        
        if(type(header['NOTES']) is list):
            qu = QSOUtils()
            header['NOTES'] = qu.packNote(header['NOTES'])

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
                      CABBONUS,
                      STATUS)
                   VALUES(%s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s)"""

        values = [header['START-OF-LOG'],
                  header['CALLSIGN'],
                  header['CREATED-BY'],
                  header['LOCATION'],
                  header['CONTEST'],
                  header['NAME'],
                  header['ADDRESS'],
                  header['ADDRESS-CITY'],
                  header['ADDRESS-STATE-PROVINCE'],
                  header['ADDRESS-POSTALCODE'],
                  header['ADDRESS-COUNTRY'],
                  header['EMAIL'],
                  header['CATEGORY-ASSISTED'],
                  header['CATEGORY-BAND'],
                  header['CATEGORY-MODE'],
                  header['CATEGORY-OPERATOR'],
                  header['CATEGORY-OVERLAY'],
                  header['CATEGORY-POWER'],
                  header['CATEGORY-STATION'],
                  header['CATEGORY-TRANSMITTER'],
                  header['CERTIFICATE'],
                  header['OPERATORS'],
                  header['CLAIMED-SCORE'],
                  header['CLUB'],
                  header['IOTA-ISLAND-NAME'],
                  header['OFFTIME'],
                  header['SOAPBOX'],
                  header['END-OF-LOG'],
                  cabBonus,
                  header['NOTES'] ]     
        logID = self.write_pquery(query, values)
        return logID
    
    def write_qsodata(self, logID, qsodata):
        qsoID = None
        if (type(qsodata['NOTES']) is list):
            qu = QSOUtils()
            qsodata['NOTES'] = qu.packNote(qsodata['NOTES'])
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
                                    DUPE,
                                    NOTE)
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
                         ('"%s",'%(qsodata['DUPE'])) +\
                         ('"%s")'%(qsodata['NOTES']))

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
        
    def get_log_parts(self, call):
        log=None
        headerID = self.CallinLogDB(call)
        if (headerID):
            query = "SELECT ID FROM `QSOS` WHERE LOGID=%s" 
            params = [headerID]
            qsos = self.read_pquery(query, params)
            if (qsos):
                log = {'CALL': call,
                       'HEADERID' : headerID,
                       'QSOIDS' : qsos }
        return log
        

    def delete_log(self, call, confirm = False):
        success = False
        headerID = None
        log = self.get_log_parts(call)
        #print(log)
        if (log):
            headerID = log['HEADERID']
            theseqsos = log['QSOIDS']
        if (headerID):
            print('Deleting log %s, LOGID = %d...'%(\
                                                 call,
                                                 headerID))
            if (theseqsos):
                # Delete QSO records
                qcount = len(theseqsos)
                print('Number of QSOS in log %s to delete: %d'\
                                         %(call, qcount))
                thisQ = 0
                for qid in theseqsos:
                    thisQ+=1
                    print('Deleting QSO#%d ID: %d...'%(thisQ, qid['ID']))
                    query = "DELETE FROM `QSOS` WHERE `ID`=%s"
                    params = [qid['ID']]
                    if (self.write_pquery(query, params) \
                                                     == None):
                        print('Error - QSO %d not deleted!'%\
                                                     (QSO['ID']))
                        print('Header and remaining QSOS not deleted.')
                        break                
                if (thisQ == qcount): 
                    """All qsos deleted, delete log SUMMARY, 
                       SHOWE, MISSOURI table entries and then 
                       delete log header.
                       NOTE: Add any future results tables to
                             this list!"""
                    summary = self.read_pquery(\
                      'SELECT ID FROM SUMMARY WHERE LOGID=%s',
                                                   [headerID])
                    if(summary):
                       print('Deleting SUMMARY entry %d for %s, LOGID %d'\
                                %(summary[0]['ID'], call, headerID))
                       self.write_pquery(\
                          'DELETE FROM SHOWME WHERE ID=%s',
                                                  [summary[0]['ID']])
                     
                    showme = self.read_pquery(\
                      'SELECT ID FROM SHOWME WHERE LOGID=%s',
                                                   [headerID])
                    if(showme):
                       print('Deleting SHOWME entry %d for %s, LOGID %d'\
                                %(showme[0]['ID'], call, headerID))
                       self.write_pquery(\
                          'DELETE FROM SHOWME WHERE ID=%s',
                                                  [showme[0]['ID']])
                    mo = self.read_pquery(\
                      'SELECT ID FROM MISSOURI WHERE LOGID=%s',
                                                   [headerID])
                    if(mo):
                       print('Deleting MISSOURI entry %d for %s, LOGID %d'\
                                %(mo[0]['ID'], call, headerID))
                       self.write_pquery(\
                          'DELETE FROM MISSOURI WHERE ID=%s',
                                                  [mo[0]['ID']])
                    params = [headerID]     
                    query = "DELETE FROM LOGHEADER WHERE ID=%s"
                    if (self.write_pquery(query, params)==None):
                         print(\
                           'Log Header %d for call %s not deleted.'%\
                                                     (headerID, call))
                    else:
                         print('Log for call %s deleted!'%(call))
                         success=True                          
            else: 
                print('No QSOS to delete!')        
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
                

            
