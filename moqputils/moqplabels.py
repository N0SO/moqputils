#!/usr/bin/python3
"""
moqplables - A collection of classes to help with the creation 
             and publishing of MOQP certificates and labels for 
             mailing.

Update History:
* Fri Feb 20 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
* Sun Dec 11 2021 Mike Heitmann, N0SO <n0so@arrl.net>
-V0.1.0 - Update to support the new DEVMODPATH code.
"""

from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import AWARDLIST 
from qrzutils.qrz.qrzlookup import QRZLookup
VERSION = '0.1.0'
"""
AWARDLIST = ['MISSOURI FIXED MULTI-OP',
    'MISSOURI FIXED SINGLE-OP HIGH POWER',
    'MISSOURI FIXED SINGLE-OP LOW POWER',
    'MISSOURI FIXED SINGLE-OP QRP POWER',
    'MISSOURI EXPEDITION MULTI-OP',
    'MISSOURI EXPEDITION SINGLE-OP HIGH POWER',
    'MISSOURI EXPEDITION SINGLE-OP LOW POWER',
    'MISSOURI EXPEDITION SINGLE-OP QRP POWER',
    'Missouri Mobile Unlimited',
    'Missouri Mobile Multi-Op LOW POWER',
    'Missouri Mobile Single-Op LOW POWER',
    'Missouri Mobile Single-Op LOW POWER CW',
    'Missouri Mobile Single-Op LOW POWER Phone',
    'US Single Operator HIGH POWER',
    'US Single Operator LOW POWER',
    'US Single Operator QRP POWER',
    'US Multi-Op',
    'Canada',
    'DX',
    'Missouri Rookie',
    'Missouri School Club',
    'Missouri clubs',
    'Missouri Digital',
    'Non Missouri Digital',
    'Missouri VHF',
    'Non-Missouri VHF',
    'Highest Number of Counties' ]
"""
SHOWMEHEADERS =    'AWARD\tSTATION\tOPERATORS\t'+ \
                   'NAME\tADDRESS\tCITY\tSTATE\tZIP\t'+ \
                   'COUNTRY\tEMAIL'

CATCOLUMNHEADERS = 'PLACEMENT\t' + SHOWMEHEADERS

STATEHEADER = CATCOLUMNHEADERS+'\tSCORE'

STATELIST = [  ["ALABAMA","'AL','ALABAMA'"],
               ["ALASKA","'AK','ALASKA'"],
               ["ARIZONA","'AZ','ARIZONA'"],
               ["ARKANSAS","'AR','ARKANSAS'"],
               ["CALIFORNIA", "'CA','EB','LAX','ORG','SBA','SCV','SDG','SF','SJV','SV','PAC'"],
               ["COLORADO","'CO','COLORADO'"],
               ["CONNECTICUT","'CT','CONNECTICUT'"],
               ["DELAWARE","'DE','DELAWARE'"],
               ["FLORIDA","'FL','FLORIDA','NFL','SFL','WCF'"],
               ["GEORGIA","'GA','GEORGIA'"],
               ["HAWAII","'HI','HAWAII'"],
               ["IDAHO","'ID','IDAHO'"],
               ["ILLINOIS","'IL','ILLINOIS'"],
               ["INDIANA","'IN','INDIANA'"],
               ["IOWA","'IA','IOWA'"],
               ["KANSAS","'KS','KANSAS'"],
               ["KENTUCKY","'KY','KENTUCKY'"],
               ["LOUISIANA","'LA','LOUISIANA'"],
               ["MAINE","'ME','MAINE'"],
               ["MARYLAND","'MD','MARYLAND'"],
               ["MASSACHUSETTS","'MA','EMA','WMA','MASSACHUSETTS'"],
               ["MICHIGAN","'MI','MICHIGAN'"],
               ["MINNESOTA","'MN','MINNESOTA'"],
               ["MISSISSIPPI","'MS','MISSISSIPPI'"],
               ["MISSOURI","'MO','MISSOURI'"],
               ["MONTANA","'MT','MONTANA'"],
               ["NEBRASKA","'NE','NEBRASKA'"],
               ["NEVADA","'NV','NEVADA'"],
               ["NEW HAMPSHIRE","'NH','NEW HAMPSHIRE'"],
               ["NEW JERSEY","'NJ','NNJ','SNJ','NEW JERSEY'"],
               ["NEW MEXICO","'NM','NEW MEXICO'"],
               ["NEW YORK","'NY','ENY','NLI','NNY','WNY','NEW YORK'"],
               ["NORTH CAROLINA","'NC','NORTH CAROLINA'"],
               ["NORTH DAKOTA","'ND','NORTH DAKOTA'"],
               ["OHIO","'OH','OHIO'"],
               ["OKLAHOMA","'OK','OKLAHOMA'"],
               ["OREGON","'OR','OREGON'"],
               ["MAINE","'ME','MAINE'"],
               ["PENNSYLVANIA", "'PA','EPA','WPA','PENNSYLVANIA'"],
               ["RHODE ISLAND","'RI','RHODE ISLAND'"],
               ["SOUTH CAROLINA","'SC','SOUTH CAROLINA'"],
               ["SOUTH DAKOTA","'SD','SOUTH DAKOTA'"],
               ["TENNESSEE","'TN','TENNESSEE'"],
               ["TEXAS","'TX','TEXAS'"],
               ["UTAH","'UT','UTAH'"],
               ["VERMONT","'VT','VERMONT'"],
               ["WASHINGTON","'WA','EWA','WWA','WASHINGTON'"],
               ["WEST VIRGINIA","'WV','WEST VIRGINIA'"],
               ["WISCONSIN","'WI','WISCONSIN'"],
               ["WYOMING","'WY','WYOMING'"],
               ["ALBERTA","'AB','ALBERTA'"],
               ["BRITISH COLUMBIA","'BC','BRITISH COLUMBIA'"],
               ["MANITOBA","'MB','MANITOBA'"],
               ["NEW BRUNSWICK","'NB','NEW BRUNSWICK'"],
               ["NEWFOUNDLAND","'NL','NEWFOUNDLAND','LABRADOR'"],
               ["NOVA SCOTIA","'NS','NOVA SCOTIA'"],
               ["ONTARIO","'ON','ONS','ONN','ONTARIO'"],
               ["PRINCE EDWARD","'PE','PRINCE EDWARD'"],
               ["QUEBEC","'QC','QUEBEC'"],
               ["SASKATCHEWAN","'SK','SASKATCHEWAN'"],
               ["NORTHWEST TERRITORIES","'NT','NORTHWEST TERRITORIES'"],
               ["NUNAVUT","'NU','NUNAVUT'"],
               ["YUKON","'YT','YUKON'"] ]

