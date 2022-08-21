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
    def export_to_csv(self, dblist, award):
        tsvlines = commonAwards.export_to_csv(self, dblist, award)
        return tsvlines            

    def processLabel(self, sumitem, op=None):
        if op:
            op = ('-{}.pdf'.format(op))
        else:
            op = '.pdf'
            
        tsvdata = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS'],
                               sumitem['NAME'],
                               sumitem['ADDRESS'],
                               sumitem['CITY'],
                               sumitem['STATEPROV'],
                               sumitem['ZIPCODE'],
                               sumitem['COUNTRY'],                               
                               sumitem['EMAIL'],
                               sumitem['CALLSIGN']+op,
                               sumitem['S'],
                               sumitem['H'],
                               sumitem['O'],
                               sumitem['W'],
                               sumitem['M'],
                               sumitem['E'],
                               sumitem['WC']))
        return tsvdata


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
    def export_to_csv(self, dblist, award):
        tsvlines = commonAwards.export_to_csv(self, dblist, award)
        return tsvlines            

    def processLabel(self, sumitem, op=None):
        if op:
            op = ('-{}.pdf'.format(op))
        else:
            op = '.pdf'
            
        tsvdata = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS'],
                               sumitem['NAME'],
                               sumitem['ADDRESS'],
                               sumitem['CITY'],
                               sumitem['STATEPROV'],
                               sumitem['ZIPCODE'],
                               sumitem['COUNTRY'],                               
                               sumitem['EMAIL'],
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
           d.saveAndView('shomerpt.html')
        
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
           d.saveAndView('shomerpt.html')
        
