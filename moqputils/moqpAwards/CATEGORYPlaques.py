#!/usr/bin/python3
from  moqpdbutils import *
from  moqpdbconfig import *
from  moqpawardefs import *
from . commonAwards import commonAwards
           
class CATEGORYPlaques(commonAwards):
    
    def __init__(self, placement = '1'):
        self.AwardList=[]
        if (placement):
            self.appMain(placement)

    def get_awardquery(self, mydb, cati):
       sumlist = None
       cat = cati[0].upper()
       catlist = cati[1].upper()
       if cat in 'MISSOURI ROOKIE':
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
       elif cat in "MISSOURI SCHOOL CLUB":
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
              "WHERE LOGHEADER.NAME LIKE '%SCHOOL%' AND LOGHEADER.LOCATION='MO' "+\
              "ORDER BY (SCORE) DESC\n"+\
              "LIMIT 25")
           schoolclub = True
       elif cat in "MISSOURI CLUB":
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
              "WHERE CLUBS.LOGCOUNT > 2 AND LOGHEADER.LOCATION='MO' "+\
              "ORDER BY (SCORE) DESC\n"+\
              "LIMIT 10")
           schoolclub = True
       elif cat in 'HIGHEST DIGITAL':
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
       elif cat in 'HIGHEST NUMBER OF COUNTIES':
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
       else:
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
       return sumlist

    def processOne(self, mydb, cati, placement):
       tsvdata = None
       sumlist = None
       schoolclub = False
       if cati in PLAQUELIST:
           sumlist = self.get_awardquery(mydb, cati)

       if (sumlist):
           sumlist = sumlist[0]
       tsvdata = ''
       #if (len(sumlist)>0):
       tsvdata = self.processHeader(mydb, 
                                    "FIRST PLACE PLAQUE", 
                                    cati[0], 
                                    sumlist)

       #if ((sumlist ==None) or (len(sumlist) == 0)):
       #        tsvdata =['\t%s\tNO ENTRY'%(cati[0])]
       #print(tsvdata)
       return tsvdata

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       for CAT in PLAQUELIST:
           #print(CAT)
           tsvdata = self.processOne(mydb, CAT, placement)
           self.AwardList.append(tsvdata)
       self.AwardDisplay(self.AwardList) 
