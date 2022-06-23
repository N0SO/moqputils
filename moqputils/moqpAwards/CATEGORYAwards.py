#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *
from moqputils.moqpAwards.commonAwards import commonAwards

CATLABELHEADER =   'RANK\tAWARD\tSTATION\tOPERATORS\t'+ \
                   'NAME\tADDRESS\tCITY\tSTATE\tZIP\t'+ \
                   'COUNTRY\tEMAIL'
       
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
       elif cat in 'MISSOURI SCHOOL CLUB':
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
       elif cat in 'MISSOURI CLUB':
           sumlist = mydb.read_query(\
              """SELECT CLUBS.*, CLUB_MEMBERS.*,
              LOGHEADER.CALLSIGN, LOGHEADER.LOCATION,
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
               ORDER BY COUNTY.COUNT DESC, COUNTY.LWTIME ASC
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
        tsvdata = ['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
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

    def processAll(self, mydb, placement):
        labeldata = self.Labels_processAll(mydb, 
                                            CATLABELHEADER, 
                                            AWARDLIST)
        return labeldata
        
class HTMLAwards(CATEGORYAwards):

     def AwardDisplay(self, tsvdata): 
       if (tsvdata):
           #print(tsvdata[1])
           from htmlutils.htmldoc import htmlDoc  
           if ('FIRST PLACE' in tsvdata[1]):
               subStg = 'First'
               fileAdd=1
           elif ('SECOND PLACE' in tsvdata[1]):
               subStg = 'Second'
               fileAdd=2
           else:
               subStg = 'UNKOWN'
               fileAdd=0
           subStg += ' Place Certificate'
           d = htmlDoc()
           d.openHead('2021 Missouri QSO Party %s Awards'%(subStg),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>2021 Missouri QSO Party %s Winners</h2>"""%(subStg))
           tdata=d.tsvlines2list(tsvdata)
           d.addTable(tdata, 
                          header=True,
                          caption='2021 Missouri QSO Party %s Winners'%(subStg))
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           d.saveAndView('certificates%s.html'%(fileAdd))
        
      
