#!/usr/bin/python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
                
"""
from CabrilloUtils import *
from logsummary import *
import os
import argparse


VERSION = '0.0.3' 
FILELIST = './'
ARGS = None


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

ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputpath", default=FILELIST,
            help="Specifies the path to the folder that contains the log files to summarize.")
        return parser.parse_args()


class MOQPCategory():

    #category = None
    
    #moqp_category = None

    def __init__(self, filename = None):
        if (filename):
           self.appMain(filename)

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
             
       return category
       
    def determineMOQPCat(self, gen_category):
       moqp_category = []
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
       moqp_category.append(qth)

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
       moqp_category.append(catstation)
		   
           
       temp = gen_category[1].upper().strip()
       opcat = ('UNDEFINED OP CATEGORY:%s'%(temp))
       if (temp == 'SINGLE-OP'):
          opcat  = 'SINGLE-OP'
       elif (temp == 'MULTI-OP'):
          opcat = 'MULTI-OP'
       elif (temp == 'CHECKLOG'):
          opcat = ('CHECKLOG')
       moqp_category.append(opcat)
       
       temp = gen_category[2].upper().strip()
       power = ('UNDEFINED STATION POWER ENTRY:%s'%(temp))
       if (temp == 'LOW' or temp == 'HIGH' or temp == 'QRP'):
           power = ('%s POWER'%(temp))
       moqp_category.append(power)
    
       temp = gen_category[3].upper().strip()
       opmode = ('UNDEFINED STATION MODE ENTRY:%s'%(temp))
       if (temp == 'PH' or temp == 'SSB'):
          opmode = 'SSB'
       elif (temp == 'CW'):
          opmode = 'CW'
       elif (temp == 'MIXED'):
          opmode = 'MIXED'
       moqp_category.append(opmode)
          
       temp = gen_category[4].upper().strip()
       opovly = ('UNDEFINED OP OVERLAY:%s'%(temp))
       if (temp == 'ROOKIE'):
          opovly  = 'ROOKIE'
       elif (temp == ''):
          opovly = ''
       moqp_category.append(opovly)
       
       for element in moqp_category:
          if ('UNDEFINED' in element):
             moqp_category[0] = 'UNABLE TO DETERMINE'
             moqp_category[1] = ''
             moqp_category[2] = ''
             moqp_category[3] = ''
             moqp_category[4] = ''
             moqp_category[5] = ''
             break
          

       #print ('%s %s %s %s %s OVERLAY:%s'%(qth, catstation, opcat, power, opmode, opovly))
          
       #print moqp_category
       
       moqp_category
       
       return moqp_category
       
    def csvHeader(self):
       print (',,,CATEGORIES FROM THE LOG FILE,,,,,')
       print ('STATION,OPS,MOQP CATEGORY,STATION,OPERATOR,POWER,MODE,LOCATION,OVERLAY,PH Qs,CW Qs,DIGI,TOTAL')
       
    def exportcsvline(self, gen, moqp):
       print ('%s,%s,%s %s %s %s %s %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(gen[6], 
                        gen[7], 
                        moqp[0],
                        moqp[1],
                        moqp[2],
                        moqp[3],
                        moqp[4],
                        moqp[5],
                        gen[0],
                        gen[1],
                        gen[2],
                        gen[3],
                        gen[5],
                        gen[4], 
                        gen[8], 
                        gen[9], 
                        gen[10], 
                        gen[11] 
                        ))
       
    def exportcsvfile(self, filename, Headers=True):
       gencat = self.processLog(filename)
       if (gencat):
          moqpcat = self.determineMOQPCat(gencat)
          if (Headers): self.csvHeader()
          self.exportcsvline(gencat, moqpcat)
       else:
          print ('File %s does not exist or is not in CABRILLO format.'%filename)
          
    def exportcsvflist(self, pathname):
       self.csvHeader()
       for (dirName, subdirList, fileList) in os.walk(pathname, topdown=True):
          #print ('dirName =%s, subdirList =%s, fileList=%s'%(dirName,
          #                                                subdirList,
          #                                                fileList))
          if (fileList != ''): 
             for fileName in fileList:
                fullPath = ('%s/%s'%(dirName, fileName))
                self.exportcsvfile(fullPath, False)
 
 
    def appMain(self, pathname):
       if (os.path.isfile(pathname)):
          self.exportcsvfile(pathname)
       else:
          self.exportcsvflist(pathname)
       
if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())


