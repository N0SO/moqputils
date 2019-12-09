from moqpcategory import MOQPCategory
import os
from moqpdbconfig import *
#import MySQLdb


VERSION = '0.0.1' 


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
            print('%s  %s  %s  %s  %s  %s  %s  %s  %s' \
                    %(qso['FREQ'],
                      qso['MODE'],
                      qso['DATE'],
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
        print('CATEGORY: %s'%(log['MOQPCAT']))
        
    def dbconnect(self, host, user, pw, dbname):
        print('%s, %s, %s, %s'%(host, user, pw, dbname))
        connection = MySQLdb.connect (host = host,
                                  user = user,
                                  passwd = pw,
                                  db = dbname)
                                  
        return connection

        
    def write_header(self, header, catg):
        logID = None
        
        
        return logID
        
    def write_qsodata(self, qsodata):
        qsoID = None
        print('%s  %s  %s  %s  %s  %s  %s  %s  %s' \
                %(qso['FREQ'],
                  qso['MODE'],
                  qso['DATE'],
                  qso['MYCALL'],
                  qso['MYREPORT'],
                  qso['MYQTH'],
                  qso['URCALL'],
                  qso['URREPORT'],
                  qso['URQTH']))
        
        
        
        return qsoID
        
    def write_qsolist(self, qsolist):
        success = None
        for qso in qsolist:
            qID = self.write_qsodata(qso)
            if (qID):
                continue
            else:
                print('Error writing QSO data!')
                break
        
    
            
    def appMain(self, fileName):
        log = self.parseLog(fileName)
        if(log):
            print('MOQPLoadLogs: Importing %s...'%(fileName))    
            self.show_details(log)
            db = self.dbconnect(HOSTNAME, USER, PW, DBNAME)


if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())

"""
'FREQ', 'MODE', 'DATE', 'TIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH'
"""