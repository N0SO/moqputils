#!/usr/bin/python
"""
CabrilloUtils - A collection of utilities to process CABRILLO
                Format log files.
Update History:
* Tues Sep 18 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Initial release
* Tue May 01 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.2 - Release of moqpcategory class
* Fri Oct 11 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.8 - 2019-10-11
- Fixed typo in CABRILLOAGS tag END-OF-LOG:
* Thu Oct 17 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.9 
- Adding dictionary objects for HEADER and QSO data
"""

class CabrilloUtils():
    CABRILLOTAGS = ['START-OF-LOG',
             'CALLSIGN',
             'CREATED-BY',
             'LOCATION',
             'CONTEST',
             'NAME',
             'ADDRESS',
             'ADDRESS',
             'ADDRESS-CITY',
             'ADDRESS-STATE-PROVINCE',
             'ADDRESS-POSTALCODE',
             'ADDRESS-COUNTRY',
             'EMAIL',
             'CATEGORY-ASSISTED', 
             'CATEGORY-BAND', 
             'CATEGORY-MODE', 
             'CATEGORY-OPERATOR', 
             'CATEGORY-OVERLAY',
             'CATEGORY-POWER', 
             'CATEGORY-STATION', 
             'CATEGORY-TRANSMITTER', 
             'CERTIFICATE', 
             'OPERATORS', 
             'CLAIMED-SCORE',
             'CLUB', 
             'CREATED-BY',
             'IOTA-ISLAND-NAME',
             'OFFTIME',
             'SOAPBOX',
             'QSO',
             'END-OF-LOG']
             
    VERSION = '1.0.9'
    PHONEMODES = 'PH SSB LSB USB FM DV'
    DIGIMODES = 'RY RTY RTTY FSK AFSK PSK PSK31 PSK64 DIGU DIGL DG FT8'
    MODES = 'CW' + PHONEMODES + DIGIMODES
    VHFFREQ = '144 222 432 440 902 1.2G'
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
    
    QSOTAGS = ['FREQ', 'MODE', 'DATE', 'TIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH']

    CATEGORYTAGL = ['CATEGORY-ASSISTED', 'CATEGORY-BAND', 'CATEGORY-MODE',
                    'CATEGORY-OPERATOR', 'CATEGORY-POWER',
                    'CATEGORY-STATION', 'CATEGORY-TIME',
                    'CATEGORY-TRANSMITTER', 'CATEGORY-OVERLAY']

    def __init__(self):
        pass

    def __version__(self):
        return self.VERSION

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
        
    def getLogFile(self, filename):
        log = None
        fileText = self.readFile(filename)
        if (self.IsThisACabFile(fileText)):
            log = self.getQSOdata(fileText)
        return log

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
       
    def MakeEmptyDict(self,taglist, initval):
       """
       Return an empty dictionary of elements
       based on taglist passed.
       """
       emptydict = dict()
       for tag in taglist:
           emptydict[tag] = initval
           
       return emptydict    
           
    def makeHEADERdict(self):
       """
       Return an empty  dictionary for Cabrillo HEADER Data
       based on CABRILLITAGS list above.
       header = dict()
       for tag in self.CABRILLOTAGS:
           header[tag] = ''
       """
       header = self.MakeEmptyDict(self.CABRILLOTAGS, '')
       return header

    def makeQSOdict(self):
       """
       Return an empty dictionary for Cabrillo QSO Data
       based on the QSOTAGS list above
       """
       qso = self.MakeEmptyDict(self.QSOTAGS, '')
       return qso

    def getCABHeaderdict(self, cabdata):
       header = self.makeHEADERdict()
       for line in cabdata:
          headerline = self.packLine(line.upper())
          linesplit = line.split(':')
          if (linesplit[0] in 'QSO END-OF-LOG'):
             continue
          else:
             if (len(linesplit) > 1):
                header[linesplit[0]] += linesplit[1].strip()
       #print(header)
       return header
       
    def getQSOdata(self, cabdata):
       thislog = dict()
       qsos = []
       header = self.makeHEADERdict()
       for line in cabdata:
          cabline = self.packLine(line)
          linesplit = cabline.split(':')
          if (linesplit[0] == 'QSO'):
             qso = self.makeQSOdict()
             qsoparts = linesplit[1].split(' ')
             i=1
             for tag in self.QSOTAGS:
                 qso[tag] = qsoparts[i].strip()
                 i += 1
             qsos.append(qso)
          else:
             if (len(linesplit) > 1):
                 header[linesplit[0]] += linesplit[1].strip()
       thislog['HEADER'] = header
       thislog['QSOLIST'] = qsos
       return thislog


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
        
    def getCategorydict(self, data):
        """
        Return a dictionary all of the lines defining 
        CATEGORY as defined in self.CATEGORYTAGS
        """
        retdata = dict()
        for tag in self.CATEGORYTAGL:
           retdata[tag] = ''
        for line in data:
           line = self.packLine(line)
           lineparts = line.split(':')
           if (lineparts[0] in self.CATEGORYTAGL):
              if(len(lineparts)>1):
                  retdata[lineparts[0]] = lineparts[1]
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
        
    def determineCategorydict(self, data):
        returnvals = dict()
        #operator = self.getCabArray('CATEGORY-OPERATOR:', data)
        #operator = data['CATEGORY-OPERATOR']
        if (data['CATEGORY-OPERATOR'] in \
                                  'SINGLE-OP MULTI-OP CHECKLOG'):
           returnvals['CATEGORY-OPERATOR'] = \
                                   data['CATEGORY-OPERATOR']

        else:
           returnvals['CATEGORY-OPERATOR'] = 'UNKNOWN'
           
        #mode = self.getCabArray('CATEGORY-MODE:', data)
        #if (mode in 'CW SSB RTTY DIGITAL FM MIXED'):
        if (data['CATEGORY-MODE'] in \
                                 'CW SSB RTTY DIGITAL FM MIXED'):
           returnvals['CATEGORY-MODE'] = data['CATEGORY-MODE']
        else:
           data['CATEGORY-MODE'] = 'UNKNOWN'
           
        #power = self.getCabArray('CATEGORY-POWER:', data)
        #if (power in 'HIGH LOW QRP'):
        if (data['CATEGORY-POWER'] in 'HIGH LOW QRP'):
           returnvals['CATEGORY-POWER'] = data['CATEGORY-POWER']
        else:
           returnvals['CATEGORY-POWER'] = 'UNKNOWN'
           
        #station = self.getCabArray('CATEGORY-STATION:', data)
        #if (station in 'FIXED MOBILE PORTABLE ROVER ROVER-LIMITED \
        #                ROVER-UNLIMITED EXPEDITION HQ SCHOOL'):
        if (data['CATEGORY-STATION'] in 'FIXED MOBILE PORTABLE \
                          ROVER ROVER-LIMITED \
                          ROVER-UNLIMITED EXPEDITION HQ SCHOOL'):
           returnvals['CATEGORY-STATION'] = \
                                         data['CATEGORY-STATION']
        else:
           returnvals['CATEGORY-STATION'] = 'UNKNOWN'
        
        #overlay = self.getCabArray('CATEGORY-OVERLAY:', data)
        #if (overlay in 'CLASSIC ROOKIE TB-WIRES BAND-LIMITED \
        #                NOVICE-TECH OVER-50'):
        if (data['CATEGORY-OVERLAY'] in 'CLASSIC ROOKIE TB-WIRES \
                        BAND-LIMITED NOVICE-TECH OVER-50'):
           returnvals['CATEGORY-OVERLAY'] = \
                                   data['CATEGORY-OVERLAY']
        else:
           returnvals['CATEGORY-OVERLAY'] = 'UNKNOWN'
           
        return returnvals


if __name__ == '__main__':
   app=CabrilloUtils()
   """
   logdata = app.getLogFile('../testfiles/W0QBX.LOG')
   print (logdata)
   #catg = app.getCategorydict(logdata)
   
   #print(catg)
   """
   """print('Callsign:%s\n Name:%s\n Ops:%s\n'%(header['CALLSIGN'],
                                             header['NAME'],
                                             header['OPERATORS']))"""
   
   
   print ('Classname: %s Version: %s'%(app.__class__.__name__,
                                       app.__version__()))
