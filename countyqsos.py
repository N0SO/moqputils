#!/usr/bin/python
"""
countyqsos - A summary of QSOs by mode, with 
county, state, providence and DX counts
"""
import datetime
import argparse
from CabrilloUtils import *

VERSION = '1.0.3'
COUNTYLIST = 'Countylist.csv'
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
   def __init__(self, data=None):
      if __name__ == '__main__':
          self.main(data)
      if (data != None):
          #print "Calling sum method"
          summary, counties, states, provs, dx, cw, ph, dg = self.sum(data)
          self.summary = summary
          self.counties = counties
          self.states = states
          self.provs = provs
          self.dx = dx
          self.cw = cw
          self.ph = ph
          self.dg = dg
          self.score = self.totalscore(counties, states, provs, dx, cw, ph, dg)
      else:
          self.summary = None
          self.counties = 0
          self.states = 0
          self.provs = 0
          self.dx = 0
          self.cw = 0
          self.ph = 0
          self.dg = 0
          self.score = 0
      
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
      
   def sum(self, logdata = None):
      summary = ""
      cab = CabrilloUtils()
      countydata = self.readCountylist()
      cw = 0
      ph = 0
      dg = 0
      mults = 0
      counties = 0
      states = 0
      provs = 0
      dx = 0
      for line in logdata:
         line = cab.packLine(line)
         #print line
         if 'QSO:' in line.upper():
            line = line.upper()
            qsoparts = line.split(' ')
            ci = 0
            for county in countydata:
               if (qsoparts[10] == county[0]):
                  #if (county[0] == 'MAR'): print line
                  if (countydata[ci][2] == 0):
                     mults +=1
                  countydata[ci][2] +=1
               ci += 1
            if (qsoparts[2] in cab.MODES):
                      if ('CW' in qsoparts[2]):
                         cw +=1
                      elif (qsoparts[2] in cab.PHONEMODES):
                         ph +=1
                      elif (qsoparts[2] in cab.DIGIMODES):
                         dg +=1
            else:
               print("UNDEFINED MODE: %s -- QSO data = %s"%(qsoparts[2], line))
      #Display summary
      if (mults > 0):
         ci = 0;
         for county in countydata:
            #print('%s, (%s), %d'%(county[1], county[0], county[2]))
            if (county[2] > 0):
               summary += ('%s, (%s), %d\n'%(county[1], county[0], county[2]))
               if (ci<115): # End of counties list
                  counties += 1
               elif (ci < 174): #End of states / US territories
                  states += 1
               elif (ci<183): #End of Canadian Providence list
                  provs += 1
               elif (ci <184): #End of DX list
                  dx += county[2]
            ci += 1
      return summary, counties, states, provs, dx, cw, ph, dg
    
   def totalscore(self, mo, states, provs, dx, cw, ph, dg):
      mults = mo+states+provs+dx
      qsopoints = ((cw+dg)*2) + ph
      score = qsopoints * mults
      return score

   def main(self, logdata = None):
      if ( logdata == None):
          args = get_args()
          logdata = self.readFile(args.args.inputfile)
      summary, counties, states, provs, dx, cw, ph, dg = self.sum(logdata)
      print ('QSO Summary:\n%d CW QSOs + %d PHONE QSOs + %d DIGITAL QSOs = %d Total QSOS\n'%(cw, ph, dg,cw+ph+dg))
      print ('MULT Summary:\nCounties worked:%d\nUS States worked:%d\nCanada worked:%d\nDX worked:%d\n'%(counties, states, provs, dx))
      print ('List of MULTS:\n %s\n'%(summary))
      print ('Score = %d'%(self.totalscore(counties, states, provs, dx, cw, ph, dg)))
            
if __name__ == '__main__':
   app=theApp()