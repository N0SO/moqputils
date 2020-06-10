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
from moqpdbconfig import *
from moqpawardefs import *

class STATEAwards():
    #from moqpawardefs import STATELIST

    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def getOne(self, mydb, place, state, sdata):

        tsvdata = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d"%( \
                               place,state,
                               sdata['CALLSIGN'],
                               sdata['OPERATORS'],
                               sdata['NAME'],
                               sdata['ADDRESS'],
                               sdata['CITY'],
                               sdata['STATEPROV'],
                               sdata['ZIPCODE'],
                               sdata['COUNTRY'],                               
                               sdata['EMAIL'],
                               sdata['SCORE']))
        return tsvdata
       
    def ShowAward(self, mydb, place, state, sdata):

        tsvdata = ("%s\t%s\t%s\t%s\t%d"%( \
                               place,state,
                               sdata['CALLSIGN'],
                               sdata['OPERATORS'],
                               sdata['SCORE']))
        return tsvdata


    def getState(self,mydb, STATE, NAMELIST):
       CATLIST = mydb.read_query(\
                "SELECT LOGHEADER.*, "+\
                "SUMMARY.* "+ \
                "FROM LOGHEADER INNER JOIN SUMMARY ON "+\
                "LOGHEADER.ID=SUMMARY.LOGID "+\
                "WHERE LOGHEADER.LOCATION IN "+\
                "(" + NAMELIST+ ") " +\
                "ORDER BY SCORE DESC")
       if (len(CATLIST)>0):
           print(self.ShowAward(mydb, "FIRST PLACE",
                         STATE,
                         CATLIST[0]))
           if (len(CATLIST) > 1):
               print(self.ShowAward(mydb, "SECOND PLACE",
                             STATE,
                             CATLIST[1]))
       else:
           print('\t%s\tNO ENTRY'%(STATE))

    def states(self, mydb, call):
       #print('%s'%(STATEHEADER))
       for state in STATELIST:
           self.getState(mydb, state[0], state[1])

    def appMain(self, call):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       self.states(mydb, call)

class STATELabels(STATEAwards):

    def ShowAward(self, mydb, place, state, sdata):

        tsvdata = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d"%( \
                               place,state,
                               sdata['CALLSIGN'],
                               sdata['OPERATORS'],
                               sdata['NAME'],
                               sdata['ADDRESS'],
                               sdata['CITY'],
                               sdata['STATEPROV'],
                               sdata['ZIPCODE'],
                               sdata['COUNTRY'],                               
                               sdata['EMAIL'],
                               sdata['SCORE']))
        return tsvdata
       
class CATEGORYAwards():
           
    #from moqpawardefs import AWARDLIST

    def __init__(self, callsign = None):
        self.AwardList=[]
        if (callsign):
            self.appMain(callsign)

    def processHeader(self, mydb, place, cat, sumitem):
       tsvdata = ("%s\t%s AWARD\t%s\t%s"%( \
                               place,cat,
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS']))
       return tsvdata
    
           
    def processOne(self, mydb, cati, placement):
       tsvdata = None
       #print('Placement=%s'%(placement))
    
       cat = cati.upper()
       #print(cat)
       sumlist = mydb.read_pquery(\
       "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
       "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
       "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
       "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
       "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
       "LOGHEADER.EMAIL, SUMMARY.* "+\
       "FROM LOGHEADER INNER JOIN SUMMARY ON "+\
       "LOGHEADER.ID=SUMMARY.LOGID "+\
       "WHERE SUMMARY.MOQPCAT=%s "+\
       "ORDER BY (SCORE) DESC",[cat])
       if (sumlist):
           #sumlist = sumlist[0]
           tsvdata = []
           #print(cat, sumlist)
           if (placement == '1'):
               if (len(sumlist)>0):
                   tsvdata.append(self.processHeader(mydb, 
                                            "FIRST PLACE", 
                                            cat, 
                                            sumlist[0]) )
           if (placement == '2'):
               if (len(sumlist) >1):
                   tsvdata.append(self.processHeader(mydb, 
                                          "SECOND PLACE", 
                                           cat, 
                                           sumlist[1]) )
         
       if ((sumlist ==None) or (len(sumlist) == 0)):
               tsvdata =['\t%s\tNO ENTRY'%(cat)]
       #print(tsvdata)
       return tsvdata
       
    def AwardDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line)) 

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       for CAT in AWARDLIST:
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       self.AwardDisplay(self.AwardList) 

