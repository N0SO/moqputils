#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *
from moqputils.moqpAwards.commonAwards import commonAwards
           
class SHOWMEAwards(commonAwards):
    
    def __init__(self, showme):
        self.AwardList=[]
        if (showme):
            self.appMain(showme)

    def getdbData(self, db):
        dbData = db.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, SHOWME.*
              FROM LOGHEADER INNER JOIN SHOWME ON
              LOGHEADER.ID=SHOWME.LOGID
              WHERE QUALIFY > 0
              ORDER BY (CALLSIGN)""")
        #print(dbData)
        return dbData

    def export_to_csv(self, dblist, award):
        csvlist = []
        for rec in dblist:
            csvlist.append('%s\t%s\t%s'%(award,
                                         rec['CALLSIGN'],
                                         rec['OPERATORS']))
        return csvlist

    def appMain(self, showme):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       dblist = self.getdbData(mydb)
       csvlist = self.export_to_csv(dblist, 'SHOWME')
       self.AwardDisplay(csvlist) 

class SHOWMELabels(SHOWMEAwards):
  
    def getdbData(self, db):
        return db.read_query("""SELECT * FROM SHOWME_VIEW1
                                  WHERE  QUALIFY=1
                                  ORDER BY CALLSIGN;""")


    def addWC(self, st):
        """
        If the WILDCARD station is in the log.
            substitute WC the first blank letter
        """
        for s in('SHOWME'):
            if st['WC'] != None and st['WC'].strip() != '':
                if st[s] == None or st[s].strip() == '':
                    st[s]=st['WC']
                    break # Stop after WC station is applied.
        return st


    def processLabel(self, sumitem, op=None):
        if op:
            op = ('-{}.pdf'.format(op))
        else:
            op = '.pdf'
            
        sumitem = self.addWC(sumitem)
            
        tsvdata = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
                               sumitem['CALLSIGN'],
                               sumitem['ops'],
                               sumitem['name'],
                               sumitem['address'],
                               sumitem['city'],
                               sumitem['state'],
                               sumitem['zip'],
                               sumitem['country'],                               
                               sumitem['email'],
                               sumitem['CALLSIGN']+op,
                               sumitem['S'],
                               sumitem['H'],
                               sumitem['O'],
                               sumitem['W'],
                               sumitem['M'],
                               sumitem['E'],
                               sumitem['WC']))
        return tsvdata

    def export_to_csv(self, dblist, award):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('/home/pi/Projects/moqputils/moqputils/configs/qrzsettings.cfg')
        if award=='SHOWME':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'S\tH\tO\tW\tM\tE\tWC']
        elif award=='MISSOURI':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'M\tI\tS\tS\tO\tU\tR\tI\tWC']
            
        for station in dblist:
            if len(station['ops']) > 0:
                ops = station['ops'].split(' ')
                if len(ops) > 1: #Multi-op station
                    tempData = station
                    for op in ops:
                        try:
                            opdata = qrz.callsign(op.strip())
                            qrzdata=True
                        except:
                            qrzdata=False
                            tempData['name']=\
                               'NO QRZ FOR {} - {}'.format(op,len(op))
                       
                        if qrzdata:
                            #print(opdata)
                            tempData = self.swapData(\
                                   station, 
                                   op, 
                                   opdata)
                        tsvlines.append(self.processLabel(tempData, op))
                    
                else: #Single-op station
                    if station['CALLSIGN'] == station['ops']:
                        station['ops'] = ''
                    tsvlines.append(self.processLabel(station))
        return tsvlines            


class MOAwards(SHOWMEAwards):
    
    def getdbData(self, db):
       dbData = db.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, MISSOURI.*
              FROM LOGHEADER INNER JOIN MISSOURI ON
              LOGHEADER.ID=MISSOURI.LOGID
              WHERE QUALIFY > 0
              ORDER BY (CALLSIGN)""")
       return dbData


    def appMain(self, showme):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       dblist = self.getdbData(mydb)
       csvlist = self.export_to_csv(dblist, 'MISSOURI')
       self.AwardDisplay(csvlist) 

