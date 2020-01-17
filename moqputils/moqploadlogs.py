from moqpcategory import MOQPCategory
import os
from moqpdbconfig import *
from bothawards import BothAwards
import MySQLdb


VERSION = '0.0.2' 


class MOQPLoadLogs(MOQPCategory):

    def __init__(self, filename = None):
        if (filename):
            self.appMain(filename)
            
    def show_header_details(self, header):
        for tag in self.CABRILLOTAGS:
            if (tag in header):
                if (tag in 'QSO END-OF-LOG'):
                    continue
                else:
                    print('%s: %s'%(tag, header[tag]))
                
    def show_qso_details(self,qsolist):
        for qso in qsolist:
            print('%s  %s  %s  %s  %s  %s  %s  %s  %s %s' \
                    %(qso['FREQ'],
                      qso['MODE'],
                      qso['DATE'],
                      qso['TIME'],
                      qso['MYCALL'],
                      qso['MYREPORT'],
                      qso['MYQTH'],
                      qso['URCALL'],
                      qso['URREPORT'],
                      qso['URQTH']))
            
    def show_details(self, log):
        print(log.keys())
        self.show_header_details(log['HEADER'])
        self.show_qso_details(log['QSOLIST'])
        print('CATEGORY: %s'%(log['MOQPCAT']['MOQPCAT']))
        
    def dbconnect(self, host, user, pw, dbname):
        print('%s, %s, %s, %s'%(host, user, pw, dbname))
        connection = MySQLdb.connect (host = host,
                                  user = user,
                                  passwd = pw,
                                  db = dbname)
                                  
        return connection

    def _write_query(self, db, query):
        qstat = None
        print('Writeing query Data: %s'%(query))
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        qstat = cursor.lastrowid
        return qstat
       
    def write_header(self, db, header, catg, qsostatus):
        logID = None

        query = """INSERT INTO logheader(START,
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
                      MOQPCAT,
                      STATUS)
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
                        ('"%s",'%(catg)) +\
                        ('"%s")'%(qsostatus))      
        logID = self._write_query(db, query)
        """
        #print('query = %s'%(query))
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        logID = cursor.lastrowid
        """
        return logID
        
    def write_qsodata(self, db, logID, qsodata):
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
                                    URQTH)
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
                         ('"%s")'%(qsodata['URQTH']))

        qsoID = self._write_query(db, query)
        """
        print('Writeing QSO data Data: %s'%(query))
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        qsoID = cursor.lastrowid
        """
        return qsoID

    def writeSummary(self, db, logID, log, smresult):
        if (smresult['BONUS']['W0MA']):
            w0mabonus = 100
        else:
            w0mabonus = 0

        if (smresult['BONUS']['K0GQ']):
            k0gqbonus = 100
        else:
            k0gqbonus = 0

        cabbonus = 0

        if (log['MOQPCAT']['DIGITAL'] == 'DIGITAL'):
            digital_log = True
        else:
            digital_log = False

        if (log['MOQPCAT']['VHF'] == 'VHF'):
            vhf_log = True
        else:
            vhf_log = False

        if (log['MOQPCAT']['ROOKIE'] == 'ROOKIE'):
            rookie_log = True
        else:
            rookie_log = False

        query = """INSERT INTO SUMMARY(LOGID,
                                       CWQSO,
                                       PHQSO,
                                       RYQSO,
                                       VHFQSO,
                                       MULTS,
                                       QSOSCORE,
                                       W0MABONUS,
                                       K0GQBONUS,
                                       CABBONUS,
                                       MOQPCAT,
                                       DIGITAL,
                                       VHF,
                                       ROOKIE)
                      VALUES(""" + \
                         ('"%d",'%(logID)) +\
                         ('"%d",'%(log['QSOSUM']['CW'])) +\
                         ('"%d",'%(log['QSOSUM']['PH'])) +\
                         ('"%d",'%(log['QSOSUM']['DG'])) +\
                         ('"%d",'%(log['QSOSUM']['VHF'])) +\
                         ('"%d",'%(log['MULTS'])) +\
                         ('"%d",'%(log['SCORE'])) +\
                         ('"%d",'%(w0mabonus)) +\
                         ('"%d",'%(k0gqbonus)) +\
                         ('"%d",'%(cabbonus)) +\
                         ('"%s",'%(log['MOQPCAT']['MOQPCAT'])) +\
                         ('"%d",'%(digital_log)) +\
                         ('"%d",'%(vhf_log)) +\
                         ('"%d")'%(rookie_log))

        sumID = self._write_query(db, query)
        return sumID
        
    def writeSHOWME(self, db, logID, smresult):

        query = """INSERT INTO SHOWME(LOGID,
                                       S,
                                       H,
                                       O,
                                       W,
                                       M,
                                       E,
                                       WC,
                                       QUALIFY)
                      VALUES(""" + \
                         ('"%d",'%(logID)) +\
                         ('"%s",'%(smresult['CALLS']['S'])) +\
                         ('"%s",'%(smresult['CALLS']['H'])) +\
                         ('"%s",'%(smresult['CALLS']['O'])) +\
                         ('"%s",'%(smresult['CALLS']['W'])) +\
                         ('"%s",'%(smresult['CALLS']['M'])) +\
                         ('"%s",'%(smresult['CALLS']['E'])) +\
                         ('"%s",'%(smresult['WILDCARD'])) +\
                         ('"%d")'%(smresult['QUALIFY']))

        sumID = self._write_query(db, query)
        return sumID

    def writeMO(self, db, logID, smresult):

        query = """INSERT INTO MISSOURI(LOGID,
                                       M,
                                       I_1,
                                       S_1,
                                       S_2,
                                       O,
                                       U,
                                       R,
                                       I_2,
                                       WC,
                                       QUALIFY)
                      VALUES(""" + \
                         ('"%d",'%(logID)) +\
                         ('"%s",'%(smresult['CALLS']['M'])) +\
                         ('"%s",'%(smresult['CALLS']['I0'])) +\
                         ('"%s",'%(smresult['CALLS']['S0'])) +\
                         ('"%s",'%(smresult['CALLS']['S1'])) +\
                         ('"%s",'%(smresult['CALLS']['O'])) +\
                         ('"%s",'%(smresult['CALLS']['U'])) +\
                         ('"%s",'%(smresult['CALLS']['R'])) +\
                         ('"%s",'%(smresult['CALLS']['I1'])) +\
                         ('"%s",'%(smresult['WILDCARD'])) +\
                         ('"%d")'%(smresult['QUALIFY']))

        sumID = self._write_query(db, query)
        return sumID

    def write_qsolist(self, db, logID, qsolist):
        success = None

        for qso in qsolist:
            qID = self.write_qsodata(db, logID, qso)
            if (qID):
                continue
            else:
                print('Error writing QSO data!')
                break
            
    def appMain(self, fileName):
        log = self.parseLog(fileName)
#        print(log)
#        dir(log)
        if(log):
            bawards = BothAwards()
            smresult = (bawards.appMain(\
                        log['HEADER']['CALLSIGN'],
                        log['QSOLIST']))
            print(dir(smresult))
            print(smresult)
            print('MOQPLoadLogs: Importing %s...'%(fileName))    
            self.show_details(log)
            db = self.dbconnect(HOSTNAME, USER, PW, DBNAME)
            cursor = db.cursor()
            cursor.execute ("SELECT VERSION()")
            row = cursor.fetchone()
            print("server version:", row[0])
            logID = self.write_header(db, log['HEADER'], 
                              log['MOQPCAT']['MOQPCAT'],
                              'QSOSTATUS')
            if (logID):
                self.write_qsolist(db, logID, log['QSOLIST'])
                self.writeSummary(db, logID, log, smresult)
                self.writeSHOWME(db, logID, smresult['SHOWME'])
                self.writeMO(db, logID, smresult['MO'])
            cursor.close()
            db.close()

if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())

"""
'FREQ', 'MODE', 'DATE', 'TIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH'
"""
