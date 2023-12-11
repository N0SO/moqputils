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
       #print(cat, catlist)
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
              "WHERE (QSOS > 49) AND (LOGHEADER.LOCATION='MO') "+\
              "ORDER BY (SCORE) DESC")
       elif cat in 'NON-MISSOURI HIGHEST DIGITAL':
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, DIGITAL.* "+\
              "FROM LOGHEADER INNER JOIN DIGITAL ON "+\
              "LOGHEADER.ID=DIGITAL.LOGID "+\
              "WHERE (LOGHEADER.LOCATION<>'MO') "+\
              "ORDER BY (SCORE) DESC")
       elif cat in 'MISSOURI VHF':
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, VHF.* "+\
              "FROM LOGHEADER INNER JOIN VHF ON "+\
              "LOGHEADER.ID=VHF.LOGID "+\
              "WHERE LOGHEADER.LOCATION='MO' "+\
              "ORDER BY (SCORE) DESC")
           #print('MISSOURI VHF Selections = {}'.format(sumlist))
       elif cat in 'NON-MISSOURI VHF':
           sumlist = mydb.read_query(\
             "SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN, "+\
              "LOGHEADER.CALLSIGN, LOGHEADER.OPERATORS, "+\
              "LOGHEADER.NAME, LOGHEADER.ADDRESS, "+\
              "LOGHEADER.CITY, LOGHEADER.STATEPROV ,"+\
              "LOGHEADER.ZIPCODE, LOGHEADER.COUNTRY, "+\
              "LOGHEADER.EMAIL, VHF.* "+\
              "FROM LOGHEADER INNER JOIN VHF ON "+\
              "LOGHEADER.ID=VHF.LOGID "+\
              "WHERE LOGHEADER.LOCATION <> 'MO' "+\
              "ORDER BY (SCORE) DESC")
           #print('NON-MISSOURI VHF Selections = {}'.format(sumlist))
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
       
       if (placement == '1'):
              placeStg = 'FIRST PLACE'
              placeIndex = 0
       elif (placement == '2'):
              placeStg = 'SECOND PLACE'
              placeIndex = 1
       
       sumlist = self.get_awardquery(mydb, cati)

       if (len(sumlist) >= placeIndex + 1):
           sumData = sumlist[placeIndex]
       else:
           sumData = dict()
       tsvdata = ''
       tsvdata = self.processHeader(mydb, 
                                    placeStg, 
                                    cati[0], 
                                    sumData)

       return tsvdata

    def _getAwards(self,mydb):
        """
        Read award names from database
        """
        awlist = None
        awlist = mydb.read_query(\
                 "SELECT * FROM CONTESTCATEGORIES WHERE 1")
        return awlist

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       self.AwardList=['FIRST PLACE PLAQUES','AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
       for CAT in PLAQUELIST:
           #print(CAT)
           tsvdata = self.processOne(mydb, CAT, placement)
           self.AwardList.append(tsvdata)
       self.AwardList.append('ADDITIONAL FIRST PLACE CERTIFICATES')
       self.AwardList.append('AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS')
       #print('now certs...')
       for CAT in ADDITIONALFIRST:
           #print(CAT)
           CATi=[CAT, "'{}'".format(CAT)]
           #print(CATi)
           tsvdata = self.processOne(mydb, CATi, placement)
           self.AwardList.append(tsvdata)
       self.AwardDisplay(self.AwardList) 
       
class HTMLPlaques(CATEGORYPlaques):

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       self.AwardList=['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
       for CAT in PLAQUELIST:
           #print(CAT)
           tsvdata = self.processOne(mydb, CAT, placement)
           self.AwardList.append(tsvdata)
           
       if (placement == '1'): 
           """
           Build 2nd table for additional first place certificates
           """
           placeStg = 'First'
           captionStg = \
               'First Place Plaques - Plaque recipients will also recieve certificates.'
           self.AwardList2=\
              ['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
           for CAT in ADDITIONALFIRST:
               CATi=[CAT, "'{}'".format(CAT)]
               tsvdata = self.processOne(mydb, CATi, placement)
               self.AwardList2.append(tsvdata)
       else:
           """ Add additional awards to the first table."""
           placeStg = 'Second'
           captionStg = 'Certificates Only, No Plaques'
           for CAT in ADDITIONALFIRST:
               CATi=[CAT, "'{}'".format(CAT)]
               tsvdata = self.processOne(mydb, CATi, placement)
               self.AwardList.append(tsvdata)
       # Build HTML document
       from htmlutils.htmldoc import htmlDoc   
       d = htmlDoc()
       if (placement == '1'):
           d.openHead('{} Missouri QSO Party First Place Awards'\
                      .format(YEAR),
                      './styles.css')
       else:
           d.openHead('{} Missouri QSO Party Second Place Awards'\
                      .format(YEAR),
                      './styles.css')
       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party {} Place Awards</h2>""".format(YEAR,placeStg))
       d.addTable(tdata=d.tsvlines2list(self.AwardList), 
                  header=True,
                  caption=captionStg)

       if (placement == '1'):
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party Additional First Place Awards</h2>""".format(YEAR, placeStg))
           d.addTable(tdata=d.tsvlines2list(self.AwardList2), 
                  header=True,
                  caption='Certificates Only, No Plaques')

       d.closeBody()
       d.closeDoc()

       d.showDoc()
       d.saveAndView('plaquerpt.html')
