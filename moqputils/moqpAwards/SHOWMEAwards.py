#!/usr/bin/python3
from moqpdbutils import *
from moqpdbconfig import *
from moqpawardefs import *
from . commonAwards import commonAwards
           
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
              LOGHEADER.EMAIL, SHOWME.QUALIFY
              FROM LOGHEADER INNER JOIN SHOWME ON
              LOGHEADER.ID=SHOWME.LOGID
              WHERE QUALIFY > 0
              ORDER BY (CALLSIGN)""")
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

class MOAwards(SHOWMEAwards):
    
    def getdbData(self, db):
       dbData = db.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, MISSOURI.QUALIFY
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
