#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *
from moqputils.moqpAwards.commonAwards import commonAwards

class STATEAwards(commonAwards):
    
    def __init__(self, place = None):
        #print("Running STATEAwards __init__...")
        self._readStates(defslist=STATELIST)
        #self._createAwardTable()
        if (place):
            if place == 'update-list':
                self._readStates(defslist=STATELIST, force=True)
            elif place == 'create-table':
                self._createAwardTable(TABLENAME='STATEPROVAWARDS')
            else:
                self.appMain(place)
            
    def _readStates(self, db=None, defslist=None, force=False):
            """
            Save the state/province defs from moqpawardefs to a new
            table STATELIST.
            call with force = True to force an update of the DB table
            STATELIST.
            """
            if db == None:
                db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
                db.setCursorDict()
            result = db.read_query("SHOW TABLES LIKE 'STATELIST'")
            if (force or len(result) == 0):
                """Create and fill state / prov  list tables"""
                db.write_query('DROP TABLE IF EXISTS STATELIST;')
                db.write_query("""CREATE TABLE STATELIST (
                        id int NOT NULL AUTO_INCREMENT,
                        name varchar(30) NULL,
                        sp varchar(5) NULL,
                        matchlist varchar(80) NULL,
                        PRIMARY KEY (id));""")
                for s in defslist:
                    """
                    name = s[0]
                    spl = s[1].split(',')
                    sp = spl[0].replace("'","")
                    ml = s[1].replace("'","")
                    print('name={}\nAbreviation={}\nmatchlist={}\nsplit={}'.format(name, sp, ml,spl))
                    """
                    db.write_pquery(\
                        """INSERT INTO STATELIST (name, sp, matchlist)
                                  VALUES (%s, %s, %s)""",
                                  [name, sp, ml])
                        
            return result  

    def _createAwardTable(self, 
                          db=None, 
                          TABLENAME='STATEPROVAWARDS'):
        print('Creating state/province award table...')
        if db == None:
            db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            db.setCursorDict()
        result = db.read_query("SHOW TABLES LIKE '{}';".format(TABLENAME))
        print(result)
        if (len(result) != 0):
            """Create and fill state / prov  list tables"""
            db.write_query("DROP TABLE IF EXISTS `{}`;".format(TABLENAME))
        db.write_query("""CREATE TABLE {} (
                                id int NOT NULL AUTO_INCREMENT,
                                awardid int NULL,
                                recipientid int NULL,
                                place int NULL,
                                PRIMARY KEY (id));""".format(TABLENAME))
        sl = db.read_query("""SELECT * FROM STATELIST WHERE 1;""")
        #print(sl)
        for s in sl:
            mstg=''
            temp=s['matchlist'].split(',')
            
            first = True      
            for t in temp:
                if first:
                    mstg += ('"{}"'.format(t))
                    first = False
                else:
                    mstg += (', "{}"'.format(t))
            
            #print(s['matchlist'],'->',mstg)
            
            entry = db.read_query(\
                """SELECT LOGHEADER.*,
                   SUMMARY.*
                   FROM LOGHEADER INNER JOIN SUMMARY ON
                   LOGHEADER.ID=SUMMARY.LOGID
                   WHERE LOGHEADER.LOCATION IN
                   (""" + mstg + """) AND 
                   SUMMARY.MOQPCAT != 'CHECKLOG'
                   ORDER BY SCORE DESC
                   LIMIT 5""")
            #print(entry)

            logid1=0
            logid2=0
            if len(entry)>=1:
               logid1 = entry[0]['ID'] #logid of 1st place winner
            if len(entry)>=2:
               logid2 = entry[1]['ID'] #logid of 2nd place winner

            awardid1 = db.write_pquery(\
                        """INSERT INTO """+TABLENAME+""" 
                            (awardid, recipientid, place)
                            VALUES (%s, %s, %s);""",
                            [s['id'], logid1, 1])

            awardid2 = db.write_pquery(\
                        """INSERT INTO """+TABLENAME+""" 
                            (awardid, recipientid, place)
                            VALUES (%s, %s, %s);""",
                            [s['id'], logid2, 2])                    

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

        tsvdata = "%s\t%s\t"%(place,state)
        if (sdata):
            if (sdata['OPERATORS'] == sdata['CALLSIGN']):
                """ Don't display operator if op call matches 
                station call """
                sdata['OPERATORS'] = ''
            tsvdata += '%s\t%s\t%s\t'%(\
                                       sdata['NAME'],
                                       sdata['CALLSIGN'],
                                       sdata['OPERATORS'])
        else:
            tsvdata += 'NO ENTRY'
        return tsvdata

    def getStateQuery(self, mydb, NAMELIST):
        CATLIST = mydb.read_query(\
                """SELECT LOGHEADER.*,
                   SUMMARY.*
                   FROM LOGHEADER INNER JOIN SUMMARY ON
                   LOGHEADER.ID=SUMMARY.LOGID
                   WHERE LOGHEADER.LOCATION IN
                   (""" + NAMELIST + """) AND SUMMARY.MOQPCAT != 'CHECKLOG'
                   ORDER BY SCORE DESC
                   LIMIT 5""")
        return CATLIST

    def getState(self,mydb, place, STATE, NAMELIST):
       CATLIST = self.getStateQuery(mydb, NAMELIST)
       #if (len(CATLIST)>1):
       placestg, catdata = self.setPlacement(place, CATLIST)
       #print(placestg,catdata)
       tsvdata = self.ShowAward(mydb, 
                                placestg,
                                STATE,
                                catdata)
       return tsvdata

    def _oneLine(self, place, dat):
        retdat = ''
        placestg ='oops...'
        if place =='1':
            placestg = 'FIRST PLACE'
        if place =='2':
            placestg = 'SECOND PLACE'
        if dat['recipientid'] == 0:
            name = 'NO ENTRY'
            call = ''
            ops = ''
        else:
            name = dat['name']
            call = dat['callsign']
            if dat['ops'] == dat['callsign']:
                ops = ''
            else:
                ops = dat['ops']            
            
        return '{}\t{}\t{}\t{}\t{}'.format(\
                                       placestg,
                                       dat['awardname'],
                                       name,
                                       call,
                                       ops)
    
    def states(self, db, place):
        stateprovs = db.read_query("""SELECT * FROM 
                                         STATEPROVAWARDS_VIEW 
                                         WHERE `place`= {}
                                         ORDER BY awardid;""".format(\
                                                               place))
        awards = ['PLACE\tAWARD\tRECIPIENT\tCALLSIGN\tOPS']
        for sp in stateprovs:
            awards.append(self._oneLine(place, sp))
        return awards

 
    def appMain(self, place):
       if (place in ['1','2']):
           mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
           mydb.setCursorDict()
           awards = self.states(mydb, place)
           self.AwardDisplay(awards)

