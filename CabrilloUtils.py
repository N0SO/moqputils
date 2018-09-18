#!/usr/bin/python
"""
pyreadlog - description goes here
"""
import datetime
import argparse

class CabrilloUtils():
    CABRILLOTAGS = ['START-OF-LOG:',
			 'CALLSIGN:',
			 'CREATED-BY:',
			 'LOCATION:',
			 'CONTEST:',
			 'NAME:',
			 'ADDRESS:',
			 'ADDRESS:',
			 'ADDRESS-CITY:',
			 'ADDRESS-STATE-PROVINCE:',
			 'ADDRESS-POSTALCODE:',
			 'ADDRESS-COUNTRY:',
			 'EMAIL:',
			 'CATEGORY-ASSISTED:', 
			 'CATEGORY-BAND:', 
			 'CATEGORY-MODE:', 
			 'CATEGORY-OPERATOR:', 
			 'CATEGORY-POWER:', 
			 'CATEGORY-STATION:', 
			 'CATEGORY-TRANSMITTER:', 
			 'CERTIFICATE:', 
			 'OPERATORS:', 
			 'CLAIMED-SCORE:',
			 'CLUB:', 
			 'SOAPBOX:',
			 'QSO:',
			 'END-OF-LOG: ']
			 
    VERSION = '1.0.2'
    PHONEMODES = 'PH SSB LSB USB FM DV'
    DIGIMODES = 'RY RTY RTTY FSK AFSK PSK PSK31 PSK64 DIGU DIGL'
    MODES = 'CW' + PHONEMODES + DIGIMODES
    HEADERTAGS = 'CALLSIGN LOCATION NAME ADDRESS ADDRESS-CITY ADDRESS-STATE-PROVINCE ADDRESS-POSTALCODE ADDRESS-COUNTRY EMAIL OPERATORS SOAPBOX'

    def __init__(self):
        pass

    def getVersion(self):
       return self.VERSION
       
    def readFile(self, filename):
        """Read and return the entire file"""
        data = None
        try:
            with open(filename, 'r') as thisfile:
                data = thisfile.readlines()
        except:
            data = None
        return data

    def IsThisACabFile(self, data):
        cabfile = False
        if ( (any ('START-OF-LOG:' in string for string in data)) and
            (any ('CALLSIGN:' in string for string in data)) and
            (any ('QSO:' in string for string in data)) and
            (any ('END-OF-LOG:' in string for string in data)) ):
            cabfile = True
        return cabfile
    
    def getCabstg(self, target, data):
        returnstg = ''
        if (target in data):
            tmparry = data.split(target)
            returnstg = tmparry[1]
        if (returnstg):
            returnstg = returnstg.strip()
        return returnstg
        
    def packLine(self, line):
       """Remove extra spaces, commas, trailing garbage from each record"""
       newline = line.replace(',',' ')
       newline = newline.replace('\t',' ')
       while "  " in newline:
          newline = newline.replace("  ", " ")
       newline = newline.strip()
       newline = newline.lstrip()
       
       return newline
        
    def getCABHeader(self, cabdata):
       header = []
       for line in cabdata:
          linesplit = line.split(':')
          if (linesplit[0] in 'QSO START-OF-LOG END-OF-LOG'):
             continue
          else:
             headerline = self.packLine(line)
             header.append(headerline)
       return header
        
    def getOperatorData(self, data):
       opData = []
       for line in data:
          headertag = line.split(':')
          if (headertag[0] in self.HEADERTAGS):
             opData.append(line)
       return opData
       
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

if __name__ == '__main__':
   app=CabrilloUtils()
   print app.getVersion()