class CATEGORYLabels(CATEGORYAwards):

    def processHeader(self, mydb, place, cat, sumitem):
       tsvdata = ("%s\t%s AWARD\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%( \
                               place,cat,
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS'],
                               sumitem['NAME'],
                               sumitem['ADDRESS'],
                               sumitem['CITY'],
                               sumitem['STATEPROV'],
                               sumitem['ZIPCODE'],
                               sumitem['COUNTRY'],                               
                               sumitem['EMAIL']))
       return tsvdata
    
class CATEGORYPlaques(CATEGORYAwards):
    
    def __init__(self, placement = '1'):
        self.AwardList=[]
        if (placement):
            self.appMain(placement)

    def processClub(self, mydb, place, cat, sumitem):
       tsvdata = ("%s\t%s AWARD\t%s\t%s"%( \
                               place,cat,
                               sumitem['NAME'],
                               " "))
       return tsvdata
    
    def processOne(self, mydb, cati, placement):
       tsvdata = None
       sumlist = None
       cat = cati[0].upper()
       catlist = cati[1].upper()
       schoolclub = False
       if cati in PLAQUELIST:
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, SUMMARY.* "+\
              "FROM LOGHEADER INNER JOIN SUMMARY ON "+\
              "LOGHEADER.ID=SUMMARY.LOGID "+\
              "WHERE SUMMARY.MOQPCAT IN ("+ catlist +") "+\
              "ORDER BY (SCORE) DESC")
       elif cati in ROOKIELIST:
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, SUMMARY.* "+\
              "FROM LOGHEADER INNER JOIN SUMMARY ON "+\
              "LOGHEADER.ID=SUMMARY.LOGID "+\
              "WHERE ROOKIE > 0 "+\
              "ORDER BY (SCORE) DESC")
       elif cati in SCHOOLLIST:
           sumlist = mydb.read_query(\
              "SELECT CLUBS.*, CLUB_MEMBERS.*, "+\
              "LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL \n"+\
              "FROM CLUBS INNER JOIN CLUB_MEMBERS ON "+\
              "CLUBS.CLUBID=CLUB_MEMBERS.CLUBID "+\
              "INNER JOIN LOGHEADER ON "+\
              "CLUB_MEMBERS.LOGID=LOGHEADER.ID \n"+\
              "WHERE LOGCOUNT>2 "+\
              "ORDER BY (SCORE) DESC\n"+\
              "LIMIT 25")
           schoolclub = True
       elif cati in DIGITALLIST:
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, DIGITAL.* "+\
              "FROM LOGHEADER INNER JOIN DIGITAL ON "+\
              "LOGHEADER.ID=DIGITAL.LOGID "+\
              "WHERE QSOS > 49 "+\
              "ORDER BY (SCORE) DESC")
       elif cati in CNTYLIST:
           sumlist = mydb.read_query(\
            """SELECT LOGHEADER.CALLSIGN,
               LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
               LOGHEADER.NAME, LOGHEADER.ADDRESS, 
               LOGHEADER.CITY, LOGHEADER.STATEPROV,
               LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
               LOGHEADER.EMAIL, COUNTY.COUNT, COUNTY.NAMES
               FROM LOGHEADER INNER JOIN COUNTY ON 
               LOGHEADER.ID=COUNTY.LOGID 
               ORDER BY (COUNT) DESC
               LIMIT 10""")
       #print(cat)
       #print(catlist)
       """
       for rec in sumlist:
           print(rec)
       """
       if (sumlist):
           #sumlist = sumlist[0]
           tsvdata = []
           if (len(sumlist)>0):
               if (schoolclub):
                   tsvdata.append(self.processClub(mydb, 
                                            "FIRST PLACE PLAQUE", 
                                            cat, 
                                            sumlist[0]) )
               else:
                   tsvdata.append(self.processHeader(mydb, 
                                            "FIRST PLACE PLAQUE", 
                                            cat, 
                                            sumlist[0]) )

       if ((sumlist ==None) or (len(sumlist) == 0)):
               tsvdata =['\t%s\tNO ENTRY'%(cat)]
       #print(tsvdata)
       return tsvdata

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       for CAT in PLAQUELIST:
           #print(CAT)
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       for CAT in ROOKIELIST:
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       for CAT in SCHOOLLIST:
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       for CAT in DIGITALLIST:
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       for CAT in CNTYLIST:
           tsvdata = self.processOne(mydb, CAT, placement)
           for line in tsvdata: 
               self.AwardList.append(line)
       self.AwardDisplay(self.AwardList) 

