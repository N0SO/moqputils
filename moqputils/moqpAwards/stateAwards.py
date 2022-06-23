#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *
from moqputils.moqpAwards.commonAwards import commonAwards

class STATEAwards(commonAwards):
    
    def __init__(self, place = None, extra = None):
        #print("Running STATEAwards __init__...")
        if (place):
            self.appMain(place)

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
            tsvdata += '%s\t%s\t%s\t'%(\
                                       sdata['NAME'],
                                       sdata['CALLSIGN'],
                                       sdata['OPERATORS'])
        else:
            tsvdata += 'NO ENTRY'
        return tsvdata


    def getState(self,mydb, place, STATE, NAMELIST):
       CATLIST = mydb.read_query(\
                """SELECT LOGHEADER.*,
                   SUMMARY.*
                   FROM LOGHEADER INNER JOIN SUMMARY ON
                   LOGHEADER.ID=SUMMARY.LOGID
                   WHERE LOGHEADER.LOCATION IN
                   (""" + NAMELIST+ """)
                   ORDER BY SCORE DESC
                   LIMIT 5""")
       #if (len(CATLIST)>1):
       placestg, catdata = self.setPlacement(place, CATLIST)
       #print(placestg,catdata)
       tsvdata = self.ShowAward(mydb, 
                                placestg,
                                STATE,
                                catdata)
       return tsvdata

    def states(self, mydb, place):
       awards = []
       for state in STATELIST:
           awards.append(self.getState(mydb, 
                              place, 
                              state[0], 
                              state[1]))
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
           if ('FIRST PLACE' in  awards[0]):
               thisPlace='FIRST'
           elif ('SECOND PLACE' in awards[0]):
               thisPlace='SECOND'
           titleStr = '2021 Missouri QSO Party  State / Province %s PLACE Awards'%(thisPlace)
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
                            header=None,
                            caption='Certificates only, no plaques'))
           d.closeDoc()

           d.showDoc()
           d.saveAndView('states%s.html'%(thisPlace))
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
                               sdata['ZIPCODE'],
                               sdata['COUNTRY'],                               
                               sdata['EMAIL'],
                               sdata['SCORE'])
        else:
            tsvdata += 'NO ENTRY'
        return tsvdata

    def appMain(self, place=None):
        STATEAwards.appMain(self, '1')
        STATEAwards.appMain(self, '2')
