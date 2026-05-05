#!/usr/bin/python3
from  moqputils.moqpdbutils import *
from  moqputils.configs.moqpdbconfig import *
from  moqputils.moqpawardefs import *
from  moqputils.moqpAwards.commonAwards import commonAwards

class CATEGORYPlaques(commonAwards):
    def __init__(self, placement = '1'):
        self.AwardList=[]
        if (placement):
            if placement.lower() == 'create-table':
               self._genPlaques()
               exit()
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
            """SELECT LOGHEADER.ID, LOGHEADER.CALLSIGN,
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
    """
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
       """
    def _genCerts(self, mydb):
        """
        Read award names from database
        """
        awlist = None
        awlist = mydb.read_query(\
                 """SELECT * FROM PLAQUESLIST WHERE 
                    certificate = 1
                    and plaque = 0;""")
        #print(awlist)
        ptext = ''
        first = True      
        for p1 in awlist:
            cati = [p1['award'],'"{}"'.format(p1['award'])]
            #print(cati)    
            sumlist = self.get_awardquery(mydb, cati)
            """
            First Place
            """
            if p1['plaque'] == 0:
                if (len(sumlist) >= 1):
                    sumData = sumlist[0]
                    #print(sumData)
                    #print ('{} {}'.format(p['id'], sumData['ID'])) 
                    awardid = mydb.write_pquery(\
                       """INSERT INTO FIRSTPLACE (awardid, recipientid, place)
                                  VALUES (%s, %s, %s)""",
                                         [p1['id'], sumData['ID'], 1])
                else: # No recipeint for this award
                    awardid = mydb.write_pquery(\
                       """INSERT INTO FIRSTPLACE (awardid, place)
                                  VALUES (%s, %s)""",
                                         [p1['id'], 1])
            """
            2nd Place
            """                             
            if (len(sumlist) >=2 ):
                sumData = sumlist[1]    
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, recipientid, place)
                                  VALUES (%s, %s, %s)""",
                                         [p1['id'], sumData['ID'], 2])
            else: # No recipeint for this award
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, place)
                                  VALUES (%s, %s)""",
                                         [p1['id'], 2])
            
        return True
           

    def _genPlaques(self, mydb=None):
        if mydb == None:
            mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            mydb.setCursorDict()
            
        print('Generating 1st and 2nd place awards table...')
    
        dquery ='DROP TABLE IF EXISTS FIRSTPLACE;'
        query1 = """CREATE TABLE FIRSTPLACE (
          id int NOT NULL AUTO_INCREMENT,
          awardid int NULL,
          recipientid int NULL,
          place int NULL,
          PRIMARY KEY (id));"""
        
        """
        Read award names from database
        """
        awlist = None
        awlist = mydb.read_query(\
                 """SELECT PLAQUES.*, CONTESTCATEGORIES.ID as CID,
                    CONTESTCATEGORIES.NAME as CNAME 
                    FROM PLAQUES LEFT JOIN CONTESTCATEGORIES ON
                    CONTESTCATEGORIES.ID = PLAQUES.CAT_ID""")
        #print(awlist)
        if (awlist):
            result = mydb.read_query("SHOW TABLES LIKE 'FIRSTPLACE'")
            if (len(result) > 0): #If FIRSTPLACE table exists...
                mydb.write_query(dquery) #Delete it
            mydb.write_query(query1) #and create new, empty table

        # Walk thru award list and find winners in SUMMARY table
        for p in awlist:
            #print(p)
            if (p['CAT_ID']==0) and (p['MULTI']==1): 
                #Multicategory award, build list
                #aname = ''
                plstg = ''
                plcats = mydb.read_query(f"""SELECT CAT_ID FROM 
                        MULTIAWARD WHERE AWARD_ID = {p['ID']}""")
                if (len(plcats)) > 0:
                    plstg = ", ".join(\
                      str(v) for d in plcats for v in d.values())
                    print('{plstg=}')
                    plquery = f"""SELECT SUMMARY.*, LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPERATORS,
                                LOGHEADER.LOCATION AS LOCATION
                            from SUMMARY LEFT JOIN LOGHEADER ON
                            SUMMARY.LOGID = LOGHEADER.ID
                            WHERE SUMMARY.MOQPCTAB in ({plstg})
                            ORDER BY SCORE DESC LIMIT 2;"""
                    #aname = p['NAME'].upper()
                else:
                    print('*** Error finding category names for award.')
                    print(f'Category data:\n{p}')
                    print(f'MULTIAWARD data:\n{plstg=}\n{plcats=}')
                    #print(f'{aname=}')
                    print(f'{plquery=}')
            else: #Single category award
                plquery = f"""SELECT SUMMARY.*, LOGHEADER.ID AS LID,
                        LOGHEADER.CALLSIGN AS CALLSIGN,
                        LOGHEADER.OPERATORS AS OPERATORS,
                        LOGHEADER.LOCATION AS LOCATION
                    from SUMMARY LEFT JOIN LOGHEADER ON
                        SUMMARY.LOGID = LOGHEADER.ID
                    WHERE SUMMARY.MOQPCTAB = {p['CAT_ID']}
                    ORDER BY SCORE DESC LIMIT 2;"""
                #aname = p['CNAME']
                    
            """
            First Place
            """
            sumlist = mydb.read_query(plquery) # Get summary data
            if (len(sumlist) >= 1):
                sumData = sumlist[0]
                #print(sumData)
                #print ('{} {}'.format(p['id'], sumData['ID'])) 
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, recipientid, place)
                                  VALUES (%s, %s, %s)""",
                                         [p['ID'], sumData['ID'], 1])
            else: # No recipeint for this award
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, place)
                                  VALUES (%s, %s)""",
                                         [p['ID'], 1])
            """
            2nd Place
            """                             
            if (len(sumlist) >=2 ):
                sumData = sumlist[1]    
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, recipientid, place)
                                  VALUES (%s, %s, %s)""",
                                         [p['ID'], sumData['ID'], 2])
            else: # No recipeint for this award
                awardid = mydb.write_pquery(\
                   """INSERT INTO FIRSTPLACE (awardid, place)
                                  VALUES (%s, %s)""",
                                         [p['ID'], 2])
                                         
        #self._genCerts(mydb)
                                   
        return True
        
    def _getAwards(self,mydb):
        """
        Read award names from database
        """
        awlist = None
        awlist = mydb.read_query(\
                 "SELECT * FROM CONTESTCATEGORIES WHERE 1")
        return awlist
        
    def _fixNone(self, s):
        if s == None:
            return ''
        else:
            return s
            
    def _oneLine(self, place, dat):
        print(f'{dat=}')
        retdat = ''
        placestg ='oops...'
        if place =='1':
            placestg = 'FIRST PLACE'
        if place =='2':
            placestg = 'SECOND PLACE'
        if (dat['RECIPIENT'] == 0) or (dat['RECIPIENT'] == None):
            name = 'NO ENTRY'
            call = ''
            ops = ''
            award = ''
        else:
            call = dat['CALLSIGN']
            if dat['OPERATORS'] == dat['CALLSIGN']:
                ops = ''
            else:
                ops = dat['OPERATORS']            

            award = 'Oops'
            name = ''
            if dat['CNAME'] != None:
                award = dat['CNAME'] # Use name from CONTESTCATEGORIES
            elif dat['PNAME'] != None:
                award = dat['PNAME'] # Use name from PLAQUES
        return '{}\t{}\t{}\t{}\t{}'.format(\
                                       placestg,
                                       award,
                                       name,
                                       call,
                                       ops)
            
        
    def _getDBAwardList(self, mydb, placement):
       if placement == '1':
           placestg = 'FIRST PLACE'
                    
           AListq = """SELECT FIRSTPLACE.ID as ID,
                       FIRSTPLACE.recipientid as RECIPIENT,
                       FIRSTPLACE.awardid,
                       PLAQUES.ID as PID,
                       PLAQUES.CAT_ID as PCID,
                       PLAQUES.NAME as PNAME,
                       CONTESTCATEGORIES.ID as CID,
                       CONTESTCATEGORIES.NAME as CNAME,                       
                       SUMMARY.ID as SID,
                       SUMMARY.LOGID as LOGID,
                       SUMMARY.SCORE as SCORE,
                       SUMMARY.MOQPCTAB as CTAB,
                       LOGHEADER.CALLSIGN as CALLSIGN,
                       LOGHEADER.OPERATORS as OPERATORS,
                       LOGHEADER.LOCATION as LOCATION
                FROM FIRSTPLACE LEFT JOIN PLAQUES ON FIRSTPLACE.awardid = PLAQUES.ID
                       LEFT JOIN SUMMARY on FIRSTPLACE.recipientid = SUMMARY.ID
                       LEFT JOIN CONTESTCATEGORIES ON
                           CONTESTCATEGORIES.ID = PLAQUES.CAT_ID  
                       LEFT JOIN LOGHEADER ON LOGHEADER.ID = SUMMARY.LOGID
                WHERE FIRSTPLACE.place=1 """
                    
       else:
           placestg = 'SECOND PLACE'
           AListq = """SELECT * FROM FIRSTPLACE_VIEW WHERE 
                    place = 2 and
                    plaque = 1
                    order by awardid;"""
                    
       DBPLAQUELIST = mydb.read_query(AListq)
                    
       self.AwardList=['PLACE\tAWARD\tRECIPIENT\tCALL\tOPERATORS']
       for plaque in DBPLAQUELIST:
           self.AwardList.append(self._oneLine(placement, plaque))
           """
           self.AwardList.append('{}\t{}\t{}\t{}\t{}'.format(\
                                  placestg,
                                  plaque['award'],
                                  self._fixNone(plaque['name']),
                                  self._fixNone(plaque['callsign']),
                                  self._fixNone(plaque['operators'])))
           """
       if (placement == '2'):
           AwardList2 = None
           DBCERTLIST = mydb.read_query(\
                 """SELECT * FROM FIRSTPLACE_VIEW WHERE 
                    plaque = 0 and
                    place = 2 and
                    certificate = 1
                    order by awardid;""")
           for cert in DBCERTLIST:
               self.AwardList.append(self._oneLine(placement, cert))
               """
               self.AwardList.append('{}\t{}\t{}\t{}\t{}'.\
                           format(placestg,
                                  cert['award'],
                                  self._fixNone(cert['name']),
                                  self._fixNone(cert['callsign']),
                                  self._fixNone(cert['operators'])))
               """


       else:
           """
           Build 2nd table for additional first place certificates
           placeStg = 'First'
           captionStg = \
               'First Place Plaques - Plaque recipients will also recieve certificates.'
           """
           AwardList2=\
              ['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
           DBCERTLIST = mydb.read_query(\
                 """SELECT * FROM FIRSTPLACE_VIEW WHERE 
                    plaque = 0 and
                    place = 1 and
                    certificate = 1
                    order by awardid;""")
                    
           for cert in DBCERTLIST:
               AwardList2.append(self._oneLine(placement, cert))
               """
               AwardList2.append('{}\t{}\t{}\t{}\t{}'.\
                           format(placestg,
                                  cert['award'],
                                  self._fixNone(cert['name']),
                                  self._fixNone(cert['callsign']),
                                  self._fixNone(cert['operators'])))
               """ 
       return [self.AwardList, AwardList2]

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
 
       awards = self._getDBAwardList(mydb, placement)
 
       if placement == '1':
           self.AwardList.append('ADDITIONAL FIRST PLACE CERTIFICATES')
           for a in awards[1]:
               self.AwardList.append(a)

       self.AwardDisplay(self.AwardList) 
       
class HTMLPlaques(CATEGORYPlaques):

    def appMain(self, placement):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       awards = self._getDBAwardList(mydb, placement)
       # Build HTML document
       from htmlutils.htmldoc import htmlDoc   
       d = htmlDoc()
       if (placement == '1'):
           d.openHead('{} Missouri QSO Party First Place Awards'\
                      .format(YEAR),
                      './styles.css')
           placeStg='First'
           captionStg='First Place Plaques - Plaque recipients will also receive certificates'
       else:
           d.openHead('{} Missouri QSO Party Second Place Awards'\
                      .format(YEAR),
                      './styles.css')
           placeStg='Second'
           captionStg='Second Place Certificates - No Plaques'

       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party {} Place Awards</h2>""".format(YEAR,placeStg))
       d.addTable(tdata=d.tsvlines2list(awards[0]), 
                  header=True,
                  caption=captionStg)

       if (placement == '1'):
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party Additional First Place Awards</h2>""".format(YEAR, placeStg))
           d.addTable(tdata=d.tsvlines2list(awards[1]), 
                  header=True,
                  caption='Certificates Only, No Plaques')

       d.closeBody()
       d.closeDoc()

       d.showDoc()
       #d.saveAndView('plaquerpt.html')
