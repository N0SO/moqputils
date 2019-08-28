#!/usr/bin/python
"""
logsummary.py - Display Cabrillo header from logfile
                and print a summary of QSOs made.
"""
import datetime
import argparse
from CabrilloUtils import *

VERSION = '1.0.7'
ARGS = None


class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(description = \
            'Display Cabrillo header from logfile and print ' + \
            'a summary of QSOs made.')
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the log file input file name")
        return parser.parse_args()
    
class LogSummary(CabrilloUtils):
   """
   LogSummary inherits methods from parent class CalbrilloUtils.
   """
   def __init__(self):
      if __name__ == '__main__':
         self.main()
         
   def _get_version(self):
      return VERSION
      
   def processLog(self, logfile):
      retdata = None
      #cab = CabrilloUtils()
      data = self.readFile(logfile)
      if (data):
         retdata = self.processData( data)
      else:
         print('\n\n==>No data for %s\n\n'%(logfile))
      return retdata
      
   def processQSOs(self,  data):
      """
      Process and return QSO data only
      """
      call = None
      ops = None
      qso = 0
      cw = 0
      ph = 0
      vhf = 0
      dg = 0
      for line in data:
         line = self.packLine(line)
         for tag in self.CABRILLOTAGS:
            if tag in line:
               if (tag == 'QSO:'):
                   lineparts = line.split(tag)
                   if (lineparts[1]):
                      line = self.packLine(lineparts[1])
                      lineparts = line.split(' ')
                      qso += 1
                      tfreq = lineparts[0]
                      try:
                         freq = float(tfreq)
                      except:
                         freq = 0
                      if ((freq >= 144000.0) or (tfreq in self.VHFFREQ) ):
                         vhf += 1
                      mode = lineparts[1].upper()
                      if ('CW' in mode):
                         cw +=1
                      elif (mode in self.PHONEMODES):
                         ph +=1
                      elif (mode in self.DIGIMODES):
                         dg +=1
                      else:
                         print("UNDEFINED MODE: %s -- QSO data = %s"%(mode, line))
                      #print ('Frequency = %.2f, vhf count = %d, digi count =%d'%(freq, vhf, dg))
               elif (tag == 'CALLSIGN:'):
                  call = self.getCabstg('CALLSIGN:',line)
               elif (tag == 'OPERATORS:'):
                  ops = self.getCabstg('OPERATORS:',line)
      return call, ops, qso, cw, ph, dg, vhf

   def processData(self,  data):
      retdata = []
      qso = 0
      cw = 0
      ph = 0
      dg = 0
      header = self.getCABHeader(data)
      opdata = self.getOperatorData(header)
      catdata = self.determineCategory(header)
      call, ops, qso, cw, ph, dg, vhf = self.processQSOs( data)
      retdata.append( "LOG FILE REPORT FOR STATION %s" \
                          %(self.getCabArray('CALLSIGN:',header)) )
      retdata.append( "CONTEST: %s\n" \
                          %(self.getCabArray('CONTEST:',header).upper()) )
                          
      retdata.append('SUBMITTED BY:')
      retdata.append('%s %s' \
         %(self.getCabArray('NAME:',header), 
           self.getCabArray('EMAIL:', header)) )                   
      retdata.append('%s'%(self.getCabArray('ADDRESS:',header)) )
      retdata.append('%s'%(self.getCabArray('ADDRESS-CITY:',header)) )
      retdata.append('%s'%(self.getCabArray('ADDRESS-STATE-PROVINCE:',header)) )
      retdata.append('%s\n'%(self.getCabArray('ADDRESS-ADDRESS-POSTALCODE: ',header)) )
    
      retdata.append('OPERATORS:%s\n'%(self.getCabArray('OPERATORS:',header)) )
                            
      retdata.append( \
      "Category: %s STATION, %s, %s MODE, %s POWER\nOverlay: %s\n" \
                                                     %(catdata[0], \
                                                       catdata[1], \
                                                       catdata[3], \
                                                       catdata[2], \
                                                       catdata[4]))
      retdata.append("QSO Summary:\nCW: %d"%(cw))
      retdata.append("PH: %d"%(ph))
      retdata.append("DIGITAL: %d"%(dg))
      retdata.append("VHF: %d"%(vhf))
      retdata.append("TOTAL QSOs: %d"%(qso))
     
      return retdata
   
      
   def main(self):
      args = get_args()
      sumdata = self.processLog(args.args.inputfile)
      if (sumdata):
         for line in sumdata:
            print line

if __name__ == '__main__':
   app=LogSummary()
   print( 'Version %s exiting...'%(app._get_version()) )