class GENLabels():
    def __init__(self):
        self.AwardList = []
        self.qrz=QRZLookup('./moqputils/configs/qrzsettings.cfg')
        self.appMain()
        
    def appMain(self, AWARD):
        pass

class SHOWMELabels(GENLabels):
    def __init__(self, AWARD):
        #if __name__ == '__main__':
           self.AwardList =[]
           self.appMain(AWARD)

    def processOne(self, mydb, logid, AWARD):

        logheader = mydb.read_pquery("SELECT * from LOGHEADER WHERE ID=%s",[logid])
        tsvdata = ("%s AWARD\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%( \
                               AWARD,
                               logheader[0]['CALLSIGN'],
                               logheader[0]['OPERATORS'],
                               logheader[0]['NAME'],
                               logheader[0]['ADDRESS'],
                               logheader[0]['CITY'],
                               logheader[0]['STATEPROV'],
                               logheader[0]['ZIPCODE'],
                               logheader[0]['COUNTRY'],                               
                               logheader[0]['EMAIL']))
        return tsvdata

    def showmeDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line)) 
    
    def appMain(self, AWARD):
       csvdata = 'No Data.'
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()

       IDLIST = mydb.read_query("SELECT LOGID FROM %s WHERE QUALIFY = 1"%(AWARD))
       
       self.AwardList.append(SHOWMEHEADERS)
       for logID in IDLIST:
           #print(logID['LOGID'])
           self.AwardList.append( \
               self.processOne(mydb, logID['LOGID'],AWARD))
       self.showmeDisplay(self.AwardList)  
           
