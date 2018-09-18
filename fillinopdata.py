#!/usr/bin/python
"""
fillinopdata.py - Read the awards.csv file and fill in
the missing name, address, e-mail address from the
cabrillo log files.
"""
import datetime
import argparse
from os import walk
from CabrilloUtils import *

VERSION = '0.0.1'
COUNTYLIST = 'Countylist.csv'
ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(usage='This is the usage string.',
                                         description='This is the description.',
                                         epilog='That\'s all folks!')
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the log file input file name")
        parser.add_argument("-d", "--directory", default='./',
            help="Specifies the directory in which the log files reside.")
        return parser.parse_args()

class theApp():
   def __init__(self):
      self.main()
      
   def readFile(self, filename):
       """Read and return data from a file"""
       with open(filename, 'r') as thisfile:
          data = thisfile.readlines()
       return data
       
   def readCountylist(self, filename=COUNTYLIST):
       """Read list of counties"""
       data = self.readFile(filename)
       countylist = []
       for line in data:
          #print('===> %s'%(line))
          if (line[0:1] != '#'):
             nextent = line.split(',')
             nextent = [nextent[1].strip(), nextent[0].strip(), 0]
             countylist.append(nextent)
       return countylist
       
   def getHeaderField(self, tag, hdata):
      retdata = 'y'
      tempdata ='z'
      #if tag in hdata:
      for el in hdata:
         #print el
         if (tag in el):
             #print('found tag %s\nhdata=%s\n'%(tag, hdata))
             tempdata = el.split(':')
             #print('tempdata = %s'%(tempdata))
             retdata = tempdata[1].strip()
             #print('retdata = %s'%(retdata))
             #print('found %s'%(tag))
             break
      #print('tag = %s, temp = %s data = %s\nhdata = %s'%(tag, tempdata, retdata, hdata))
      return retdata
     
   def main(self):
      args = get_args()
      cab = CabrilloUtils()
      dirpath = args.args.directory.strip()
     
      f = []
      for (dirpath, dirnames, filenames) in walk(args.args.directory):
          f.extend(filenames)
          break

      award_data=self.readFile(args.args.inputfile)
      
      for line in award_data:
          elements = line.split('\t')
          e=elements[3]
          opcall = ''
          for c in e:
              if (c == '\xD8'):
                  opcall+='0'
              else:
                  opcall+=c
          logfile = opcall.upper()+'.LOG'
          #print opcall, logfile
	  opname='x'
	  opadr='x'
	  opcity='x'
	  opstate='x'
	  opzipcode='x'
	  opcountry='x'
	  opemail='x'
          if (logfile in f):
              data = cab.readFile(dirpath+'/'+logfile)
              if (data):
                  #print logfile, len(logfile)
                  header = cab.getCABHeader(data)
                  opdata = cab.getOperatorData(header)
                  if (opdata):
                      #print opdata
                      opname = self.getHeaderField('NAME:', opdata)
                      opadr=self.getHeaderField('ADDRESS:', opdata)
                      opcity=self.getHeaderField('ADDRESS-CITY:', opdata)
                      opstate=self.getHeaderField('ADDRESS-STATE-PROVINCE:', opdata)
                      opzipcode=self.getHeaderField('ADDRESS-POSTALCODE:', opdata)
                      opcountry=self.getHeaderField('ADDRESS-COUNTRY:', opdata)
                      opemail=self.getHeaderField('EMAIL:', opdata)
          print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(
                  elements[0],
                  elements[1],    
                  elements[2],    
                  elements[3], 
                  elements[4],
                  opname,
                  opadr,
                  opcity,
                  opstate,
                  opzipcode,
                  opcountry,
                  opemail))
          
            
if __name__ == '__main__':
   app=theApp()
  
  