class HTMLSTATEAwards(STATEAwards):

    def __init__(self, place = None, extra = None):
        #print("Running STATEAwards...")
        if (place):
            self.appMain(place)

    def forDebug(self):
        print('In the HTMLSTATEAwards class...')


    def AwardDisplay(self, awards):
       if (awards):
           #theader = self.buildDictHeader(KEYS1, LABELS1)
           #showmeList= self.addHeader(theader, showmeList)

           from htmlutils.htmldoc import htmlDoc
           from htmlutils.htmltable import htmlTable
           d = htmlDoc()
           thisPlace='WTF'
           if ('FIRST PLACE' in  awards[1]):
               thisPlace='FIRST'
           elif ('SECOND PLACE' in awards[1]):
               thisPlace='SECOND'
           titleStr = '{} Missouri QSO Party  State / Province {} PLACE Awards'.format(YEAR, thisPlace)
           d.openHead(titleStr, './styles.css')
           d.closeHead()
           d.openBody()
           d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
           d.add_unformated_text(\
             """<h2 align='center'>%s</h2>"""%(titleStr) )

           awardslist = d.tsvlines2list(awards)
           t = htmlTable()
           d.add_unformated_text(t.makeTable(awardslist,
                            header=True,
                            caption='Certificates only, no plaques'))
           d.closeDoc()

           d.showDoc()
           #d.saveAndView('states%s.html'%(thisPlace))
           
class STATELabels(STATEAwards):

    def ShowAward(self, mydb, place, state, sdata):

        tsvdata = '%s\t%s\t'%(place,state)
        if (sdata):     
            tsvdata += '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d'%(\
                               sdata['CALLSIGN'],
                               sdata['OPERATORS'],
                               sdata['NAME'],
                               sdata['ADDRESS'],
                               sdata['CITY'],
                               sdata['STATEPROV'],                  
                               sdata['EMAIL'],
                               sdata['ZIPCODE'],
                               sdata['COUNTRY'],             
                               sdata['SCORE'])
        else:
            tsvdata += 'NO ENTRY'
        return tsvdata
        
    def states(self, mydb, place):
        awards = [CATLABELHEADER]
        labeldata = self.Labels_processAll(mydb, 
                                            CATLABELHEADER, 
                                            STATELIST)
        return labeldata
        
    def get_awardquery(self, mydb, cat):
        sumlist = STATEAwards.getStateQuery(self, mydb, cat)
        return sumlist

    def appMain(self, place=None):
        STATEAwards.appMain(self, '1')
        #STATEAwards.appMain(self, '2')
