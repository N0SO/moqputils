#!/usr/bin/python3
from  moqputils.moqpdbutils import *
from  moqputils.configs.moqpdbconfig import *
from  moqputils.moqpawardefs import *
from  moqputils.moqpAwards.commonAwards import commonAwards
           
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
           """SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN,
              LOGHEADER.OPERATORS, LOGHEADER.LOCATION,
              LOGHEADER.NAME, LOGHEADER.ADDRESS, 
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY,
              LOGHEADER.EMAIL, SUMMARY.*
              FROM LOGHEADER INNER JOIN SUMMARY ON 
              LOGHEADER.ID=SUMMARY.LOGID
              WHERE ROOKIE > 0 AND LOGHEADER.LOCATION='MO'
              ORDER BY (SCORE) DESC""")
       elif cat in "MISSOURI SCHOOL CLUB":
           sumlist = mydb.read_query(\
           """SELECT CLUBS.*, CLUB_MEMBERS.*, 
              LOGHEADER.ID, LOGHEADER.CALLSIGN, 
              LOGHEADER.OPERATORS, 
              LOGHEADER.NAME, LOGHEADER.ADDRESS,
              LOGHEADER.CITY, LOGHEADER.STATEPROV ,
              LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, 
              LOGHEADER.EMAIL
              FROM CLUBS INNER JOIN CLUB_MEMBERS ON 
              CLUBS.CLUBID=CLUB_MEMBERS.CLUBID 
              INNER JOIN LOGHEADER ON 
              CLUB_MEMBERS.LOGID=LOGHEADER.ID 
              WHERE LOGHEADER.NAME LIKE '%SCHOOL%' AND 
              LOGHEADER.LOCATION='MO'
              ORDER BY (SCORE) DESC LIMIT 25""")
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
               LOGHEADER.EMAIL, COUNTY.COUNT, COUNTY.NAMES, COUNTY.LWTIME
               FROM LOGHEADER INNER JOIN COUNTY ON 
               LOGHEADER.ID=COUNTY.LOGID 
               ORDER BY (COUNTY.COUNT) DESC, (COUNTY.LWTIME) ASC
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
       #print(cat, sumlist)
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
       self.AwardList=['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
       for CAT in PLAQUELIST:
           #print(CAT)
           tsvdata = self.processOne(mydb, CAT, placement)
           self.AwardList.append(tsvdata)
       self.AwardDisplay(self.AwardList) 
       
class HTMLPlaques(CATEGORYPlaques):

    def AwardDisplay(self, tsvdata): 
       if (tsvdata):
           from htmlutils.htmldoc import htmlDoc   
           d = htmlDoc()
           d.openHead('2021 Missouri QSO Party First Place Plaques',
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>2021 Missouri QSO Party First Place Plaques</h2>""")
           tsvlist=d.tsvlines2list(tsvdata)
           d.addTable(tdata=tsvlist, 
                          header=True,
                          caption='2021 Missouri QSO Party First Place Plaque Winners')
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           d.saveAndView('plaquerpt.html')
           
               
       
