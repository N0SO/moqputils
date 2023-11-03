#!/usr/bin/python
"""
MOQPMults    - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file for the ARRL Missouri QSO Party.
               Inherits from ContestMults() class.
Update History:
* Sat Feb 22 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

from cabrilloutils.contestmults import *
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *

VERSION = '0.0.2'

COUNTYLIST = ['shared/multlists/Countylist.csv']

COLUMNHEADERS = 'COUNTY (ABREV)\tQSO COUNT\tCW\tPH\tDIG'

PHONEMODES = 'PH SSB LSB USB FM DV'
DIGIMODES = 'RY RTY RTTY FSK AFSK PSK PSK31 PSK64 DIGU DIGL DG FT8'


class MOQPDBCountyCount(ContestMults):
    def __init__(self, callsign=None):
       self.mults = self.readmultlists(COUNTYLIST)
       if (callsign):
           self.appMain(callsign)

    def create_mult_dict(self, indexList):
       multDict = dict()
       #print(indexList)
       for i in indexList:
           if ('#US States' in i):
               break # Stop at end of MO counties list
           if (i[0] != '#'): # Skip comment lines
               iparts = i.split(',')
               multkey = str(iparts[1].rstrip().lstrip())
               multname = str(iparts[0].rstrip())
               #print(iparts, multkey, multname)
               multDict[multkey] = { 'FULLNAME' : multname,
                                     'COUNT' :  0 }
       #print(multDict)
       return multDict

    def setMult(self, mult):
       retval = False
       if (mult in self.mults):
          self.mults[mult]['COUNT'] += 1
          retval = True
       return retval

    def getMultList(self):
        returnList = []
        for multname in self.mults:
            returnList.append(('%s'%(multname)))
        return returnList

class MOQPDBCountyCountRpt():
    def __init__(self, validqsos):
       self.appMain()
    
    def processAll(self, mydb):
        Total = 0
        statList =[]
        query = "SELECT * FROM `mocounties`"
        cntylist = mydb.read_query(query)
        for cnty in cntylist:
            result = self.processOne(mydb, cnty['code'])
            result.CntyID = cnty['ID']
            result.Name = cnty['name']
            result.Code = cnty['code']
            Total += result.qsosum()
            statList.append(result)
            
        return statList
            
    def processOne(self, mydb, county):
        countystat = countyStats()
        querystg = """SELECT * FROM `QSOS` WHERE (VALID=1 and 
                      (MYQTH='{}' or URQTH='{}'))"""\
                      .format(county, county)
        qsolist = mydb.read_query(querystg)
        
        if (qsolist):
            countystat.Total = len(qsolist)
            for qso in qsolist:
                if ('CW' in qso['MODE']):
                    countystat.CW +=1
                elif (qso['MODE'] in PHONEMODES):
                    countystat.PH +=1
                elif (qso['MODE'] in DIGIMODES):
                    countystat.DI +=1
            
        return countystat

    def makeTSV(self, countyData):
        tsvData = [COLUMNHEADERS]
        counties = list(countyData['CW'].getMultList())
        for county in counties:
           qsototal = countyData['CW'].mults[county]['COUNT'] +\
                      countyData['PH'].mults[county]['COUNT'] +\
                      countyData['DI'].mults[county]['COUNT']
           tsvData.append('{} ({})\t{}\t{}\t{}\t{}'.format(\
                            countyData['CW'].mults[county]['FULLNAME'], 
                            county,
                            qsototal,
                            countyData['CW'].mults[county]['COUNT'],
                            countyData['PH'].mults[county]['COUNT'],
                            countyData['DI'].mults[county]['COUNT']))
        return tsvData
 
    def altmakeTSV(self, statData):
        tsvData=[COLUMNHEADERS]
        newData = sorted(statData, key=lambda countyStats: countyStats.Total, reverse=True)
        for county in newData:
            tsvData.append(county.makeTSV()) 
        return tsvData
        
    def altdisplayTSV(self, statData):
        newData = sorted(statData, key=lambda countyStats: countyStats.Total, reverse=True)
        print(COLUMNHEADERS)
        for county in newData:
            print(county.makeTSV())       
 
    def displayTSV(self, tsvData):
        for line in tsvData:
            print(line)

    def appMain(self):
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()
        countyData = self.processAll(mydb)
        tsvData = self.altmakeTSV(countyData)
        self.displayTSV(tsvData)

class HTML_CountyCntRpt(MOQPDBCountyCountRpt):

    def displayTSV(self, tsvData):

        from htmlutils.htmldoc import htmlDoc
        d = htmlDoc()
        d.openHead('{} Missouri QSO Party QSOs per County'.format(YEAR),
                        './styles.css')
        d.closeHead()
        d.openBody()
        d.addTimeTag(prefix='Report Generated On ', 
                            tagType='comment') 

        d.add_unformated_text(\
                """<h2 align='center'>{} Missouri QSO Party QSOs per County</h2>
                """.format(YEAR))
            
        d.addTable(tdata=d.tsvlines2list(tsvData),
                  header=True,
                  caption='<h3>Missouri County QSOs</h3>')
        d.closeBody()
        d.closeDoc()

        d.showDoc()
        d.saveAndView('countyqsocounts.html')

class countyStats():
    def __init__(self, Name='', Code = '', CntyID = None, 
                                CW=0, PH=0, DI=0, Total=0):
        self.Name = Name
        self.Code = Code
        self.CID = CntyID
        self.CW = CW
        self.PH = PH
        self.DI = DI
        self.Total = Total
    
    def __repr__(self):
        return repr((self.Name, self.CW, Self.PH, self.DI, self.Total))
    
    def qsosum(self):
        self.Total = self.CW + self.PH + self.DI
        return self.Total
        
    def __dofmt(self, fmt):
        return (fmt.format(self.Name,
                            self.Code,
                            self.Total,
                            self.CW, 
                            self.PH, 
                            self.DI))
 
    def makeTSV(self):
        fmt = '{} ({})\t{}\t{}\t{}\t{}'
        return(self.__dofmt(fmt))

        
    
  
