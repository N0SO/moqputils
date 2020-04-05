#!/usr/bin/python3
"""
moqplables - A collection of classes to help with the creation 
             and publishing of MOQP certificates and labels for 
             mailing.

Update History:
* Fri Feb 20 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

from moqpdbutils import *

VERSION = '0.0.1'

SHOWMEHEADERS =    'AWARD\tSTATION\tOPERATORS\t'+ \
                   'NAME\tADDRESS\tCITY\tSTATE\tZIP\t'+ \
                   'COUNTRY\tEMAIL'

CATCOLUMNHEADERS = 'PLACEMENT\t' + SHOWMEHEADERS

STATEHEADER = CATCOLUMNHEADERS+'\tSCORE'

class SHOWMELabels():
    def __init__(self, AWARD):
        #if __name__ == '__main__':
           self.AwardList =[]
           self.appMain(AWARD)

    def processOne(self, mydb, logid, AWARD):

        logheader = mydb.read_query("SELECT * from logheader WHERE ID=%s"%(logid))
        tsvdata = ("%s AWARD\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%( \
                               AWARD,
                               logheader[0]['CALLSIGN'],
                               logheader[0]['OPERATORS'],
                               logheader[0]['NAME'],
                               logheader[0]['ADDRESS'],
                               logheader[0]['CITY'],
                               logheader[0]['STATEPROV'],
                               logheader[0]['ZIPCODE'],
                               logheader[0]['COUNTRY'],                               
                               logheader[0]['EMAIL']))
        return tsvdata

    def showmeDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line)) 
    
    def appMain(self, AWARD):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       IDLIST = mydb.read_query("SELECT LOGID FROM %s WHERE QUALIFY = 1"%(AWARD))
       
       self.AwardList.append(SHOWMEHEADERS)
       for logID in IDLIST:
           #print(logID['LOGID'])
           self.AwardList.append( \
               self.processOne(mydb, logID['LOGID'],AWARD))
       self.showmeDisplay(self.AwardList)  
           
class CATEGORYLabels():
    def __init__(self):
        #if __name__ == '__main__':
           self.AwardList =[]
           self.appMain()
           
    def processHeader(self, mydb, place, cat, logid):
       logheader = mydb.read_query("SELECT * from logheader WHERE ID=%s"%(logid))
       tsvdata = ("%s\t%s AWARD\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%( \
                               place,cat,
                               logheader[0]['CALLSIGN'],
                               logheader[0]['OPERATORS'],
                               logheader[0]['NAME'],
                               logheader[0]['ADDRESS'],
                               logheader[0]['CITY'],
                               logheader[0]['STATEPROV'],
                               logheader[0]['ZIPCODE'],
                               logheader[0]['COUNTRY'],                               
                               logheader[0]['EMAIL']))
       return tsvdata
    
           
    def processOne(self, mydb, cat):
    
       sumlist = mydb.read_query("SELECT * FROM SUMMARY WHERE MOQPCAT='%s' ORDER BY (SCORE) DESC"%(cat))
       tsvdata = []
       tsvdata.append(self.processHeader(mydb, 
                                         "FIRST PLACE", 
                                         cat, 
                                         sumlist[0]['LOGID']) )
       if (len(sumlist) >1):
           tsvdata.append(self.processHeader(mydb, 
                                         "SECOND PLACE", 
                                         cat, 
                                         sumlist[1]['LOGID']) )
       return tsvdata
       
    def AwardDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line)) 

    def appMain(self):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       CATLIST = mydb.read_query("SELECT DISTINCT MOQPCAT FROM SUMMARY WHERE 1")
       self.AwardList.append(CATCOLUMNHEADERS)
       for CAT in CATLIST:
           #print(CAT['MOQPCAT'])
           tsvdata = self.processOne(mydb, CAT['MOQPCAT'])
           for line in tsvdata: 
               self.AwardList.append(line)
       self.AwardDisplay(self.AwardList) 

class STATELabels():
    def __init__(self):
        #if __name__ == '__main__':
           self.AwardList =[]
           self.appMain()

    def getOne(self, mydb, place, state, IDSTG, score):

        logheader = mydb.read_query("SELECT * FROM logheader "+ \
                                    "WHERE ID = "+ \
                                    ('%s'%(IDSTG)))


        tsvdata = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d"%( \
                               place,state,
                               logheader[0]['CALLSIGN'],
                               logheader[0]['OPERATORS'],
                               logheader[0]['NAME'],
                               logheader[0]['ADDRESS'],
                               logheader[0]['CITY'],
                               logheader[0]['STATEPROV'],
                               logheader[0]['ZIPCODE'],
                               logheader[0]['COUNTRY'],                               
                               logheader[0]['EMAIL'],
                               score))
        return tsvdata
       

    def getState(self,mydb, STATE, NAMELIST):
       CATLIST = mydb.read_query("SELECT ID "+ \
                                 "FROM logheader "+ \
                                 "WHERE LOCATION IN "+ \
                                 "(" + NAMELIST+ ")")
       if (len(CATLIST)>0):
           STRIDS =""
           for ID in CATLIST:
              STRIDS += ("'%s',"%(ID['ID']))
           STRIDS = STRIDS[:len(STRIDS)-1]
           #print(STRIDS)
           #print(CATLIST)
           SUMLIST = mydb.read_query('SELECT LOGID, SCORE '+ \
                                  'FROM SUMMARY '+ \
                                  'WHERE LOGID IN '+ \
                                  '(' + STRIDS +') '+ \
                                  'ORDER BY (SCORE) DESC')
           print(self.getOne(mydb, "FIRST PLACE",
                         STATE,
                         SUMLIST[0]['LOGID'],
                         SUMLIST[0]['SCORE']))
           if (len(SUMLIST) > 1):
               print(self.getOne(mydb, "SECOND PLACE",
                             STATE,
                             SUMLIST[1]['LOGID'],
                             SUMLIST[1]['SCORE']))
       else:
           print('\t%S\tNO ENTRY'%(STATE))

    def states(self, mydb):
       self.getState(mydb, "ALABAMA","'AL','ALABAMA'")
       self.getState(mydb, "ALASKA","'AK','ALASKA'")
       self.getState(mydb, "ARIZONA","'AZ','ARIZONA'")
       self.getState(mydb, "ARKANSAS","'AR','ARKANSAS'")

       self.getState(mydb, "PENN", "'PA','EPA','WPA'")


    def appMain(self):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       self.states(mydb)

