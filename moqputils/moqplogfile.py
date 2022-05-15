#!/usr/bin/env python3
"""
MOQPLogFile     - An MOQP Log File structure with processing
                  utilities.
                
Update History:
* Thu Apr 28 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Just getting started
* Sun May 01 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Ready for first release.
-          Added method sortQSOdictList to sort the resulting QSO
-          list in various ways. Default is by DATETIME in ascending
-          order. 
"""
import sys, os
from moqputils.moqpqsoutils import MOQPQSOUtils



class MOQPLogFile(MOQPQSOUtils):
    """
    QSOTAGS = ['FREQ', 'MODE', 'DATETIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 'URQTH', 'NOTES']
    """
    QSOTAGS = ['FREQ', 'MODE', 'DATETIME', 'MYCALL',
               'MYREPORT', 'MYQTH', 'URCALL', 'URREPORT', 
               'URQTH', 'DUPE', 'ERROR', 'NOTES', 'QID']

    def __init__(self, logFile=None):
        self.initLog()
        if (logFile):
            if (isinstance(logFile,str)):
                if (os.path.isfile(logFile)):
                    self.buildLog(logFile)
            
    """
    Initialize log object:
       Set interal values RAWLOG, HEADER, QSOLIST to None
    """
    def initLog(self):
        self.RAWLOG = None
        self.HEADER = None
        self.QSOLIST = None
        
    """
    Fetch data from raw log file and return as a single 
    string of text if Perist is set True the raw log text
    string will also be save in self.RAWLOG
    """
    def readLogText(self, logpath, Persist = False):
       
       rawlog = self.readFile(logpath, linesplit = False)
       #print(isinstance(rawlog,str),'\n',rawlog)
       if (self.IsThisACabFile(rawlog.strip())):
           pass
       else:
          rawlog = None
       if (Persist):
          self.RAWLOG = rawlog
       return rawlog
       
    """
    Return the logfile data as a list of lines.
    if a logString is passed, it is parsed and
    returned as a list. If no logstring is passed, the
    string in self.RAWLOG is parsed returned as a list.
    """
    def getLogList(self, logString=None):
       logList = None
       if (logString == None):
           logString = self.RAWLOG
       
       if (logString):
           logList = []
           logList = logString.splitlines()
       
       return logList
   
    """
    Build the MOQP Log object:
       if the input  parameter Log is a list, it is assumed
       to be a the raw log as a list of lines.
       
       if the parameter Log is a string, is is assumed to be
       the path to a file containing the raw log data.
       
       If the parameter Log is set to None or omitted, the
       raw log text will be taken from self.RAWLOG if it is
       something other than None type.
       
       The header and qso list will be returned as a dict
       object (log in the example below) with two elements:
        log['HEADER']  - A dict object of the log header, with 
                         the dictionary index elements using the 
                         names defined in self.CABRILLOTAGS
        log['QSOLIST'] - A list of dictionary objects, with each
                         element in the list a dictionary of a QSO
                         record, with the dictionary index elements
                         using the names defined in self.QSOTAGS.
                
       Set Persist = False if it is not desired to save the header
       data in self.HEADER and the qso list saved as self.QSOLIST.
    """
    def buildLog(self, Log=None, Persist = True):
       logList = None
       if(Log):
           if(isinstance(Log, str)):
               #Path name string, read file for data
               logText = self.readLogText(Log, Persist)
               logList = self.getLogList(logText)
           elif (isinstance(Log, list)):
               #List of raw log file text lines
               logList = Log
       else:
           logList=self.getLogList(self.RAWLOG)
    
       if (logList):
           log = self.getLogdictData(logText)
           dictqsoList = self.buildQSOList(log['QSOLIST'])
           log['QSOLIST'] = dictqsoList
           if (Persist):
               self.HEADER = log['HEADER']
               self.QSOLIST = dictqsoList               
           return log
       else:
           return None
    """
    sortQSOdictList - Sort a list of qso record dictionary objects.
      This uses the python sort() function and is taylored for 
      sorting MOQP QSO lists of dict objesct Default action is 
      to by the DATETIME key in ascending order.

    qsodictList - A list object containing QSO records in dict
                  format where each element in the object is
                  indexed by the key names defined in QSOTAGS.
                  If omitted, the internal object sel.QSOLIST
                  will be sorted and returned.
                  
    sortKey     - String containing the dict key name to sort 
                  by. The default key is DATETIME. 
                  This may be omitted if the default action of
                  sort by DATETIME is desired.
                  
    sortLtoS    - A boolean representing the sort order desired.
                  True = largest to smallest, False = smallest 
                  to largest. Defaults to smallest to largest.
                  This my be omitted if the default behavior of
                  smallest to largest is desired.
                  
    
    """       
    def sortQSOdictList(self, qsodictList=None, 
                              sortKey='DATETIME',
                              sortLtoS = False):
           newList = None
           if qsodictList == None:
                  qsodictList = self.QSOLIST
           """
           This can fail because the log file QSO data is not
           formatted properly. Catch error and return without
           crashing.
           """       
           try:       
               newList = sorted(qsodictList, 
                            key=lambda i: i[sortKey],
                            reverse = sortLtoS)
           except Exception as e: # Catch everything
               #e = sys.exc_info()[0]
               print( "error data: {}".format(e) )
    
           return newList       
    """
    buildQSOList - Build a list of qsos as dictionary objects
                   using the MOQP QSOTAGS list as the index keys.
         qsolist - A list with each entry represnting the text
                   from an MOQP QSO:
    QSO: <freq> <mode> <date> <time> <mycall> <myreport> 
                               <myqth> <urcall> <urreport> <urqth>
    
    Returns a list of dictionary indexed with keys from QSOLIST[]    
    """       
    def buildQSOList(self, qsolist):
       qsodictList = None
       if (qsolist and isinstance(qsolist, list)):
           qsodictList = []
           qcount = 0
           for qso in qsolist:
               qcount += 1
               #Split off the 'QSO:' text
               tagpos = qso.find('QSO:')
               tqso=self.packLine(qso[tagpos+4:])
               #print(tqso)
               dictqso = self.getQSOdict(tqso)
               dictqso['QID'] = qcount
               dictqso['DUPE'] = 0
               qsodictList.append(dictqso)               
       return qsodictList
    
    """
    showQSO - Converts a qso dictionary object back into text that
              may be printed or displayed.
              
        qso - The QSO dict() object
        
        Returns textqso as a string:
    QSO: <freq> <mode> <date_time> <mycall> <myreport> <myqth>
                                   <urcal> <urreport> <urqth>
    """
    def showQSO(self, qso):
      textqso = ('QSO: {} {} {} {} {} {} {} {} {}'.format(\
                     qso['FREQ'],
                     qso['MODE'],
                     qso['DATETIME'],
                     qso['MYCALL'],
                     qso['MYREPORT'],
                     qso['MYQTH'], 
                     qso['URCALL'],
                     qso['URREPORT'], 
                     qso['URQTH']))
      return textqso     

    """
    showQSOList - Converts a list of qso dict objects to text
                  by calling showQSO for each element in the list.
                  
        qsolist - The list of dict() qso objects to convert. If 
                  None or omitted, the class object self.QSOLIST
                  will be used as input.
        returns a list of strings, string for each QSO line.
    """
    def showQSOList(self, qsolist=None):
      if qsolist == None:
        qsolist = self.QSOLIST
      textqsolist =''
      for qso in qsolist:        
        textqsolist += '{}\n'.format(self.showQSO(qso))
      return textqsolist

    """
    showHeader - Converts a cabrillo file log header from dict()
                 format to a single string containing the log header
                 with each line separated by the '\n' character.
                  
        header  - The dict() indexed log header to convert. If 
                  None or omitted, the class object self.HEADER
                  will be used as input.
        returns the log header as a single string containing the 
        log header text with each line separated by the '\n' character.
    """
    def showHeader(self, header = None, tagList = None):
      if header == None:
        #Use oject HEADER
        header = self.HEADER
      if tagList == None:
        tagList = self.CABRILLOTAGS

      textheader = ''
      for tag in tagList:
        #if not( tag in ['QSO','END-OF-LOG']):
        textheader += '{}: {}\n'.format(tag, header[tag])
        
      return textheader
      
    """
    getValidQSOs - return a list of valid QSOs.
    """
    def getValidQSOs(self, qsolist=None, witherrors=False):
        return_list = None
        if (qsolist == None): qsolist = self.QSOLIST
        if (qsolist):
            return_list = []
            for q in qsolist:
                if( (q['ERROR'] == witherrors) ):
                    return_list.append(q)
            if (len(return_list) == 0): return_list = None
        return return_list
