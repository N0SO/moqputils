#!/usr/bin/env python3

from moqputils.moqpcertificates import MOQPCertificates
from moqputils.moqpdbutils import MOQPDBUtils
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpmults import MOQPMults
from moqputils.bothawards import BothAwards


class MOQPDBCertificates(MOQPCertificates):

    def __init__(self, call = None):
        if (call):
            self.appMain(call.upper())

    def writeSHOWME(self, db, logID, smresult):
        showmeID = None
        #Does a record for this log exist already?
        #logID = self.CallinLogDB(log['HEADER']['CALLSIGN'])
        IDL = db.read_pquery(\
            "SELECT ID FROM SHOWME WHERE LOGID=%s",
            [logID])
        #print(IDL)
        if (IDL):
            showmeID = IDL[0]['ID']
            #print('code to update row %s goes here'%(showmeID))
            query="UPDATE `SHOWME` SET `LOGID`=%s, "+\
                  "`S`=%s,`H`=%s,`O`=%s,`W`=%s,`M`=%s,`E`=%s, "+\
                  "`WC`=%s,`QUALIFY`=%s WHERE ID=%s"

            params = [logID,
                      smresult['CALLS']['S'],
                      smresult['CALLS']['H'],
                      smresult['CALLS']['O'],
                      smresult['CALLS']['W'],
                      smresult['CALLS']['M'],
                      smresult['CALLS']['E'],
                      smresult['WILDCARD'],
                      smresult['QUALIFY'],
                      showmeID]
            #print (query, params)
            showmeID = db.write_pquery(query, params)
            #exit()
        else:
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

            showmeID = db.write_query(query)
        return showmeID

    def writeMO(self, db, logID, smresult):
        moID = None
        #Does a record for this log exist already?
        #logID = self.CallinLogDB(log['HEADER']['CALLSIGN'])
        IDL = db.read_pquery(\
            "SELECT ID FROM MISSOURI WHERE LOGID=%s",
            [logID])
        #print('IDL=%s'%(IDL))
        if (IDL):
            moID = IDL[0]['ID']
            #print('code to update row %s goes here'%(moID))

            query = 'UPDATE MISSOURI SET LOGID=%s, '+\
                    'M=%s, I_1=%s, S_1=%s, S_2=%s, O=%s, '+\
                    'U=%s, R=%s, I_2=%s, WC=%s, QUALIFY=%s '+\
                    'WHERE ID=%s'
            params = (logID,
                      smresult['CALLS']['M'],
                      smresult['CALLS']['I0'],
                      smresult['CALLS']['S0'],
                      smresult['CALLS']['S1'],
                      smresult['CALLS']['O'],
                      smresult['CALLS']['U'],
                      smresult['CALLS']['R'],
                      smresult['CALLS']['I1'],
                      smresult['WILDCARD'],
                      smresult['QUALIFY'],
                      moID)
            moID = db.write_pquery(query, params)
        else:
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

            moID = db.write_query(query)
        return moID

    def processLogdict(self, callsign):
       """
       Read the Cabrillo log file and separate log header data
       from qso data. 
       Returns a dictionary with four elements:
          HEADER = a dictionary objject of the log header
          QSOLIST = a list dictionary objects with QSO data
          ERRORS = A list of errors encountered while 
                   processing the log.
          QSOSUM = a summary of the QSO statstics
                   QSOS = total number of QSOs
                   CW = number of CW QSOs
                   PH = number of PHONE QSOSs
                   DG = number of DIGITAL QSOs
                   VHF = number of VHF (>=144MHz) QSOs
       """
       logSummary = None
       log = self.getLogFile(callsign)
       if ( log ):
          qsosummary = self.processQSOList(log['QSOLIST'])
          logSummary = dict()
          logSummary['HEADER'] = log['HEADER']
          logSummary['QSOLIST'] = log['QSOLIST']
          logSummary['ERRORS'] = log['ERRORS']
          logSummary['QSOSUM'] = qsosummary
          logSummary['MULTS'] = log['MULTS']
          
       return logSummary

    def getLogFile(self, callsign):
        log = None
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()
        mults = MOQPMults()
        #Fetch log header
        header = mydb.fetchCABHeader(callsign)
        #print(header)
        qsos = mydb.fetchValidQSOS(callsign)

        for qso in qsos:
            mults.setMult(qso['URQTH'])
        #print('mults = %d'%(mults.sumMults()))
        log = dict()
        log['HEADER'] = header
        log['QSOLIST'] = qsos
        log['MULTS'] = mults.sumMults()
        log['ERRORS'] = []
        return log
 
    def parseLog(self, callsign, Headers=True):
       """
       This method processes a single file passed in filename
       If the Headers option is false, it will skip printing the
       csv header info.
    
       Using dictionary objects
       """
       fullSummary = None
       logsummary = self.processLogdict(callsign)
       #print('parseLog: parsing errors: \n%s'%(logsummary['ERRORS'] ))
       #print(logsummary['QSOSUM'])
       if (logsummary):
          moqpcat = self.determineMOQPCatdict(logsummary)
          #print(moqpcat)
          #Score = self.calculate_score(logsummary['QSOSUM'],
          #                             logsummary['MULTS'])
          Score = 0
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MULTS'] = logsummary['MULTS']
          fullSummary['SCORE'] = Score
          fullSummary['MOQPCAT'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          fullSummary['ERRORS'] = logsummary['ERRORS']
       else:
          print('No log in database for call %s.'%(filename))
       return fullSummary

    def scoreLog(self, call, HEADER=False):
        #print(call)
        tsvdata=None
        log = self.parseLog(call)
        #print('log=%s'%(log))
        if log:
            tsvdata = ''
            if (log['ERRORS'] == []):
                bawards = BothAwards()
                result = (bawards.appMain(\
                           log['HEADER']['CALLSIGN'],
                           log['QSOLIST']))
                #print(result)
                if (HEADER):
                   tsvdata += 'STATION\tSHOWME AWARD\tS\tH\t O\tW\tM\tE\tWC\t' \
                      'MISSOURI AWARD\tM\tI\tS\tS\t O\tU\tR\tI\tWC\t' \
                      'W0MA BONUS\tK0GQ BONUS'
                tsvdata += ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s' \
                        %(log['HEADER']['CALLSIGN'],
                          result['SHOWME']['QUALIFY'],
                          result['SHOWME']['CALLS']['S'],
                          result['SHOWME']['CALLS']['H'],
                          result['SHOWME']['CALLS']['O'],
                          result['SHOWME']['CALLS']['W'],
                          result['SHOWME']['CALLS']['M'],
                          result['SHOWME']['CALLS']['E'],
                          result['SHOWME']['WILDCARD'],
                          result['MO']['QUALIFY'],
                          result['MO']['CALLS']['M'],
                          result['MO']['CALLS']['I0'],
                          result['MO']['CALLS']['S0'],
                          result['MO']['CALLS']['S1'],
                          result['MO']['CALLS']['O'],
                          result['MO']['CALLS']['U'],
                          result['MO']['CALLS']['R'],
                          result['MO']['CALLS']['I1'],
                          result['MO']['WILDCARD'],
                          result['BONUS']['W0MA'],
                          result['BONUS']['K0GQ']))
                          
                mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
                mydb.setCursorDict()
                logID = mydb.CallinLogDB(log['HEADER']['CALLSIGN'])
                smID = self.writeSHOWME(mydb, 
                                        logID, 
                                        result['SHOWME'])          
                moID = self.writeMO(mydb, 
                                    logID, 
                                    result['MO'])          
            else:
                print('log file %s has errors' \
                %(pathname))
        else:
            print(\
            'File %s does not exist or is not in CABRILLO Format'\
                %(pathname))
        return tsvdata

    def appMain(self, call):
       csvdata = 'Nothing.'
       query = 'SELECT ID, CALLSIGN FROM LOGHEADER WHERE '
       if (call == 'ALLCALLS'):
           query += '1;'
       else:
           query += 'CALLSIGN = "%s";'%(call)
           
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       loglist = mydb.read_query(query)
       if (loglist):
           HEADER = True
           for nextlog in loglist:
               #print('callsign = %s'%(nextlog['CALLSIGN']))
               csvdata = self.scoreLog(nextlog['CALLSIGN'], HEADER)
               HEADER=False     
               print(csvdata)
       else:
           print('No %s found in database.'%(call))

