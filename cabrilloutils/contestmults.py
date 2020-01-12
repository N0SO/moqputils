#!/usr/bin/python
"""
ContestMults - A collection of utilities to process contest 
               multipliers extracted from a CABRILLO format 
               log file.
Update History:
* Fri Jan 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

VERSION = '0.0.1'

MULTFILES = ['shared/multlists/arrlw0.csv',
             'shared/multlists/arrlw1.csv',
             'shared/multlists/arrlw2.csv',
             'shared/multlists/arrlw3.csv',
             'shared/multlists/arrlw4.csv',
             'shared/multlists/arrlw5.csv',
             'shared/multlists/arrlw6.csv',
             'shared/multlists/arrlw7.csv',
             'shared/multlists/arrlw8.csv',
             'shared/multlists/arrlw9.csv',
             'shared/multlists/arrlCA.csv']

class ContestMults():
    def __init__(self):
       self.mults = self.readmultlists(MULTFILES)

    def __version__(self):
       return VERSION

    def getVersion(self):
       return VERSION

    def readonefile(self, filename):
        data = None
        try:
            with open(filename, 'r') as thisfile:
                data = thisfile.readlines()
        except:
            print('Error reading file %s'%(filename))
            data = None
        return data
       
    def readmultlists(self, files):
        multlist = []
        mults = dict()
        for fn in files:
            fndata = self.readonefile(fn)
            #print(fndata)
            if fndata:
                multlist.append(fndata)
        multlist = self.combine_multLists(multlist)
        mults = self.create_mult_dict(multlist)
        return mults

    def combine_multLists(self, lLists):
       C = []
       for ll in lLists:
          for i in ll:
             if (i in C):
                print('Caution: Duplicate mult key for %s already exists.'%(i))
             C.append(i)
       return C
       
    def create_mult_dict(self, indexList):
       multDict = dict()
       for i in indexList:
          multDict[i.strip()] = False
       return multDict
       
    def isValidMult(self, mult):
       if (mult in self.mults):
          retval = True
       else:
          retval = False
       return retval
       
    def isMultSet(self, mult):
       retval = False
       if (mult in self.mults):
          retval = self.mults[mult]
       return retval
       
    def setMult(self, mult):
       retval = False
       if (mult in self.mults):
          self.mults[mult] = True
          retval = True
       return retval
       
    def sumMults(self):
       mults = 0
       for mult in self.mults:
          if self.mults[mult]:
             mults += 1
       return mults

    def sumMultsinQSOList(self, qsolist):
       for Qso in qsolist:
           self.setMult(Qso['URCALL'])
       return self.sumMults()
       
if __name__ == '__main__':
   app=ContestMults()
   print(app.mults)
   #print( 'Version %s exiting...'%(app._get_version()) )
       