class CATEGORYLabels(GENLabels):
           
    def makeTSV(self, place, cat, logheader):
       tsvdata = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%( \
                               place,cat,
                               logheader['CALLSIGN'],
                               logheader['OPERATORS'],
                               logheader['NAME'],
                               logheader['ADDRESS'],
                               logheader['CITY'],
                               logheader['STATEPROV'],
                               logheader['ZIPCODE'],
                               logheader['COUNTRY'],
                               logheader['EMAIL']))

       return tsvdata

    def processHeader(self, mydb, place, cat, logid):
       logheader = mydb.read_pquery(\
                   "SELECT * from LOGHEADER WHERE ID=%s",[logid])

       tsvdata = self.makeTSV(place, cat, logheader[0])
       if (len(logheader[0]['OPERATORS']) > 0):
           ops = logheader[0]['OPERATORS'].split(' ')
           if  len(ops)>1:
               for op in ops:
                   try:
                       opdata = self.qrz.callsign(op.strip())
                       qrzdata=True
                   except:
                       qrzdata=False
                       logheader[0]['NAME']='NO QRZ FOR {} - {}'.format(op,len(op))
                       
                   if qrzdata:
                       #print(opdata)
                       if ('fname' in opdata) and ('name' in opdata):
                           
                           logheader[0]['NAME']=('{} {}, {}'.format(\
                                                 opdata['fname'].upper(),
                                                 opdata['name'].upper(),
                                                 op.upper()))
                       elif ('attn' in opdata) and ('name' in opdata):
                           logheader[0]['NAME']=('{} ATTN {}'.format(\
                                                 opdata['name'].upper(),
                                                 opdata['att1'].upper()))
                       elif ('name' in opdata):
                           logheader[0]['NAME']=('{}'.format(\
                                                 opdata['name'].upper()))
                       else:
                           logheader[0]['NAME']=('***NO NAME FOR {} ***'.format(\
                                                 op.upper()))
                       if('addr1' in opdata):   
                           logheader[0]['ADDRESS']=opdata['addr1'].upper()
                       else:
                           logheader[0]['ADDRESS']=''
                       if ('addr2' in opdata):    
                           logheader[0]['CITY'] = opdata['addr2'].upper()
                       else:
                           logheader[0]['CITY'] = ''
                       if('state' in opdata):
                           logheader[0]['STATEPROV'] = opdata['state'].upper()
                       else:
                           logheader[0]['STATEPROV'] = ''
                       if ('zip' in opdata):
                           logheader[0]['ZIPCODE'] = opdata['zip'].upper()
                       else:
                           logheader[0]['ZIPCODE'] = ''
                       if ('country' in opdata):    
                           logheader[0]['COUNTRY'] = opdata['country'].upper()
                       else:
                           logheader[0]['COUNTRY'] = ''
                       if ('email' in opdata):
                           logheader[0]['EMAIL'] = opdata['email'].upper()                       
                       else:                        
                           logheader[0]['EMAIL'] = ''                       
                   
                   tsvdata += '\n'+ self.makeTSV(place, cat, logheader[0])
       return tsvdata
    
           
    def processOne(self, mydb, cati):
       tsvdata = None
    
       cat = cati.upper()
       #print(cat)
       sumlist = mydb.read_pquery(\
           "SELECT * FROM SUMMARY WHERE MOQPCAT=%s "+\
           "ORDER BY (SCORE) DESC",[cat])
       if (sumlist):
           #sumlist = sumlist[0]
           tsvdata = []
           #print(sumlist)
           if (len(sumlist)>0):
               tsvdata.append(self.processHeader(mydb, 
                                         "FIRST PLACE", 
                                         cat, 
                                         sumlist[0]['LOGID']) )

           if (len(sumlist) >1):
               tsvdata.append(self.processHeader(mydb, 
                                         "SECOND PLACE", 
                                         cat, 
                                         sumlist[1]['LOGID']) )
       if ((sumlist ==None) or (len(sumlist) == 0)):
               tsvdata =['\t%s\tNO ENTRY'%(cat)]
       return tsvdata
       
    def AwardDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line)) 

    def appMain(self):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       #CATLIST = mydb.read_query("SELECT DISTINCT MOQPCAT FROM SUMMARY WHERE 1")
       self.AwardList.append(CATCOLUMNHEADERS)
       #for CAT in CATLIST:
       for CAT in AWARDLIST:
           #print(CAT['MOQPCAT'])
           #tsvdata = self.processOne(mydb, CAT['MOQPCAT'])
           tsvdata = self.processOne(mydb, CAT)
           for line in tsvdata: 
               self.AwardList.append(line)
       self.AwardDisplay(self.AwardList) 

class STATELabels(GENLabels):

    def getOne(self, mydb, place, state, IDSTG, score):

        logheader = mydb.read_pquery("SELECT * FROM LOGHEADER "+\
                                    "WHERE ID=%s",
                                    [IDSTG])


        tsvdata = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d"%( \
                               place,state,
                               logheader[0]['CALLSIGN'],
                               logheader[0]['OPERATORS'],
                               logheader[0]['NAME'],
                               logheader[0]['ADDRESS'],
                               logheader[0]['CITY'],
                               logheader[0]['STATEPROV'],
                               logheader[0]['ZIPCODE'],
                               logheader[0]['COUNTRY'],                               
                               logheader[0]['EMAIL'],
                               score))
        return tsvdata
       

    def getState(self,mydb, STATE, NAMELIST):
       CATLIST = mydb.read_query("SELECT ID "+ \
                                 "FROM LOGHEADER "+ \
                                 "WHERE LOCATION IN "+ \
                                 "(" + NAMELIST+ ")")
       if (len(CATLIST)>0):
           STRIDS =""
           for ID in CATLIST:
              STRIDS += ("'%s',"%(ID['ID']))
           STRIDS = STRIDS[:len(STRIDS)-1]
           #print(STRIDS)
           #print(CATLIST)
           SUMLIST = mydb.read_query('SELECT LOGID, SCORE '+ \
                                  'FROM SUMMARY '+ \
                                  'WHERE LOGID IN '+ \
                                  '(' + STRIDS +') '+ \
                                  'ORDER BY (SCORE) DESC')
           print(self.getOne(mydb, "FIRST PLACE",
                         STATE,
                         SUMLIST[0]['LOGID'],
                         SUMLIST[0]['SCORE']))
           if (len(SUMLIST) > 1):
               print(self.getOne(mydb, "SECOND PLACE",
                             STATE,
                             SUMLIST[1]['LOGID'],
                             SUMLIST[1]['SCORE']))
       else:
           print('\t%s\tNO ENTRY'%(STATE))

    def states(self, mydb):
       print('%s'%(STATEHEADER))
       for state in STATELIST:
           self.getState(mydb, state[0], state[1])

    def appMain(self):
       mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
       mydb.setCursorDict()
       self.states(mydb)