LABELS1 = ['STATION',
           'OPERATORS',
           'QUALIFY',
           'S',
           'H',
           'O',
           'W',
           'M',
           'E',
           'WILDCARD']

KEYS1 = ['CALLSIGN',
         'OPERATORS',
         'QUALIFY',
         'S',
         'H',
         'O',
         'W',
         'M',
         'E',
         'WC']
         

"""Generate SHOWME and MISSOURI reports from the
   SHOME and MISSOURI database results table"""
class SHOWMEReport():
    def __init__(self, call = None):
        if (call):
            self.appMain(call)
            
    def fetchShowMe(self, callsign):
       db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       db.setCursorDict()
       query = """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              SHOWME.*
              FROM LOGHEADER INNER JOIN SHOWME ON
              LOGHEADER.ID=SHOWME.LOGID """
       if ('SHOWME' in callsign):      
            query+= 'ORDER BY QUALIFY DESC, CALLSIGN;'
       else:
            query+= 'WHERE CALLSIGN = "%s";'%(callsign)
       #print (query)
       dbData = db.read_query(query)
       return dbData

    def buildDictHeader(self, hkeys, hdata):
       header = dict()
       i=0
       for key in hkeys:
           header[key] = hdata[i]
           i+=1
       return header

    def addHeader(self, header, dictdata): 
       retData = [header]
       for ent in dictdata:
          retData.append(ent)
       return retData
       
    def exportCSV(self, dictkeys, dictdata):
       csvdata = ''
       #print(dictkeys)
       #print(dictdata)
       for ent in dictdata:
          for entkey in dictkeys:
             csvdata += '%s\t'%(ent[entkey])
          csvdata+='\n'
       return csvdata

    def appMain(self, call):
       call = call.upper()
       showmeList = self.fetchShowMe(call)
       theader = self.buildDictHeader(KEYS1, LABELS1)
       showmeList= self.addHeader(theader, showmeList)
       #print(showmeList)
       print(self.exportCSV(KEYS1, showmeList))

