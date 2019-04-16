#!/usr/bin/python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
                
"""
from CabrilloUtils import *

VERSION = '0.0.1' 

INSTATE = 'MO MISSOURI'

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT'

US = 'CT EMA ME NH RI VT WMA ENY NLI NNJ NNY SNJ WNY DE EPA MDC WPA '
US += 'AL GA KY NC NFL SC SFL WCF TN VA PR VI AR LA MS NM NTX OK STX '
US+= 'WTX EB LAX ORG SB SCV SDG SF SJV SV PAC AZ EWA ID MT NV OR UT '
US+= 'WWA WY AK MI OH WV IL IN WI CO IA KS MN NE ND SD'

DX = 'DX'

class MOQPCategory():

    category = None

    def __init__(self, filename = None):
        if (filename):
           self.determineMOQPCat(filename)

    def getVersion(self):
       return VERSION

    def processLog(self, fname):
       category = None
       cab = CabrilloUtils()
       log = cab.readFile(fname)
       if ( log ):
          if cab.IsThisACabFile(log):
             headerdata = cab.getCABHeader(log)
             catdata = cab.getCategory(headerdata)
             category = cab.determineCategory(catdata)
             qth = cab.getCabArray('LOCATION:',headerdata)
             category.append(qth)
       self.category = category
       return category
       
    def determineMOQPCat(self, filename):
       gen_category = self.processLog(filename)
          temp = gen_category[5].upper()
          if(temp in INSTATE):
              qth = 'MISSOURI'
          elif (temp in US):
              qth = 'US'
          elif (temp in CANADA):
              qth = ('CANADA %s'%(temp))
          elif (temp in DX):
              qth = 'DX'
          else:
              qth = ('%s UNKNOWN QTH'%(temp))
              
              
              
       
if __name__ == '__main__':
   app = MOQPCategory('../../Ham/BEARS/moqp/moqp2019/processedlogs/K0R.LOG')
   print app.category
   print app.getVersion()


