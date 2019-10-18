#!/usr/bin/python
"""
moqpcategory  - Determine which Missouri QSO Party Award
                category a Cabrillo Format log file is in.
                
                Based on 2019 MOQP Rules
                
"""
from logsummary import *
import os

VERSION = '0.2.1' 
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

class MOQPCategory(LogSummary):

    def __init__(self, filename = None):
        if (filename):
           if (filename):
              self.appMain(filename)

    def getVersion(self):
       return VERSION

    def processLog(self, fname):
       category = None
       log = self.readFile(fname)
       if ( log ):
          if self.IsThisACabFile(log):
             headerdata = self.getCABHeader(log)
             catdata = self.getCategory(headerdata)
             category = self.determineCategory(catdata)
             qth = self.getCabArray('LOCATION:',headerdata)
             qcall, qops, qso, cw, ph, dg, vhf = self.processQSOs( log)
             category.append(qth)
             category.append(qcall)
             category.append(qops)
             category.append(cw)
             category.append(ph)
             category.append(dg)
             category.append(qso)
             category.append(vhf)
       
       return category
       
    def processLogdict(self, fname):
       """
       Read the Cabrillo log file and separate log header data
       from qso data. 
       Returns a dictionary with two elements:
          HEADER = a dictionary objject of the log header
          QSOLIST = a list dictionary objects with QSO data
          QSOSUM = a summary of the QSO statstics
                   QSOS = total number of QSOs
                   CW = number of CW QSOs
                   PH = number of PHONE QSOSs
                   DG = number of DIGITAL QSOs
                   VHF = number of VHF (>=144MHz) QSOs
       """
       log = None
       logSummary = None
       logtext = self.readFile(fname)
       if ( logtext ):
          if self.IsThisACabFile(logtext):
             log = self.getQSOdata(logtext)
             #headerdata = log[HEADER]
             #catdata = self.getCategorydict(headerdata)
             #category = self.determineCategorydict(catdata)
             qsosummary = self.processQSOList(log['QSOLIST'])
             logSummary = dict()
             logSummary['HEADER'] = log['HEADER']
             logSummary['QSOLIST'] = log['QSOLIST']
             logSummary['QSOSUM'] = qsosummary

       return logSummary

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
          opmode = 'PHONE'
       elif (temp == 'CW'):
          opmode = 'CW'
       elif (temp == 'MIXED'):
          opmode = 'MIXED'
       if (opmode in 'PHONE CW MIXED'):
          if (gen_category[10] > 0):
             opmode += '+DIG'
          if (gen_category[12] > 0):
             opmode += '+VHF'
       moqp_category.append(opmode)
          
       temp = gen_category[4].upper().strip()
       opovly = ''
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
          if ( 'CHECKLOG' in opcat):
             moqp_category[0] = 'CHECKLOG'
             moqp_category[1] = ''
             moqp_category[2] = ''
             moqp_category[3] = ''
             moqp_category[4] = ''
             moqp_category[5] = ''
             break
          

       #print ('%s %s %s %s %s OVERLAY:%s'%(qth, catstation, opcat, power, opmode, opovly))
          
       #print moqp_category
       
       #moqp_category
       
       return moqp_category

    def determineMOQPCatdict(self, gen_category):
       moqp_category = dict()
       compstring = gen_category['LOCATION'].strip()
       if(compstring in INSTATE):
          moqp_category['LOCATION'] = 'MISSOURI'
       elif (compstring in US):
          moqp_category['LOCATION'] = 'US'
       elif (compstring in CANADA):
          moqp_category['LOCATION'] = \
                         ('CANADA: %s'%(gen_category['LOCATION']))
       elif (compstring in DX):
          moqp_category['LOCATION'] = 'DX'
       else:
          moqp_category['LOCATION'] = \
            'UNDEFINED OP CATEGORY:%s'%(gen_category['LOCATION'])
            
       compstring = gen_category['CATEGORY-STATION'].strip()
       moqp_category['CATEGORY-STATION'] = \
           ('UNDEFINED STATION CATEGORY:%s' \
                             %(gen_category['CATEGORY-STATION']))
       #print('compstring =%s'%(compstring))
       if (compstring in STATIONS):
           if (compstring == 'FIXED'):
               moqp_category['CATEGORY-STATION'] = 'FIXED'
           elif ( (compstring == 'MOBILE') \
               or (compstring == 'ROVER') \
               or compstring == 'PORTABLE'):
               moqp_category['CATEGORY-STATION'] = 'MOBILE'
           elif (compstring == 'EXPEDITION'):
               moqp_category['CATEGORY-STATION'] = 'EXPEDITION'
           elif (compstring == 'SCHOOL'):
               moqp_category['CATEGORY-STATION'] = 'SCHOOL'
           
       compstring = gen_category['CATEGORY-OPERATOR'].strip()
       moqp_category['CATEGORY-OPERATOR'] = \
          ('UNDEFINED OP CATEGORY:%s'% \
                 (gen_category['CATEGORY-OPERATOR']))
       if (compstring == 'SINGLE-OP'):
          moqp_category['CATEGORY-OPERATOR']  = 'SINGLE-OP'
       elif (compstring == 'MULTI-OP'):
          moqp_category['CATEGORY-OPERATOR'] = 'MULTI-OP'
       elif (compstring == 'CHECKLOG'):
          moqp_category['CATEGORY-OPERATOR'] = 'CHECKLOG'
       
       compstring = gen_category['CATEGORY-POWER'].strip()
       moqp_category['CATEGORY-POWER'] = \
         ('UNDEFINED STATION POWER ENTRY:%s'% \
                           (gen_category['CATEGORY-POWER']))
       if (compstring == 'LOW' \
                 or compstring == 'HIGH' \
                 or compstring == 'QRP'):
           moqp_category['CATEGORY-POWER'] = compstring
    
       compstring = gen_category['CATEGORY-MODE'].strip()
       moqp_category['CATEGORY-MODE'] = \
            ('UNDEFINED STATION MODE ENTRY:%s'% \
                              (gen_category['CATEGORY-MODE']))
       if (compstring == 'PH' \
                     or compstring == 'SSB'):
          moqp_category['CATEGORY-MODE'] = 'PHONE'
       elif (compstring == 'CW'):
          moqp_category['CATEGORY-MODE'] = 'CW'
       elif (compstring == 'MIXED'):
          moqp_category['CATEGORY-MODE'] = 'MIXED'
       if (compstring in 'PHONE CW MIXED'):
          moqp_category['CATEGORY-OVERLAY'] = ''
       if (gen_category['CATEGORY-OVERLAY'].strip() == 'ROOKIE'):
          moqp_category['CATEGORY-OVERLAY']  = 'ROOKIE'                         
       
       return moqp_category
       
       
    def csvHeader(self):
       hdata = (',,,CATEGORIES FROM THE LOG FILE,,,,,\n')
       hdata += ('STATION,OPS,MOQP CATEGORY,STATION,OPERATOR,POWER,MODE,LOCATION,OVERLAY,CW QSO,PH QSO,RY QSO,TOTAL,VHF QSO\n')
       return hdata
       
    def exportcsvline(self, gen, moqp):
       hdata = ( '%s,%s,%s %s %s %s %s %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(gen[6], 
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
                        gen[11],
                        gen[12]) )
                        
       return hdata 
       
    """
    This method processes a single file passed in filename
    If the Headers option is false, it will skip printing the
    csv header info.
    """
    def exportcsvfile(self, filename, Headers=True):
       csvdata = ''
       gencat = self.processLog(filename)
       if (gencat):
          moqpcat = self.determineMOQPCat(gencat)
          if (Headers): 
             csvdata = self.csvHeader()
          csvdata += self.exportcsvline(gencat, moqpcat)
       else:
          csvdata = ('File %s does not exist or is not in CABRILLO format.'%filename)
       return csvdata
          
        
    """
    This method processes a single file passed in filename
    If the Headers option is false, it will skip printing the
    csv header info.
    
    Using dictionary objects
    """
    def exportcsvfiledict(self, filename, Headers=True):
       logsummary = self.processLogdict(filename)
       if (logsummary):
          #catdata = self.getCategorydict(logsummary['HEADER'])
          #gencat  = self.determineCategorydict(catdata)
          
          #print('HEADER = %s\nCATDATA = %s\nGENCAT = %s\n'%(logsummary['HEADER'], catdata, gencat))
          
          moqpcat = self.determineMOQPCatdict(logsummary['HEADER'])
          if(logsummary['QSOSUM']['DG'] > 0):
              moqpcat['CATEGORY-MODE'] += '+DG'
          if(logsummary['QSOSUM']['VHF'] > 0):
              moqpcat['CATEGORY-MODE'] += '+VHF'
          #logsummary.update(moqpcat)
          fullSummary = dict()
          fullSummary['HEADER'] = logsummary['HEADER']
          fullSummary['QSOSUM'] = logsummary['QSOSUM']
          fullSummary['MOQPSUM'] = moqpcat
          fullSummary['QSOLIST'] = logsummary['QSOLIST']
          #if (Headers): 
          #   csvdata = self.csvHeader()
          #csvdata += self.exportcsvline(gencat, moqpcat)
       else:
          print('File %s does not exist or is not in CABRILLO format.'%filename)
       return fullSummary
 
    """
    This method processes all files in the passed in pathname
    """
    def exportcsvflist(self, pathname):
       csvdata = self.csvHeader()
       for (dirName, subdirList, fileList) in os.walk(pathname, topdown=True):
          if (fileList != ''): 
             for fileName in fileList:
                fullPath = ('%s/%s'%(dirName, fileName))
                csvdata += self.exportcsvfile(fullPath, False)
       return csvdata
 
    def appMain(self, pathname):
       csvdata = 'Nothing.'
       if (os.path.isfile(pathname)):
          csvdata = self.exportcsvfile(pathname)
       else:
          csvdata = self.exportcsvflist(pathname)
       print csvdata
       
if __name__ == '__main__':
   args = get_args()
   app = MOQPCategory(args.args.inputpath.strip())


