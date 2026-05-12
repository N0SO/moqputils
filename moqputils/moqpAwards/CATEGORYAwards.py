#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *
from moqputils.moqpAwards.commonAwards import commonAwards
       
class CATEGORYAwards(commonAwards):
           
    def __init__(self, placement = None):
        self.AwardList=[]
        if (placement):
            if placement.lower() == 'create-table':
                self._genCerts()
                exit()

            self.appMain(placement)

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
       
       
    def _genCerts(self, mydb=None):
        # Define database queries
        dquery ='DROP TABLE IF EXISTS AWARDS;'

        cquery = """CREATE TABLE AWARDS (
          id int NOT NULL AUTO_INCREMENT,
          awardid int NULL,
          recipientid int NULL,
          place int NULL,
          PRIMARY KEY (id));"""
          
        # Read certificate names list
        rquery = """SELECT CERTIFICATES.*,
           CONTESTCATEGORIES.ID AS CID,
           CONTESTCATEGORIES.NAME AS CNAME
           FROM CERTIFICATES LEFT JOIN CONTESTCATEGORIES ON
           CERTIFICATES.CAT_ID = CONTESTCATEGORIES.ID;"""          

        # Read SUMMARY table for certs in CONTESTCATEGORIES
        awardq =\
        """SELECT CERTIFICATES.*,
            CONTESTCATEGORIES.ID AS CID,
            CONTESTCATEGORIES.NAME AS CNAME,
            SUMMARY.LOGID AS LOGID,
            SUMMARY.SCORE AS SCORE,
            LOGHEADER.CALLSIGN AS CALLSIGN,
            LOGHEADER.OPERATORS AS OPS,
            LOGHEADER.NAME AS NAME
            FROM CERTIFICATES LEFT JOIN CONTESTCATEGORIES ON
            CERTIFICATES.CAT_ID = CONTESTCATEGORIES.ID
            LEFT JOIN SUMMARY ON 
            SUMMARY.MOQPCTAB=CERTIFICATES.CAT_ID
            LEFT JOIN LOGHEADER ON LOGHEADER.ID=SUMMARY.LOGID
            WHERE CAT_ID={}
            ORDER BY SCORE DESC LIMIT 2"""

        if(mydb == None):
            mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            mydb.setCursorDict()

        print(\
         'Generating 1st and 2nd place certificate recipients table...')
        
        """
        Delete the old table if it exists,
        then create a new one
        """
        mydb.read_query(dquery)
        mydb.read_query(cquery)
        
        """
        Read award names from database
        """
        awlist = mydb.read_query(rquery)

        if (len(awlist)==0) or (awlist == None):
            print('***Unable to read database table CERTIFICATES.')
            exit()
        else:
            awl_len = len(awlist)    

            """    
            Award names are in the CONTESTCATEGORIES table, except for 
            the 'special' awards that are not categories (rookie, 
            digital, vhf, most counties...) copy the 'CONTESTCATEGORIES'
            name if the 'CERTIFICATES' name is blank or null
            """
            for aw in awlist:
                if (aw['CAT_ID'] == aw['CID']) and \
                   ((aw['NAME'] == None) or (aw['NAME'] == '')):
                    aw['NAME'] = aw['CNAME']
                    
            # Show updated table to me for debug
            #print(f'updated {awlist=}')
                
        for aw in awlist:
            
            if aw['CAT_ID'] > 0: #CATEGORY Award
                awq = awardq.format(aw['CAT_ID'])
            else: # Extra awards (ROOKIE, DIGITAL, MOST COUNTIES...
                if aw['ID'] == 25: #ROOKIE
                    awq = """SELECT SUMMARY.*,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPS,
                                LOGHEADER.LOCATION AS LOCATION
                                from SUMMARY LEFT JOIN LOGHEADER ON
                                SUMMARY.LOGID = LOGHEADER.ID
                                WHERE (SUMMARY.ROOKIE=1) and
                                      (LOGHEADER.LOCATION LIKE 'MO')
                                ORDER BY SCORE DESC LIMIT 2;"""
                elif aw['ID'] == 27: #CLUB score
                    awq = None
                    pass
                elif aw['ID'] == 28: #Missouri digital
                    awq = """SELECT DIGITAL.ID AS ID, 
                                DIGITAL.LOGID AS LOGID, 
                                DIGITAL.QSOS AS QSOS ,
                                DIGITAL.SCORE as SCORE,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPS,
                                LOGHEADER.LOCATION AS LOCATION
                                from DIGITAL LEFT JOIN LOGHEADER ON
                                LOGID = LOGHEADER.ID
                                WHERE LOGHEADER.LOCATION = 'MO'
                                ORDER BY SCORE DESC LIMIT 2"""
                elif aw['ID'] == 29: #Non-Missouri digital
                    awq = """SELECT DIGITAL.ID AS ID, 
                                DIGITAL.LOGID AS LOGID, 
                                DIGITAL.QSOS AS QSOS ,
                                DIGITAL.SCORE as SCORE,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPS,
                                LOGHEADER.LOCATION AS LOCATION
                                from DIGITAL LEFT JOIN LOGHEADER ON
                                LOGID = LOGHEADER.ID
                                WHERE LOGHEADER.LOCATION != 'MO'
                                ORDER BY SCORE DESC LIMIT 2;"""
                elif aw['ID'] == 30: #Missouri VHF
                    awq = """SELECT VHF.ID AS ID, 
                                VHF.LOGID AS LOGID, 
                                VHF.QSOS AS QSOS ,
                                VHF.SCORE as SCORE,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPS,
                                LOGHEADER.LOCATION AS LOCATION
                                from VHF LEFT JOIN LOGHEADER ON
                                VHF.LOGID = LOGHEADER.ID
                                WHERE LOGHEADER.LOCATION = 'MO'
                                ORDER BY SCORE DESC LIMIT 2;"""
                elif aw['ID'] == 31: # Non-Missouri VHF
                    awq = """SELECT VHF.ID AS ID, 
                                VHF.LOGID AS LOGID, 
                                VHF.QSOS AS QSOS ,
                                VHF.SCORE as SCORE,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPS,
                                LOGHEADER.LOCATION AS LOCATION
                                from VHF LEFT JOIN LOGHEADER ON
                                VHF.LOGID = LOGHEADER.ID
                                WHERE LOGHEADER.LOCATION <> 'MO'
                                ORDER BY SCORE DESC LIMIT 2;"""
                elif aw['ID'] == 32: # Highest number of counties
                    awq = """SELECT COUNTY.ID AS ID, 
                                COUNTY.LOGID AS LOGID, 
                                COUNTY.COUNT AS SCORE,
                                LOGHEADER.ID AS LID,
                                LOGHEADER.CALLSIGN AS CALLSIGN,
                                LOGHEADER.OPERATORS AS OPERATORS,
                                LOGHEADER.LOCATION AS LOCATION
                                from COUNTY LEFT JOIN LOGHEADER ON
                                LOGID = LOGHEADER.ID
                                ORDER BY SCORE DESC LIMIT 2;"""
                else: # No query
                    awq = None
            if awq:
                sumlist = mydb.read_query(awq)
            else:
                sumlist = None
            
            if sumlist:
                """
                First Place
                """
                #print(f"Writing 1st Place {aw['NAME']}")
                if (len(sumlist) >= 1):
                    sumData = sumlist[0]
                    #print(sumData)
                    #print ('{} {}'.format(p1['id'], sumData['ID']))
                
                    awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, recipientid, place)
                                  VALUES (%s, %s, %s)""",
                                         [aw['ID'], sumData['LOGID'], 1])
                else: # No recipeint for this award
                    awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, place)
                                  VALUES (%s, %s)""",
                                         [aw['ID'], 1])
                """
                2nd Place
                """                             
                #print(f"Writing 2nd Place {aw['NAME']}")
                if (len(sumlist) >=2 ):
                    sumData = sumlist[1]    
                    awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, recipientid, place)
                                      VALUES (%s, %s, %s)""",
                                             [aw['ID'], sumData['LOGID'], 2])
                else: # No recipeint for this award
                    awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, place)
                                      VALUES (%s, %s)""",
                                             [aw['ID'], 2])

            else: #No query or no summary data
                print(f'*** No data for award {aw["ID"]=}, {aw["NAME"]=}')
                print(f'\t{awq=}')
                #print(f'\t{sumlist=}')
                awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, place)
                                      VALUES (%s, %s)""",
                                             [aw['ID'], 1])
                awardid = mydb.write_pquery(\
                       """INSERT INTO AWARDS (awardid, place)
                                      VALUES (%s, %s)""",
                                             [aw['ID'], 2])
        return True
        

    def processOne(self, aw, placement):
       #print(f'{aw=}')
       tsvdata = None
       
       if placement == '1':
           placestg = 'FIRST PLACE'
       else:
           placestg = 'SECOND PLACE'
           
       if aw['recipientid'] == None: # No entry 
           tsvdata = '{}\t{}\tNO ENTRY\t\t'.format(\
                    placestg,
                    aw['NAME'])
                    
       else:
       
           tsvdata = '{}\t{}\t{}\t{}\t{}'.format(\
                    placestg,
                    aw['NAME'],
                    aw['OPNAME'],
                    aw['CALLSIGN'],
                    aw['OPS'])
       return tsvdata

    def processAll(self, mydb, placement):
        awq ="""SELECT AWARDS.*, 
          CERTIFICATES.CAT_ID as CAT_ID,
          CERTIFICATES.NAME AS NAME,
          CONTESTCATEGORIES.NAME AS CNAME,
          LOGHEADER.ID AS LID,
          LOGHEADER.CALLSIGN,
          LOGHEADER.OPERATORS AS OPS,
          LOGHEADER.NAME as OPNAME,
          LOGHEADER.LOCATION AS LOCATIONS
          FROM AWARDS 
          LEFT JOIN CERTIFICATES ON AWARDS.awardid = CERTIFICATES.ID
          LEFT JOIN CONTESTCATEGORIES ON 
              CERTIFICATES.CAT_ID = CONTESTCATEGORIES.ID
          LEFT JOIN LOGHEADER ON AWARDS.recipientid = LOGHEADER.ID
          WHERE AWARDS.PLACE = {}
          ORDER BY AWARDS.id;""" 

        # Read list of award certificates from database
        awlist = mydb.read_query(awq.format(placement))
        if (len(awlist)==0) or (awlist == None):
            print('***Unable to read database table AWARDS.')
            exit()
        else:
            awl_len = len(awlist)    

            """    
            Award names are in the CONTESTCATEGORIES table, except for 
            the 'special' awards that are not categories (rookie, 
            digital, vhf, most counties...) copy the 'CONTESTCATEGORIES'
            name if the 'CERTIFICATES' name is blank or null
            """
            for aw in awlist:
                if ((aw['NAME'] == None) or (aw['NAME'] == '')):
                    aw['NAME'] = aw['CNAME']

            # Show updated table to me for debug
            #print(f'updated {awlist=}')
            #exit()

        tsvdata = ['AWARD\tCATEGORY\tRECIPIENT\tCALL\tOPERATORS']
        for aw in awlist:          
           tsvline = self.processOne(aw, placement)
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
        AWARDLIST = mydb.read_query("""
          select AWARDS.id, AWARDS.recipientid,AWARDS.place,
               CERTIFICATES.NAME as cname, CERTIFICATES.CAT_ID,
               CONTESTCATEGORIES.NAME as award,
               LOGHEADER.NAME as name,
               LOGHEADER.CALLSIGN as callsign,
               LOGHEADER.OPERATORS as operators,
               SUMMARY.SCORE as score,
               LOGHEADER.ADDRESS as address,
               LOGHEADER.CITY as city,
               LOGHEADER.STATEPROV as state,
               LOGHEADER.ZIPCODE as zip,
               LOGHEADER.COUNTRY as country,
               LOGHEADER.EMAIL as email
          from AWARDS left join CERTIFICATES on 
                                 (AWARDS.awardid = CERTIFICATES.ID)
             left join CONTESTCATEGORIES on 
                       (CERTIFICATES.CAT_ID = CONTESTCATEGORIES.ID)
             left join LOGHEADER on (AWARDS.recipientid = LOGHEADER.ID)
             left join SUMMARY on (SUMMARY.LOGID = AWARDS.recipientid)
          ORDER BY callsign ASC;""")  
             
        """
        Fill-in the names not found in CONTESTCATEGORIES.
        """
        for a in AWARDLIST:
            #if a['recipientid']:
                if (a['award'] == None) or (a['award']=='') :
                    a['award'] = a['cname']
                    
                    #print(f"{a['awardname']=}, {a['cname']=}")
        #print(f'{AWARDLIST=}')
        
    
               
        #print(AWARDLIST)
        labeldata = self.new_processAll(CATLABELHEADER, 
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
           d.openHead('{} Missouri QSO Party {} Awards'.format(YEAR, subStg),
                  './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>{} Missouri QSO Party {} Winners</h2>""".format(YEAR, subStg))
           tdata=d.tsvlines2list(tsvdata)
           d.addTable(tdata, 
                          header=True,
                          caption='Certificates Only, No Plaques')
           d.closeBody()
           d.closeDoc()

           d.showDoc()
           d.saveAndView('certificates%s.html'%(fileAdd))
        
      
