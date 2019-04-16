#!/usr/bin/python
"""
CabrilloUtils - A collection of utilities to process CABRILLO
                Format log files.
import datetime
import argparse
"""

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
			 
    VERSION = '1.0.5'
    PHONEMODES = 'PH SSB LSB USB FM DV'
    DIGIMODES = 'RY RTY RTTY FSK AFSK PSK PSK31 PSK64 DIGU DIGL'
    MODES = 'CW' + PHONEMODES + DIGIMODES
    OPERATORTAGS = 'CALLSIGN LOCATION NAME ADDRESS ADDRESS-CITY \
                  ADDRESS-STATE-PROVINCE ADDRESS-POSTALCODE \
                  ADDRESS-COUNTRY EMAIL OPERATORS'
    CATEGORYTAGS = 'CATEGORY-ASSISTED CATEGORY-BAND CATEGORY-MODE \
                    CATEGORY-OPERATOR CATEGORY-POWER \
                    CATEGORY-STATION CATEGORY-TIME \
                    CATEGORY-TRANSMITTER CATEGORY-OVERLAY'
    MISCTAGS = 'CERTIFICATE CLAIMED-SCORE CLUB CONTEST \
                CREATED-BY IOTA-ISLAND-NAME OFFTIME SOAPBOX'
    HEADERTAGS = CATEGORYTAGS + OPERATORTAGS + MISCTAGS
    

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
        """
        Get the target Cabrillo data from a single string
        """
        returnstg = ''
        if (target in data):
            tmparry = data.split(target)
            returnstg = tmparry[1]
        if (returnstg):
            returnstg = returnstg.strip()
        print returnstg
        return returnstg
        
    def getCabArray(self, target, data):
        """
        Get the target Cabrillo data from an array
        (a Tuple, List, etc)
        """
        returnstg = ''
        for line in data:
            if (target in line):
                tmparry = line.split(target)
                returnstg = tmparry[1]
                break
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

    def getCabParams(self, data):
        cabCall = self.getCabArray('CALLSIGN:', data)
        cabName = self.getCabArray('NAME:', data)
        cabEmail = self.getCabArray('EMAIL:', data)
        cabAddress = self.getCabArray('ADDRESS:', data)
        cabAddCity = self.getCabArray('ADDRESS-CITY:', data)
        cabAddState = self.getCabArray('ADDRESS-STATE-PROVINCE:', data)
        cabAddZip = self.getCabArray('ADDRESS-POSTALCODE:', data)
        cabAddCountry = self.getCabArray('ADDRESS-COUNTRY:', data)
        return cabCall, cabName, cabEmail, cabAddress, cabAddCity, \
               cabAddState, cabAddZip, cabAddCountry
        
    def getCategory(self, data):
        """
        Return all of the lines defining CATEGORY
        as defined in self.CATEGORYTAGS
        """
        retdata = []
        for line in data:
           lineparts = line.split(':')
           if (lineparts[0] in self.CATEGORYTAGS):
              retdata.append(self.packLine(line))
        return retdata

    def determineCategory(self, data):
        operator = self.getCabArray('CATEGORY-OPERATOR:', data)
        if (operator in 'SINGLE-OP MULTI-OP CHECKLOG'):
           pass
        else:
           operator = 'UNKNOWN'
           
        mode = self.getCabArray('CATEGORY-MODE:', data)
        if (mode in 'CW SSB RTTY DIGITAL FM MIXED'):
           pass
        else:
           mode = 'UNKNOWN'
           
        power = self.getCabArray('CATEGORY-POWER:', data)
        if (power in 'HIGH LOW QRP'):
           pass
        else:
           power = 'UNKNOWN'
           
        station = self.getCabArray('CATEGORY-STATION:', data)
        if (station in 'FIXED MOBILE PORTABLE ROVER ROVER-LIMITED \
                        ROVER-UNLIMITED EXPEDITION HQ SCHOOL'):
           pass
        else:
           station = 'UNKNOWN'
        
        overlay = self.getCabArray('CATEGORY-OVERLAY:', data)
        if (overlay in 'CLASSIC ROOKIE TB-WIRES BAND-LIMITED \
                        NOVICE-TECH OVER-50'):
           pass
        else:
           overlay = 'UNKNOWN'
           
        returnvals = []
        returnvals.append(station)
        returnvals.append(operator)
        returnvals.append(power)
        returnvals.append(mode)
        returnvals.append(overlay)
        
        return returnvals

         
          

if __name__ == '__main__':
   app=CabrilloUtils()
   print app.getVersion()