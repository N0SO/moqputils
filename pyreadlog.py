#!/usr/bin/python
"""
pyreadlog - description goes here
"""
import datetime
import argparse
from CabrilloUtils import CabrilloUtils

VERSION = '0.0.1'
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
    
class theApp(CabrilloUtils):
   def __init__(self):
      self.main()
      
   def getOperatorData(self, input, output):
      opData = ''
      return opData
      
   def main(self):
      args = get_args()
      #cab = CabrilloUtils()
      data = self.readFile(args.args.inputfile)
      
      for line in data:
         for tag in self.CABRILLOTAGS:
            if tag in line:
               print('%s = %s' % (tag, self.getCabstg(tag, line)))
   
   
   

if __name__ == '__main__':
   app=theApp()