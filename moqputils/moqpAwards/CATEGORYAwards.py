#!/usr/bin/python3
from moqpdbutils import *
from moqpdbconfig import *
from moqpawardefs import *
from . commonAwards import commonAwards
       
class CATEGORYAwards(commonAwards):
           
    def __init__(self, callsign = None):
        self.AwardList=[]
        if (callsign):
            self.appMain(callsign)

    def get_awardquery(self, mydb, cat):
       sumlist = None
       if cat in 'MISSOURI ROOKIE':
           #print("ROOKIE - %s"%(cat))
           sumlist = mydb.read_query(\
            """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
               LOGHEADER.NAME, LOGHEADER.ADDRESS,
               LOGHEADER.CITY, LOGHEADER.STATEPROV ,
               LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
               LOGHEADER.EMAIL, SUMMARY.*
               FROM LOGHEADER INNER JOIN SUMMARY ON
               LOGHEADER.ID=SUMMARY.LOGID
               WHERE ROOKIE > 0
               ORDER BY (SCORE) DESC
               LIMIT 25""")
       elif cat in 'MISSOURI SCHOOL CLUB':
           sumlist = mydb.read_query(\
              """SELECT CLUBS.*, CLUB_MEMBERS.*,
                 LOGHEADER.CALLSIGN,
                 LOGHEADER.OPERATORS, LOGHEADER.LOCATION,
                 LOGHEADER.NAME, LOGHEADER.ADDRESS,
                 LOGHEADER.CITY, LOGHEADER.STATEPROV,
                 LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
                 LOGHEADER.EMAIL
                 FROM CLUBS INNER JOIN CLUB_MEMBERS ON
                 CLUBS.CLUBID=CLUB_MEMBERS.CLUBID
                 INNER JOIN LOGHEADER ON
                 CLUB_MEMBERS.LOGID=LOGHEADER.ID
                 WHERE LOGHEADER.NAME LIKE '%SCHOOL%' AND LOGHEADER.LOCATION='MO'
                 ORDER BY (SCORE) DESC
                 LIMIT 10""")
       elif cat in 'MISSOURI CLUB':
           sumlist = mydb.read_query(\
              """SELECT CLUBS.*, CLUB_MEMBERS.*,
              LOGHEADER.CALLSIGN,
              LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL
              FROM CLUBS INNER JOIN CLUB_MEMBERS ON
              CLUBS.CLUBID=CLUB_MEMBERS.CLUBID
              INNER JOIN LOGHEADER ON
              CLUB_MEMBERS.LOGID=LOGHEADER.ID
              WHERE LOGCOUNT>2 AND LOGHEADER.LOCATION='MO'
              ORDER BY (SCORE) DESC
              LIMIT 10""")
       elif cat in 'MISSOURI HIGHEST DIGITAL':
           sumlist = mydb.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, DIGITAL.*
              FROM LOGHEADER INNER JOIN DIGITAL ON
              LOGHEADER.ID=DIGITAL.LOGID
              WHERE LOGHEADER.LOCATION='MO'
              ORDER BY (SCORE) DESC
              LIMIT 5""")
       elif cat in 'NON-MISSOURI HIGHEST DIGITAL':
           sumlist = mydb.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, DIGITAL.*
              FROM LOGHEADER INNER JOIN DIGITAL ON
              LOGHEADER.ID=DIGITAL.LOGID
              WHERE LOGHEADER.LOCATION!='MO'
              ORDER BY (SCORE) DESC
              LIMIT 5""")
       elif cat in 'MISSOURI VHF':
           sumlist = mydb.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, VHF.SCORE
              FROM LOGHEADER INNER JOIN VHF ON
              LOGHEADER.ID=VHF.LOGID
              WHERE LOGHEADER.LOCATION='MO'
              ORDER BY (SCORE) DESC
              LIMIT 5""")
       elif cat in 'NON-MISSOURI VHF':
           sumlist = mydb.read_query(\
             """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, VHF.SCORE
              FROM LOGHEADER INNER JOIN VHF ON
              LOGHEADER.ID=VHF.LOGID
              WHERE LOGHEADER.LOCATION!='MO'
              ORDER BY (SCORE) DESC""")
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
               LIMIT 5""")
       else:
           sumlist = mydb.read_pquery(\
            """SELECT LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS,
               LOGHEADER.NAME, LOGHEADER.ADDRESS,
               LOGHEADER.CITY, LOGHEADER.STATEPROV,
               LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
               LOGHEADER.EMAIL, SUMMARY.*
               FROM LOGHEADER INNER JOIN SUMMARY ON
               LOGHEADER.ID=SUMMARY.LOGID
               WHERE SUMMARY.MOQPCAT=%s
               ORDER BY (SCORE) DESC
               LIMIT 5""",[cat])
       return sumlist

    def processOne(self, mydb, cati, placement):
       tsvdata = None
       sumlist = None
       #print('Placement=%s'%(placement))
       if (isinstance(cati, list)):
           cat = cati[0].upper()
           catlist = cati[1].upper()
       else:
           cat = cati.upper()
           catlist = cat
       #print(cat, catlist)
       sumlist = self.get_awardquery(mydb, catlist)
       placestg, catdata = self.setPlacement(placement, sumlist)
       #print(catdata)
       tsvdata = self.processHeader(mydb, 
                                    placestg, 
                                    cat, 
                                    catdata )
       #print(tsvdata)
       return tsvdata

    def processAll(self, mydb, placement):
        tsvdata = []
        for CAT in AWARDLIST:          
           tsvline = self.processOne(mydb, CAT, placement)
           if (tsvline):
               tsvdata.append(tsvline)
        return tsvdata
      
    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       tsvdata = self.processAll(mydb, placement)
       self.AwardDisplay(tsvdata) 

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