class MOLabels(MOAwards):
    def getdbData(self, db):
        return db.read_query("""SELECT * FROM MISSOURI_VIEW
                                  WHERE  QUALIFY=1
                                  ORDER BY CALLSIGN;""")

    def addWC(self, st):
        """
        If the WILDCARD station is in the log.
            substitute WC the first blank letter
        """
        for s in('M','I_1','S_1','S_2','O','U','R','I_2'):
            if st['WC'] != None and st['WC'].strip() != '':
                if st[s] == None or st[s].strip() == '':
                    st[s]=st['WC']
                    break # Stop after WC station is applied.
        return st

    def export_to_csv(self, dblist, award):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('/home/pi/Projects/moqputils/moqputils/configs/qrzsettings.cfg')
        if award=='SHOWME':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'S\tH\tO\tW\tM\tE\tWC']
        elif award=='MISSOURI':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'M\tI\tS\tS\tO\tU\tR\tI\tWC']
            
        for station in dblist:
            if len(station['ops']) > 0:
                ops = station['ops'].split(' ')
                if len(ops) > 1: #Multi-op station
                    tempData = station
                    for op in ops:
                        try:
                            opdata = qrz.callsign(op.strip())
                            qrzdata=True
                        except:
                            qrzdata=False
                            tempData['name']=\
                               'NO QRZ FOR {} - {}'.format(op,len(op))
                       
                        if qrzdata:
                            #print(opdata)
                            tempData = self.swapData(\
                                   station, 
                                   op, 
                                   opdata)
                        tsvlines.append(self.processLabel(tempData, op))
                    
                else: #Single-op station
                    if station['CALLSIGN'] == station['ops']:
                        station['ops'] = ''
                    tsvlines.append(self.processLabel(station))
        return tsvlines            

    def processLabel(self, sumitem, op=None):
        if op:
            op = ('-{}.pdf'.format(op))
        else:
            op = '.pdf'
            
        sumitem = self.addWC(sumitem)
        
        tsvdata = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
                               sumitem['CALLSIGN'],
                               sumitem['ops'],
                               sumitem['name'],
                               sumitem['address'],
                               sumitem['city'],
                               sumitem['state'],
                               sumitem['zip'],
                               sumitem['country'],                               
                               sumitem['email'],
                               sumitem['CALLSIGN']+op,
                               sumitem['M'],
                               sumitem['I_1'],
                               sumitem['S_1'],
                               sumitem['S_2'],
                               sumitem['O'],
                               sumitem['U'],
                               sumitem['R'],
                               sumitem['I_2'],
                               sumitem['WC']))
        return tsvdata




LABELS1 = ['STATION',
           'OPERATORS']

KEYS1 = ['CALLSIGN',
         'OPERATORS']

class HTMLShowMeAwards(SHOWMEAwards):
    def appMain(self, showme):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       showmeList = self.getdbData(mydb)
       if (showmeList):
           #theader = self.buildDictHeader(KEYS1, LABELS1)
           #showmeList= self.addHeader(theader, showmeList)

           from htmlutils.htmldoc import htmlDoc   
           d = htmlDoc()
           d.openHead('{} Missouri QSO Party Showme Awards'.format(YEAR),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party SHOWME Awards</h2>""".format(YEAR))
           d.addTablefromDict(dictList=showmeList, 
                          HeaderList=LABELS1,
                          caption='Download your certificate with the e-mail link provided',
                          dictIndexList=KEYS1)
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           #d.saveAndView('shomerpt.html')
        
class HTMLMoAwards(MOAwards):
    def appMain(self, showme):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       showmeList = self.getdbData(mydb)
       if (showmeList):
           #theader = self.buildDictHeader(KEYS1, LABELS1)
           #showmeList= self.addHeader(theader, showmeList)

           from htmlutils.htmldoc import htmlDoc   
           d = htmlDoc()
           d.openHead('{} Missouri QSO Party Missouri Awards'.format(YEAR),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party MISSOURI Awards</h2>""".format(YEAR))
           d.addTablefromDict(dictList=showmeList, 
                          HeaderList=LABELS1,
                          caption='Download your certificate with the e-mail link provided',
                          dictIndexList=KEYS1)
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           #d.saveAndView('shomerpt.html')
        
