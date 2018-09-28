#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fillinopdata.py - Read the awards.csv file and fill in
the missing name, address, e-mail address from the
MOQP cabrillo log files.
"""
import datetime
import argparse
from os import walk
from CabrilloUtils import *

VERSION = '1.0.0'
ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        usageSTG = ('fillinopdata.py --input <inputfile> --directory '
                    '<MOQP log files path>')
        aboutSTG = ('Utility to read the MOQP awards file (in tab '
                    'separated variable format) add operator names, '
                    'addresses and e-mail from the MOQP log files '
                    'submitted.')

        parser = argparse.ArgumentParser(usage=usageSTG,
                                         description=aboutSTG,
                                         epilog='That\'s all folks!')
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the log file input file name")
        parser.add_argument("-d", "--directory", default='./',
            help="Specifies the directory in which the log files reside.")
        return parser.parse_args()

class FillInOpData():
   def __init__(self, csvlist=None, logdir=None):
      self.return_data = []
      if __name__ == '__main__':
          self.main()
      else:
          if (csvlist and logdir):
              self.return_data = self.processOps(csvlist, logdir)
              
      
   def readFile(self, filename):
       """Read and return data from a file"""
       with open(filename, 'r') as thisfile:
          data = thisfile.readlines()
       return data
       
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
     
   def processOps(self, opcall_list, logdir):
      cab = CabrilloUtils()
      retdata = []

      f = []
      for (dirpath, dirnames, filenames) in walk(logdir):
          f.extend(filenames)
          break


      for line in opcall_list:
          elements = line.split('\t')
          e=elements[3]
          opcall = ''
          for c in e:
              if (c == '\xD8'): #No slashed zeros in file names
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
          retdata.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(
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
      self.return_data = retdata
      return retdata          

   def main(self):
      args = get_args()
      dirpath = args.args.directory.strip()
      opcall_list=self.readFile(args.args.inputfile)
      opdata = self.processOps(opcall_list, dirpath)
      for line in self.return_data:
          print('%s'%(line))
           
if __name__ == '__main__':
   app=FillInOpData()
  
  
