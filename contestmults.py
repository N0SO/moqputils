#!/usr/bin/python
"""
ContestMults - A collection of utilities to process contest 
               multipliers extracted form a CABRILLO format 
               log file.
Update History:
* Fri Jan 10 2020 Mike Heitmann, N0SO <n0so@arrl.net>
- V.0.0.1 - Just starting out
"""

VERSION = '0.0.1'

STATEMULTS = [ 'AL',
               'AK',
               'AZ',
               'AR',
               'CA',
               'CO',
               'CT',
               'DE',
               'FL',
               'GA',
               'HI',
               'ID',
               'IL',
               'IN',
               'IA',
               'KS',
               'KY',
               'LA',
               'ME',
               'MD',
               'MA',
               'MI',
               'MN',
               'MS',
               'MO',
               'MT',
               'NE',
               'NV',
               'NH',
               'NJ',
               'NM',
               'NY',
               'NC',
               'ND',
               'OH',
               'OK',
               'OR',
               'PA',
               'RI',
               'SC',
               'SD',
               'TN',
               'TX',
               'UT',
               'VT',
               'VA',
               'WA',
               'WV',
               'WI',
               'WY' ]

ARRLW0 = [ 'CO',
           'IA',
           'KS',
           'MN',
           'MO',
           'NE',
           'ND',
           'SD' ]
           
ARRLW1 = [ 'CT',
           'EMA',
           'ME',
           'NH',
           'RI',
           'VT',
           'WMA' ]

ARRLW2 = [ 'ENY',
           'NLI',
           'NNJ',
           'NNY',
           'SNJ',
           'WNY' ]

ARRLW3 = [ 'DE',
           'EPA',
           'MDC',
           'WPA' ]
         
ARRLW4 = [ 'AL',
           'GA',
           'KY',
           'NC',
           'NFL',
           'SC',
           'SFL',
           'WCF',
           'TN',
           'VA',
           'PR',
           'VI' ]

ARRLW5 = [ 'AR',
           'LA',
           'MS',
           'NM',
           'NTX',
           'OK',
           'STX',
           'WTX' ]
           
ARRLW6 = [ 'EB',
           'LAX',
           'ORG',
           'SB',
           'SCV',
           'SDG',
           'SF',
           'SJV',
           'SV',
           'PAC' ]
          
ARRLW7 = [ 'AZ',
           'EWA',
           'ID',
           'MT',
           'NV',
           'OR',
           'UT',
           'WWA',
           'WY',
           'AK' ]
           
ARRLW8 = [ 'MI',
           'OH',
           'WV' ]
           
ARRLW9 = [ 'IL',
           'IN',
           'WI' ]

PROVIDENCEMULTS = ['ON',
                   'QC',
                   'NS',
                   'NB',
                   'MB',
                   'BC',
                   'PE',
                   'SK',
                   'AB',
                   'NL' ]
                   
ARRLCA = ['MAR',
          'NL',
          'QC',
          'ONN',
          'ONS',
          'ONE',
          'GTA',
          'MB',
          'SK',
          'AB',
          'BC',
          'NT' ]
          


class ContestMults():
    def __init__(self):
        self.multList = self.combine_multLists([ARRLW0, ARRLW1,
                                                ARRLW2, ARRLW3,
                                                ARRLW4, ARRLW5,
                                                ARRLW6, ARRLW7,
                                                ARRLW8, ARRLW9,
                                                ARRLCA])
        
        self.mults = self.creat_mult_dict(self.multList)

    def __version__(self):
       return self.VERSION

    def getVersion(self):
       return self.VERSION

    def combine_multLists(self, lLists):
       C = []
       for ll in lLists:
          for i in ll:
             if (i in C):
                print('Caution: Duplicate mult key for %s already exists.'%(i))
             C.append(i)
       return C
       
    def creat_mult_dict(self, indexList):
       multDict = dict()
       for i in indexList:
          multDict[i] = False
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
       
       
