#!/usr/bin/env python3
"""
Update History:
* Tue May 12 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Separated this code from the MOQPDBUtils code.
- Enhancd QSL checks from 2019 QSO Party.
* Mon May 25 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Added call to self.modeSet method to set 
- all digimodes to RY and all phone modes to PH for QSL checking.
"""

from datetime import timedelta
from qsoutils import QSOUtils
from moqpdefs import *


class MOQPQSOValidator(QSOUtils):

    def __init__(self, db = None):
        self.db = db
       
    def qso_valid(self, qso):
       errorData = []
       qsovalid = True
       valid_date_chars = set('0123456789/-')
       valid_call_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-')
       qutils = QSOUtils()
       if ( self.is_number(qso['FREQ']) ):
          if (qutils.getBand(qso['FREQ'])):
              pass
          else:
              errorData.append( \
              ('QSO FREQ Parameter out of band: %s'%(qso['FREQ'])) )
       else:
          errorData.append( ('QSO FREQ Parameter invalid: %s'%(qso['FREQ'])) )
          qsovalid = False
       
       if ( qso['MODE'] in self.MODES ):
          pass
       else:
          errorData.append(  ('QSO MODE Parameter invalid: %s'%(qso['MODE'])) )
          qsovalid = False
       if all(char in valid_date_chars for char in qso['DATE']):
          pass
       else:
          errorData.append(  ('QSO DATE Parameter invalid: %s'%(qso['DATE'])) )
          qsovalid = False
          qso['DATE'] = None
       if ( qso['TIME'].isnumeric() ):
          pass
       else:
          errorData.append(  ('QSO TIME Parameter invalid: %s'%(qso['TIME'])) )
          qsovalid = False
          qso['TIME'] = None
       if ( qso['DATE'] and qso['TIME'] ):
          if (qutils.validateQSOtime(qso['DATE'], qso['TIME'])):
             pass
          else:
             errorData.append(  (\
              'QSO DATE/TIME outside contest time period: %s %s'\
               %(qso['DATE'],
                 qso['TIME'])) )
       if all(char in valid_call_chars for char in qso['MYCALL']):
          pass
       else:
          errorData.append(  ('QSO MYCALL Parameter invalid: %s'%(qso['MYCALL'])) )
          qsovalid = False

       if ( self.is_number(qso['MYREPORT']) ):
          if (self.validate_Report_Mode(qso['MYREPORT'], qso['MODE'])):
              pass
          else:
              errorData.append( \
                'QSO MY SIG REPORT %s does not match MODE: %s'%\
                (qso['MYREPORT'],
                 qso['MODE']) )
              qsovalid = False
       else:
          errorData.append(  ('QSO MYREPORT Parameter invalid: %s'%(qso['MYREPORT'])) )
          qsovalid = False

       if ( (qso['MYQTH'].isalpha()) and (\
            (qso['MYQTH'] in MOCOUNTY) or \
               (qso['MYQTH'] in US) or \
               (qso['MYQTH'] in CANADA) or \
               (qso['MYQTH'] in DX) ) ): 
          pass
       else:
          errorData.append(  ('QSO MYQTH Parameter invalid: %s'%(qso['MYQTH'])) )
          qsovalid = False

       if all(char in valid_call_chars for char in qso['URCALL']):
          pass
       else:
          errorData.append(  ('QSO URCALL Parameter invalid: %s'%(qso['URCALL'])) )
          qsovalid = False

       if ( self.is_number(qso['URREPORT']) ):
          if (self.validate_Report_Mode(qso['URREPORT'], qso['MODE'])):
              pass
          else:
              errorData.append( \
                'QSO UR SIG REPORT %s does not match MODE: %s'%\
                (qso['URREPORT'],
                 qso['MODE']) )
              qsovalid = False
       else:
          errorData.append(  ('QSO URREPORT Parameter invalid: %s'%(qso['URREPORT'])) )
          qsovalid = False

       if ( (qso['URQTH'].isalpha()) and (\
            (qso['URQTH'] in MOCOUNTY) or \
               (qso['URQTH'] in US) or \
               (qso['URQTH'] in CANADA) or \
               (qso['URQTH'] in DX) ) ): 
          pass
       else:
          errorData.append(  ('QSO URQTH Parameter invalid: %s'%(qso['URQTH'])) )
          qsovalid = False
          
       return errorData

    
    def checkThisqso(self, qso, urqid):
        result = False
        qlist = self.db.read_pquery('SELECT * FROM QSOS WHERE ID=%s',
                                                [urqid])
        if (qlist):
            urqso=qlist[0]
            myqtime = self.qsotimeOBJ(qso['DATE'], qso['TIME'])
            myqsoband = self.getBand(qso['FREQ'])
            myurcall = self.stripCallsign(qso['URCALL'])
            urqtime = self.qsotimeOBJ(urqso['DATE'], urqso['TIME'])
            urqsoband = self.getBand(urqso['FREQ'])
            urqsomycall = self.stripCallsign(urqso['MYCALL'])
            mymode = self.modeSet(qso['MODE'])
            urmode = self.modeSet(urqso['MODE'])
            if (myqtime > urqtime):
                timediff = myqtime - urqtime
            else:
                timediff = urqtime - myqtime
            if ( timediff < timedelta(minutes=30) ):
                if ( myqsoband == urqsoband):
                    if (mymode == urmode):
                        if (qso['URQTH'] == urqso['MYQTH']):
                            if ( (qso['URREPORT'] == \
                                  urqso['MYREPORT']) or \
                                  (self.validate_Report_Mode(\
                                        urqso['MYREPORT'],
                                        urqso['MODE']) == False) ):
                                """ QSL match! """
                                result = 0
                        else:
                            """ qso QTH does not match"""
                            result = 4
                    else:
                        """ qso modes do not match """
                        result = 3
                else:
                    """ qso bands do not match """
                    result = 2        
            else:
                """qso time too far off"""
                result = 1
        return result

    def qslcheck(self, qso):
        result = False
        mylogid = qso['LOGID']
        mycall = self.stripCallsign(qso['MYCALL'])
        myband = self.getBand(qso['FREQ'])
        urcall = self.stripCallsign(qso['URCALL'])
        urlogid = self.db.CallinLogDB(urcall)
        urqsos = self.db.read_pquery(\
            'SELECT ID,URCALL FROM QSOS WHERE LOGID=%s',
                                                [urlogid])
        #print(urqsos)
        inTheirLog = False
        for urq in urqsos:
            #print(urq)
            if mycall in urq['URCALL']:
                if (mycall == self.stripCallsign(urq['URCALL'])):
                    inTheirLog = True
                    #print(mycall, urq)
                    qslmatch = self.checkThisqso(qso, urq['ID']) 
                    if (qslmatch != None):
                        #print('QSL result: %d\n%s\n%s\n'%(qslmatch, qso, urq['ID']))
                        if (qslmatch == 0):
                            result = True
                            break
        if (result):
            #print('QSL result: %d\n%s\n%s\n'%(qslmatch, qso, urq['ID']))
            qso['NOTE'] = ''
            query = 'UPDATE QSOS SET QSL=%s, VALID=1, ' +\
                        'NOLOG=0, NOQSOS=0, NOTE=%s WHERE ID=%s'
            params = [ urq['ID'], qso['NOTE'], qso['ID'] ]
        else:
            if (inTheirLog):
                qso['NOTE'] = 'No matching QSO in log for %s.'\
                                                        %(urcall)
                query =\
                     'UPDATE QSOS SET QSL=0, VALID=0, NOQSOS=1, '+\
                     'NOTE=%s WHERE ID=%s'
            else:
                qso['NOTE'] = 'No log received from %s.'\
                                                        %(urcall)
                query = \
                     'UPDATE QSOS SET QSL=0, VALID=1, NOLOG=1, '+\
                     'NOQSOS=0, NOTE=%s WHERE ID=%s'
            params = [ qso['NOTE'], qso['ID'] ]
        self.db.write_pquery(query, params)
        #print('writing %s, params %s'%(query, params))
        return result
        
    def checkqso(self, qid, logheader):
        result = False
        qso = None
        q = \
           self.db.read_pquery('SELECT * FROM QSOS WHERE ID=%s',
                                                     [qid['ID']])
        if (q): qso = q[0] 
        qsovalid = self.qso_valid(qso)
        #if ( (qsovalid != None) and (qsovalid < 8) ):
        if (qsovalid == []):
            """ DUPE Check is performed and saved when log is 
                loaded to the DB. Use the results."""
            if (qso['DUPE']):
                qso['NOTE'] = 'DUPE of qso %s'%(qso['DUPE'])
                self.db.write_pquery(\
                 'UPDATE QSOS SET QSL=0, VALID=0, NOLOG=0, '+\
                 'NOQSOS=0, NOTE=%s WHERE ID=%s',
                      [ qso['NOTE'], qso['ID'] ])
            else:
                    if self.compareCalls(logheader['CALLSIGN'],
                                               qso['MYCALL']):
                        qsl = self.qslcheck(qso)
                    else:
                        """ if compareCalls """
                        qso['NOTE'] = \
                         'MYCALL %s does not match '%(qso['MYCALL'])+\
                         'log header callsign %s'%(logheader['CALLSIGN'])
                        self.db.write_pquery(\
                         'UPDATE QSOS SET QSL=0, VALID=0, NOLOG=0, '+\
                         'NOQSOS=0, NOTE=%s WHERE ID=%s',
                                      [ qso['NOTE'], qso['ID'] ])
        else:
            qso['NOTE'] = self.packNote(qsovalid)
            self.db.write_pquery(\
                'UPDATE QSOS SET QSL=0, VALID=0, NOLOG=0, '+\
                'NOQSOS=0, NOLOG=0, NOTE=%s WHERE ID=%s',
                [ qso['NOTE'], qso['ID'] ])
                    
        return result

    def logqslCheck(self, call):
        mylogID = self.db.CallinLogDB(call)
        if (mylogID):
            myqsoids = self.db.read_pquery(\
             'SELECT ID, URCALL FROM QSOS WHERE LOGID=%s',
                                                   [mylogID])
            #print(myqsoids)
            if (myqsoids):
                header = self.db.fetchLogHeader(call)
                header=header[0]
                for qid in myqsoids:
                    #print('checking QSO %s'%(qid))
                    result = self.checkqso(qid, header)
            else: #if (myqsoids)         
                print('No QSOS for log %s in database.'%(call))
        else:
            print('Log from %s not in database.'%(call))
