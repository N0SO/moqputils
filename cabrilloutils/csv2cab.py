#!/usr/bin/python
"""
csv2cab - 
Process a .csv file from MSExcel (or other spreadsheets)
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
Update History:
* Mon Apr 30 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.1 - Initial release
* Tue May 01 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.2 - 2018-05-01 
- Made csv2cab callable from another module. The stand-alone
- command line functions still work too.
* Thu Oct 10 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.3 - 2019-10-10
- Made csv2cab inherit from CabrilloUtils.
- Make module CSVtoCAB with classes csv2CAB and ui.
- Added csv2cab script that will do both command line and GUI.
* Sun Apr 02 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V2.0.0 - Updated to use new developmet module pathing methods.
-          Also added code to remove all the  QSO column header
-          lines and the extra QSO: ,,,,, lines present in our
-          MOQP_log.xls(x) spreadsheet.
"""
import datetime
import argparse
import sys
import string
from os.path import basename
from CabrilloUtils import *

VERSION = '1.0.3'
TAGLINE = 'SOAPBOX: This file processed by the csv2cab utility.\n'
ARGS = None

class csv2CAB(CabrilloUtils):
   def __init__(self, csvfilename = None):
      if (csvfilename):
         self.main(csvfilename)
         
   def __version__(self):
        return VERSION

         
   def readcsvcabFile(self, csvfileName):
      """Read CSV file and return data. If this file is
         not a CABRILLO format file, return None"""

      csvdata = self.readFile(csvfileName)
      if (csvdata):
         lc = 0
         for line in csvdata:
            lc += 1
            #print('cab2csv_db_4: line=', line, lc)
            if (self.IsplainText(line) == False):
               for c in line:
                  #print('cab2csv_db_5: c=', c, lc)
                  if (not(c in string.printable)):
                     print(string.printable)
                     print("I don't line character %s in line %d "%(c, lc))
                     csvdata = None
               break
      else:
          print('File %s is empty or does not exist.'%(csvfileName))
      return csvdata
      
   def processLine(self, iline):
      newline = None
      cabparts =  iline.split(':',1)
      if(len(cabparts)>1):
         line = cabparts[1].replace(',',' ')           #Replace commas
         #for tag in self.CABRILLOTAGS:                 #Skip any line without a CAB tab
         if (cabparts[0] in self.CABRILLOTAGS):
               newline = r""
               newline = cabparts[0] +':'+ self.packLine(line)
               if newline == 'QSO:':                  #Skip blank QSO: lines
                  newline = None
                  #break
      #print('newline = ',newline)
      return newline
         
   def processcsvData(self, csvdata):
      #cab = CabrilloUtils()
      tag_needed = True
      cabdata = r""
      
      for line in csvdata:
         newline = self.processLine(line)
         if (newline):                              #Skip invalid lines
            if (tag_needed):                      
               if ('SOAPBOX:' in newline):          #Flag this file as processed by me
                  cabdata += TAGLINE
                  tag_needed = False                #Only insert tag once
            cabdata += newline +'\n' 
      return cabdata
      
   def main(self, csvfilename):
      cabdata = r""
      csvdata = self.readcsvcabFile(csvfilename)

      #print('csv2cab_db_1: csvdata = %s'%(csvdata))

      if (csvdata == None):
         print('File %s is not a Cabrillo Format File.'%(csvfilename))
      else:
         cabdata = self.processcsvData(csvdata)
         print(cabdata)
  
         print('Writing .log file %s.log ...'%(csvfilename))      
         cabfile = basename(csvfilename) + ".log"
         with open(cabfile,'w') as f:
            f.write(cabdata)

      return cabdata

      
     

if __name__ == '__main__':
   app = csv2CAB()
   print ('Classname: %s Version: %s'%(app.__class__.__name__,
                                       app.__version__()))
