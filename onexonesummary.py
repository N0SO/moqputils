#!/usr/bin/python
"""
onexonesummary.py - exports a summary of all 1x1 SE staions
                    for status
"""
import datetime
import argparse
from CabrilloUtils import *

VERSION = '1.0.2'
FILELIST = './'
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

class theApp():
   def __init__(self):
      self.main()

   def exportcsv(self, data):
      #print ('Length of data is %s'%(len(data)))
      columns = len(data)
      for row in range(0,7):
          self.exportrow(row, columns, data)
          if (row == 1):
             # Add VERIFY column
             print('LOG VERIFIED')
          
   def exportrow(self,row, maxcolumn, data):
      TAGS = ['STAT\\1X1','OPs','CW QSOs','PH QSOs', 'DIGITAL QSOs', 'TOTAL QSOs','VHF']
      #maxcolumn = count-1
      for column in range(0, maxcolumn):
         if (column == 0):
            print TAGS[row],
         print ',',data[column][row],
      print

   def stripCallsign(self,callsign):
      """Strips everything after a / or - from a callsign string"""
      call = callsign
      splitchar = None
      if ('/' in callsign): splitchar = '/'
      elif ('-' in callsign): splitchar = '-'
      if (splitchar):
         temp = callsign.split(splitchar)
         call = temp[0]
      call = call.strip()
      call = call.lstrip()
      return call

   def main(self):
      summary = [['K0S',' ','0','0','0','0','0'],
                 ['K0H',' ','0','0','0','0','0'],
                 ['K0O',' ','0','0','0','0','0'],
                 ['K0W',' ','0','0','0','0','0'],
                 ['K0M',' ','0','0','0','0','0'],
                 ['K0E',' ','0','0','0','0','0'],
                 ['K0I',' ','0','0','0','0','0'],
                 ['K0R',' ','0','0','0','0','0'],
                 ['K0U',' ','0','0','0','0','0'],
                 ['N0S',' ','0','0','0','0','0'],
                 ['N0H',' ','0','0','0','0','0'],
                 ['N0O',' ','0','0','0','0','0'],
                 ['N0W',' ','0','0','0','0','0'],
                 ['N0M',' ','0','0','0','0','0'],
                 ['N0E',' ','0','0','0','0','0'],
                 ['N0I',' ','0','0','0','0','0'],
                 ['N0R',' ','0','0','0','0','0'],
                 ['N0U',' ','0','0','0','0','0'],
                 ['W0S',' ','0','0','0','0','0'],
                 ['W0H',' ','0','0','0','0','0'],
                 ['W0O',' ','0','0','0','0','0'],
                 ['W0W',' ','0','0','0','0','0'],
                 ['W0M',' ','0','0','0','0','0'],
                 ['W0E',' ','0','0','0','0','0'],
                 ['W0I',' ','0','0','0','0','0'],
                 ['W0R',' ','0','0','0','0','0'],
                 ['W0U',' ','0','0','0','0','0']]

      args = get_args()
      import logsummary
      logsum = logsummary.theApp()
      cab = CabrilloUtils()
      for si in range (0, len(summary)):
         filename = summary[si][0]+'.LOG'
         filename = args.args.inputpath.strip()+'/'+filename
         data = cab.readFile(filename)
         if (data):
            call, ops, tot, cw, ph, ry, vhf = logsum.processQSOs(cab, data)
            if(call != summary[si][0]):
               summary[si][0] += ('==>%s'%(call))
            summary[si][1] = ops
            summary[si][2] = cw
            summary[si][3] = ph
            summary[si][4] = ry
            summary[si][5] = tot
            summary[si][6] = vhf
                  #break
         else: #No data or logfile from this station
            summary[si][1] = "No log file."
        
      self.exportcsv(summary)        

if __name__ == '__main__':
   app=theApp() 
