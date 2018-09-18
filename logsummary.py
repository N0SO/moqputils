#!/usr/bin/python
"""
logsummary.py - Display Cabrillo header from logfile
                and print a summary of QSOs made.
"""
import datetime
import argparse
from CabrilloUtils import *

VERSION = '1.0.4'
ARGS = None


class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the log file input file name")
        return parser.parse_args()
    
class theApp():
   def __init__(self):
      if __name__ == '__main__':
         self.main()
      
   def processLog(self, logfile):
      retdata = None
      cab = CabrilloUtils()
      data = cab.readFile(logfile)
      if (data):
         retdata = self.processData(cab, data)
      else:
         print('\n\n==>No data for %s\n\n'%(logfile))
      return retdata
  
   def processData(self, cab, data):
      retdata = []
      qso = 0
      cw = 0
      ph = 0
      dg = 0
      header = cab.getCABHeader(data)
      opdata = cab.getOperatorData(header)
      for line in data:
         line = cab.packLine(line)
         for tag in cab.CABRILLOTAGS:
            if tag in line:
               if (tag == 'QSO:'):
                   lineparts = line.split(tag)
                   if (lineparts[1]):
                      line = cab.packLine(lineparts[1])
                      lineparts = line.split(' ')
                      qso += 1
                      mode = lineparts[1].upper()
                      if ('CW' in mode):
                         cw +=1
                      elif (mode in cab.PHONEMODES):
                         ph +=1
                      elif (mode in cab.DIGIMODES):
                         dg +=1
                      else:
                         print("UNDEFINED MODE: %s -- QSO data = %s"%(mode, line))
                         retdata.append("UNDEFINED MODE: %s -- QSO data = %s"%(mode, line))
                         
      for headerline in header:
         headerparts = headerline.split(':')
         if(len(headerparts) < 2): headerparts.append(' ')
         #print('%s:,%s'%(headerparts[0],headerparts[1]))
         retdata.append('%s: %s'%(headerparts[0],headerparts[1]))
      #print("CW: %d\nPH:  %d\nDIGITAL: %d\n TOTAL QSOs: %d"%(cw,ph,dg,qso))
      retdata.append("CW: %d"%(cw))
      retdata.append("PH: %d"%(ph))
      retdata.append("DIGITAL: %d"%(dg))
      retdata.append("TOTAL QSOs: %d"%(qso))
      
      return retdata
   
      
   def main(self):
      args = get_args()
      sumdata = self.processLog(args.args.inputfile)
      if (sumdata):
         for line in sumdata:
            print line

if __name__ == '__main__':
   app=theApp()
