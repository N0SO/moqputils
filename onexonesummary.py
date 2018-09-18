#!/usr/bin/python
"""
countyqsos - A summary of QSOs by mode, with 
county, state, providence and DX counts
"""
import datetime
import argparse
from CabrilloUtils import *

VERSION = '1.0.0'
FILELIST = 'filelist.txt'
ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputfile", default=FILELIST,
            help="Specifies the file name that contains the list of files to summarize.")
        return parser.parse_args()

class theApp():
   def __init__(self):
      self.main()
      
   def readFile(self, filename):
       """Read and return data from a file"""
       with open(filename, 'r') as thisfile:
          data = thisfile.readlines()
       return data
       
   def parseResults(self, data):
      call = None
      ops = None
      cwqs = None
      phqs = None
      dgqs = None
      totl = None
      for item in data:
         item = item.strip()
         #print('=========>%s'%(item))
         if ('CALLSIGN:' in item):
            temp = item.split(':')
            call = self.stripCallsign(temp[1])
            #print('==========================(CALL)>%s, %s'%(call, temp[1]))
         elif ('OPERATORS:' in item):
            temp = item.split(':')
            ops = temp[1].strip()
         elif ('CW:' in item):
            temp = item.split(': ')
            cwqs = temp[1].strip()
            #print('==========================(CW)>%s, %s'%(cwqs, temp[1]))
         elif ('PH:' in item):
            temp = item.split(': ')
            phqs = temp[1].strip()
            #print('==========================(PH)>%s, %s'%(phqs, temp[1]))
         elif ('DIGITAL:' in item):
            temp = item.split(': ')
            dgqs = temp[1].strip()
            #print('==========================(DG)>%s, %s'%(dgqs, temp[1]))
         elif ('TOTAL QSOs:' in item):
            temp = item.split(':')
            totl = temp[1].strip()
            #print('==========================(TOTAL)>%s, %s'%(totl, temp[1]))
      return call, ops, cwqs, phqs, dgqs, totl   
      
   def exportcsv(self, data):
      #print ('Length of data is %s'%(len(data)))
      columns = len(data)
      for row in range(0,6):
          self.exportrow(row, columns, data)
          if (row == 1):
             # Add VERIFY column
             print('LOG VERIFIED')
          
   def exportrow(self,row, maxcolumn, data):
      TAGS = ['STAT\\1X1','OPs','CW QSOs','PH QSOs', 'DIGITAL QSOs', 'TOTAL QSOs']
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
      summary = [['K0S',' ','0','0','0','0'],['K0H',' ','0','0','0','0'],['K0O',' ','0','0','0','0'],['K0W',' ','0','0','0','0'],['K0M',' ','0','0','0','0'],['K0E',' ','0','0','0','0'],
                 ['N0S',' ','0','0','0','0'],['N0H',' ','0','0','0','0'],['N0O',' ','0','0','0','0'],['N0W',' ','0','0','0','0'],['N0M',' ','0','0','0','0'],['N0E',' ','0','0','0','0'],
                 ['W0S',' ','0','0','0','0'],['W0H',' ','0','0','0','0'],['W0O',' ','0','0','0','0'],['W0W',' ','0','0','0','0'],['W0M',' ','0','0','0','0'],['W0E',' ','0','0','0','0']]

      args = get_args()
      files = self.readFile(args.args.inputfile)
      import logsummary
      logsum = logsummary.theApp()
      for file in files:
         data = logsum.processLog(file.strip())
         if (data):
            call, ops, cw, ph, ry, tot = self.parseResults(data)
            #call = self.stripCallsign(call)
            #print '===>', call,ops,cw,ph,ry,tot
            for si in range (0, len(summary)):
	     if(call == summary[si][0]):
	        summary[si][1] = ops
	        summary[si][2] = cw
	        summary[si][3] = ph
	        summary[si][4] = ry
	        summary[si][5] = tot
	        break
#	     si+=1
      #print summary
        
      self.exportcsv(summary)        

 #     for station in summary:
 #        print station
        


if __name__ == '__main__':
   app=theApp() 
