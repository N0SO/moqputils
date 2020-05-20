#!/usr/bin/env python3
"""
Update History:
* Tue May 12 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Separated this code from the MOQPDBUtils code.
- Enhancd QSL checks from 2019 QSO Party.
"""

from datetime import timedelta
from qsoutils import QSOUtils


class MOQPQSOValidator(QSOUtils):

    def __init__(self, db = None):
        self.db = db

    def qso_valid(self, qso):
       qsovalid = None
       valid_date_chars = set('0123456789/-')
       valid_call_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-')
       #qutils = QSOUtils()
       #if ( qso['FREQ'].isnumeric() ):
       if ( self.is_number(qso['FREQ']) ):
          if (self.getBand(qso['FREQ'])):
              if ( qso['MODE'] in self.MODES ):  
                  if all(char in valid_date_chars for char in qso['DATE']):
                      if ( qso['TIME'].isnumeric() ):
                          if (self.validateQSOtime(qso['DATE'], qso['TIME'])):
                              if all(char in valid_call_chars for char in qso['MYCALL']):
                                  if ( self.is_number(qso['MYREPORT']) ):
                                      if ( qso['MYQTH'].isalpha() ):
                                          if all(char in valid_call_chars for char in qso['URCALL']):
                                              if ( self.is_number(qso['URREPORT']) ):
                                                  if ( qso['URQTH'].isalpha() ):
                                                      #QSO looks valid
                                                      qsovalid = 0
                                                  else:
                                                      #Bad URQTH
                                                      qsovalid = 10
                                              else:
                                                  #Bad URREPORT
                                                  qsovalid = 9
                                          else:
                                              #Bad URCALL 
                                              qsovalid = 8
                                      else:
                                          #Bad MYQTH
                                          qsovalid = 7
                                  else:
                                      #Bad MYREPORT
                                      qsovalid = 6
                              else:
                                  #Bad MYCALL chars
                                  qsovalid = 5
                          else:
                              #QSO outside contest date/time boundaries
                              qsovalid = 4
                      else:
                          #Bad date/time chars
                          qsovalid = 3
                  else:
                      #Bad date/time chars
                      qsovalid = 3
              else:
                  #Bad Mode
                  qsovalid = 2 
          else:
              #Bad freq or band
              qsovalid = 1
       else:
          #Bad freq or band
          qsovalid = 1
       return qsovalid


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
            if (myqtime > urqtime):
                timediff = myqtime - urqtime
            else:
                timediff = urqtime - myqtime
            if ( timediff < timedelta(minutes=30) ):
                if ( myqsoband == urqsoband):
                    if (qso['MODE'] == urqso['MODE']):
                        if (qso['URQTH'] == urqso['MYQTH']):
                            if (qso['URREPORT'] == urqso['MYREPORT']):
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
                        #else:
                           #print('%s QSO %s fails match with %s QSO %s for %d'%(qso['CALL'], qso['ID'], urq['CALL'], urq['ID'], qslmatch))
        #print(result, inTheirLog)
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
                qso['NOTE'] = 'No log received for %s.'\
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
        if ( (qsovalid != None) and (qsovalid < 8) ):
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
            if (qsovalid == 1):
                qso['NOTE']='FREQ or BAND error: %s'%(qso['BAND'])
            elif (qsovalid == 2):
                qso['NOTE']='MODE error: %s'%(qso['MODE'])
            elif (qsovalid == 3):
                qso['NOTE']='DATE/TIME error: %s %S'%(qso['DATE'], qso['DATE'])
            elif (qsovalid == 4):
                qso['NOTE']='DATE/TIME outside contest boundaries: %s %S'%(qso['DATE'], qso['DATE'])
            elif (qsovalid == 5):
                qso['NOTE']='MYCALL error: %s'%(qso['MYCALL'])
            elif (qsovalid == 6):
                qso['NOTE']='MYREPORT error: %s'%(qso['MYREPORT'])
            elif (qsovalid == 7):
                qso['NOTE']='MYQTH error: %s'%(qso['MYQTH'])
            else:
                pass
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
