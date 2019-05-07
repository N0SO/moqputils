#!/usr/bin/python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
                
"""
from CabrilloUtils import *
from logsummary import *


VERSION = '0.0.2' 

INSTATE = 'MO MISSOURI'

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT'

STATIONS = 'FIXED MOBILE PORTABLE ROVER EXPEDITION HQ SCHOOL'

MODES = 'SSB USB LSB FM PH CW RTTY DIG MIXED'

OVERLAY = 'ROOKIE'

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
       sumqs = theApp()
       log = cab.readFile(fname)
       if ( log ):
          if cab.IsThisACabFile(log):
             headerdata = cab.getCABHeader(log)
             catdata = cab.getCategory(headerdata)
             category = cab.determineCategory(catdata)
             qth = cab.getCabArray('LOCATION:',headerdata)
             qcall, qops, qso, cw, ph, dg = sumqs.processQSOs(cab, log)
             category.append(qth)
             category.append(qcall)
             category.append(qops)
             category.append(cw)
             category.append(ph)
             category.append(dg)
             category.append(qso)
             
       self.category = category
       return category
       
    def determineMOQPCat(self, filename):
       ret_vals = []
       gen_category = self.processLog(filename)
       temp = gen_category[5].upper().strip()
       qth = ('%s UNDEFINED QTH:'%(temp))
       if(temp in INSTATE):
          qth = 'MISSOURI'
       elif (temp in US):
          qth = 'US'
       elif (temp in CANADA):
          qth = ('CANADA %s'%(temp))
       elif (temp in DX):
          qth = 'DX'
       ret_vals.append(qth)

       temp = gen_category[0].upper().strip()
       catstation = ('UNDEFINED STATION CATEGORY:%s'%(temp))
       if (temp in STATIONS):
		   if (temp == 'FIXED'):
			   catstation = 'FIXED'
		   elif ( (temp == 'MOBILE') or (temp == 'ROVER') or temp == 'PORTABLE'):
			   catstation = 'MOBILE'
		   elif (temp == 'EXPEDITION'):
			   catstation = 'EXPEDITION'
		   elif (temp == 'SCHOOL'):
			   catstation = 'SCHOOL'
       ret_vals.append(catstation)
		   
           
       temp = gen_category[1].upper().strip()
       opcat = ('UNDEFINED OP CATEGORY:%s'%(temp))
       if (temp == 'SINGLE-OP'):
          opcat  = 'SINGLE-OP'
       elif (temp == 'MULTI-OP'):
          opcat = 'MULTI-OP'
       elif (temp == 'CHECKLOG'):
          opcat = ('CHECKLOG')
       ret_vals.append(opcat)
       
       temp = gen_category[2].upper().strip()
       power = ('UNDEFINED STATION POWER ENTRY:%s'%(temp))
       if (temp == 'LOW' or temp == 'HIGH' or temp == 'QRP'):
           power = ('%s POWER'%(temp))
       ret_vals.append(power)
    
       temp = gen_category[3].upper().strip()
       opmode = ('UNDEFINED STATION MODE ENTRY:%s'%(temp))
       if (temp == 'PH' or temp == 'SSB'):
          opmode = 'SSB'
       elif (temp == 'CW'):
          opmode = 'CW'
       elif (temp == 'MIXED'):
          opmode = 'MIXED'
       ret_vals.append(opmode)
          
       temp = gen_category[4].upper().strip()
       opovly = ('UNDEFINED OP OVERLAY:%s'%(temp))
       if (temp == 'ROOKIE'):
          opovly  = 'ROOKIE'
       ret_vals.append(opovly)

       #print ('%s %s %s %s %s OVERLAY:%s'%(qth, catstation, opcat, power, opmode, opovly))
          
       #print ret_vals
       
       return ret_vals
              
       
if __name__ == '__main__':
   app = MOQPCategory('../../Ham/BEARS/moqp/moqp2019/processedlogs/K0R.LOG')
   print ('Missouri QSO Party Log Categorizer V %s'%(app.getVersion()))
   print ('Station: %s    Operators: %s'%(app.category[6], app.category[7]))
   print app.category