class HTMLShowMe(SHOWMEReport):
    def appMain(self, call):
       call = call.upper()
       #print (call)
       showmeList = self.fetchShowMe(call)
       #print(showmeList)
       if (showmeList):
           #theader = self.buildDictHeader(KEYS1, LABELS1)
           #showmeList= self.addHeader(theader, showmeList)

           from htmlutils.htmldoc import htmlDoc   
           d = htmlDoc()
           d.openHead('{} Missouri QSO Party Showme Report'.format(YEAR),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party SHOWME Report</h2>""".format(YEAR))
           d.addTablefromDict(dictList=showmeList, 
                          HeaderList=LABELS1,
                          caption='SHOWME Status By Call',
                          dictIndexList=KEYS1)
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           d.saveAndView('shomerpt.html')

KEYS2 = ('CALLSIGN',
           'OPERATORS',
           'QUALIFY',
           'M',
           'I_1',
           'S_1',
           'S_2',
           'O',
           'U',
           'R',
           'I_2',
           'WC')

LABELS2 = ('STATION',
         'OPERATORS',
         'QUALIFY',
         'M',
         'I',
         'S',
         'S',
         'O',
         'U',
         'R',
         'I',
         'WILDCARD')
         

"""Generate SHOWME and MISSOURI reports from the
   SHOME and MISSOURI database results table"""
class MISSOURIReport(SHOWMEReport):
            
    def fetchMO(self, callsign):
       db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       db.setCursorDict()
       query = """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              MISSOURI.*
              FROM LOGHEADER INNER JOIN MISSOURI ON
              LOGHEADER.ID=MISSOURI.LOGID """
       if ('MISSOURI' in callsign):      
            query+= 'ORDER BY QUALIFY DESC, CALLSIGN;'
       else:
            query+= 'WHERE CALLSIGN = "%s";'%(callsign)
       #print (query)
       dbData = db.read_query(query)
       return dbData

    def appMain(self, call):
       call = call.upper()
       showmeList = self.fetchMO(call)
       theader = self.buildDictHeader(KEYS2, LABELS2)
       showmeList= self.addHeader(theader, showmeList)
       #print(showmeList)
       print(self.exportCSV(KEYS2, showmeList))

class HTMLMORpt(MISSOURIReport):
    def appMain(self, call):
       call = call.upper()
       #print (call)
       showmeList = self.fetchMO(call)
       #print(showmeList)
       if (showmeList):
           #theader = self.buildDictHeader(KEYS1, LABELS1)
           #showmeList= self.addHeader(theader, showmeList)

           from htmlutils.htmldoc import htmlDoc   
           d = htmlDoc()
           d.openHead('{} Missouri QSO Party MISSOURI Report'.format(YEAR),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party MISSOURI Report</h2>""".format(YEAR))
           d.addTablefromDict(dictList=showmeList, 
                          HeaderList=LABELS2,
                          caption='MISSOURI Status By Call',
                          dictIndexList=KEYS2)
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           d.saveAndView('missourirpt.html')




