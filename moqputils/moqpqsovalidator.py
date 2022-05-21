#!/usr/bin/env python3
"""
Update History:
* Tue May 12 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Separated this code from the MOQPDBUtils code.
- Enhancd QSL checks from 2019 QSO Party.
* Mon May 25 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Added call to self.modeSet method to set 
- all digimodes to RY and all phone modes to PH for QSL checking.
* Fri Aug 20 2021 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Fix for Addressing Issue #8, #24 & #25
- Consolidating qso_valid() method in MOQPQSOUtils and
- inhereting from it instead of the more generic QSOUtils.
- Added call to qthDXSet() to allow the mass number of logs
- that logged DX entities using their DX prefix instead of DX
* Fri May 20 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 - Fix for Addressing Issue #32
"""

from datetime import timedelta
from moqputils.moqpqsoutils import *
from moqputils.moqpdefs import *


class MOQPQSOValidator(MOQPQSOUtils):

    def __init__(self, db = None):
        self.db = db
    
    def checkThisqso(self, qso, urqid):
        #print(qso)
        result = False
        qlist = self.db.read_pquery('SELECT * FROM QSOS WHERE ID=%s',
                                                [urqid])
        if (qlist):
            urqso=qlist[0]
            myqtime = qso['DATETIME']
            myurqth = self.qthDXSet(qso['URQTH'])
            myqsoband = self.getBand(qso['FREQ'])
            myurcall = self.stripCallsign(qso['URCALL'])
            urqtime = urqso['DATETIME']
            urmyqth = self.qthDXSet(urqso['MYQTH'])
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
                        #if (qso['URQTH'] == urqso['MYQTH']):
                        if (myurqth == urmyqth):
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
            """SELECT ID,URCALL 
               FROM QSOS 
               WHERE LOGID=%s AND URCALL LIKE %s""",
                                    [urlogid, mycall])
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
                qso['NOTE'] = 'No matching QSO in %s log.'\
                                                        %(urcall)
                query =\
                     'UPDATE QSOS SET QSL=0, VALID=0, NOQSOS=1, '+\
                     'NOLOG=0, NOTE=%s WHERE ID=%s'
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
        qsoErrs, qsovalid = self.qso_valid(qso)
        #if ( (qsovalid != None) and (qsovalid < 8) ):
        if (qsovalid):
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
            qso['NOTE'] = self.packNote(qsoErrs)
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
