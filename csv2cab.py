#!/usr/bin/python
"""
csv2cab - Process a .csv file from MSExcel (or other spreadsheets)
          and make it a .CAB file by removing all commas, blank
          QSO: lines, etc. Usually used to clean a file submitted
          using AA0CL's MOQP_log.xls form.
          
          Usage:
             python csv2cab.py -i logfilename.csv
             
          This will create a file named logfile.csv.log that should
          be in the same folder as the source.
          
          Starting with V1.0.2, can also be called from inside your 
	  code:
	    from csv2cab import *
	    mycab = csv2cab('csvcabfilename')
	               
	    --or-- if you want to manipulate the cab data:
	    mycab = csv2cab()
	    mycsvdata = mycab.readcsvcabFile(csvcabfilename)
	    mycabdata = mycab.processcsvData(mycsvdata)

          
          This program inserts whatever is in the TAGLINE constant
          as the first line of the SOAPBOX: fields
          
          V1.0.1 - Initial release
          
          V1.0.2 - 2018-05-01 
          Made csv2cab callable from another module. The stand-alone
          command line functions still work too.
	  
	  V1.0.3 - 2019-09-01
	  Making this a child class of Cabrilloutils.
          
"""
import datetime
import argparse
import sys
import string
from os.path import basename
from CabrilloUtils import CabrilloUtils

VERSION = '1.0.3'
TAGLINE = 'SOAPBOX: This file processed by the csv2cab utility.\n'
ARGS = None

class csv2CAB(CabrilloUtils):
   def __init__(self, csvfilename = None):
      if (csvfilename):
         self.main(csvfilename)
         
   def readcsvcabFile(self, csvfileName):
      """Read CSV file and return data. If this file is
         not a CABRILLO format file, return None"""
      csvdata = self.readFile(csvfileName)
      
      if (csvdata):
         if (self.IsThisACabFile(csvdata) == False):
            csvdata = None
      
      return csvdata
      
      
   def processLine(self, line):
      newline = None
      for tag in self.CABRILLOTAGS:                 #Skip any line without a CAB tab
         if (tag in line):
            newline = r""
            newline = self.packLine(line)
            if newline == 'QSO:':                  #Skip blank QSO: lines
               newline = None
            break
      return newline
         
   def processcsvData(self, csvdata):
      tag_needed = True
      cabdata = r""
      
      for line in csvdata:
         newline = self.processLine(line)
         if (newline):                              #Skip invalid lines
            if (tag_needed):                      
               if ('SOAPBOX:' in newline):          #Flag this file as processed by me
                  cabdata += TAGLINE
                  tag_needed = False                #Only insert tag once
            cabdata += newline.decode('utf').encode('ascii', 'replace')+'\n'
      return cabdata
      
   def main(self, csvfilename):
      cabdata = r""
      csvdata = self.readcsvcabFile(csvfilename)
 
      if (csvdata == None):
         print('File %s is not a Cabrillo Format File.'%(csvfilename))
      else:
         cabdata = self.processcsvData(csvdata)
         cabfile = basename(csvfilename) + ".log"
         with open(cabfile,'w') as f:
            f.write(cabdata)

      return cabdata

      
class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(description = \
	   'Version '+VERSION + '-- \n'+ \
	   'Process a .csv file from MSExcel (or other ' +\
	   'spreadsheets) and make it a .CAB file by '+ \
	   'removing all commas, blank QSO: lines, etc. ' +\
	   'Usually used to clean a file submitted using ' +\
	   'AA0CL\'s MOQP_log.xls form.')
        parser.add_argument('-v', '--version', action='version', 
	                    version = VERSION)
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the log file input file name")
        return parser.parse_args()

class theAPP():
   def __init__(self):
      self.main()

   def main(self):
      args = get_args()
      csv2CAB(args.args.inputfile.strip())

if __name__ == '__main__':
   app=theAPP()
