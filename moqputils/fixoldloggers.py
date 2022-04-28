#!/usr/bin/env python3
"""
fixoldloggers   - Utility to remove the sequence / serial number
                  fields from MOQP file created with old versions
                  of writelog
                
Update History:
* Wed Apr 27 2022 Mike Heitmann, N0SO <n0so@arrl.net>
-V0.0.1 - Just getting started
"""

from moqputils.moqpqsoutils import MOQPQSOUtils

class fixOldLoggers(MOQPQSOUtils):

    BADLOGGERS = ['WRITELOG V11']

    def __init__(self, wlData=None, wlFile=None):
        if (wlFile):
            logtext = self.readFile(wlFile,linesplit=False)
            if (logtext):
                if (self.IsThisACabFile(logtext)):
                    wlData = logtext
                else:
                    print('File %s is not a CABRILLO file.'\
                           %(wlFile))
            else:
                print('Could not read file %s'%(wlFile))
        if(wlData):
           self.newFileData=self.fixFileData(wlData)
        else:
           self.newFileData=None
           
    def fixQSO(self, qso):
        newQSO = None
        linesplit = qso.split(':')
        lineparts = len(linesplit)
        #print('%d Split data items: %s, %s'%(lineparts, linesplit[0],linesplit[1].strip()))
        qsoTag=linesplit[0].strip()
        qsoData = linesplit[1].strip()
        temp = qsoData.replace(':','')
        qsoParts = temp.split(' ')
        qsoLen = len(qsoParts)
        
        if (qsoLen >= 12):
            newQSO = '%s %s %s %s %s %s %s %s %s %s'%(\
                                                      qsoParts[0],
                                                      qsoParts[1],
                                                      qsoParts[2],
                                                      qsoParts[3],
                                                      qsoParts[4],
                                                      qsoParts[5],
                                                      qsoParts[7],
                                                      qsoParts[8],
                                                      qsoParts[9],
                                                      qsoParts[11])
        
         
        return newQSO
        
    def fixQSOList(self, qsolist):
        newList = []
        for qso in qsolist:
            newList.append(self.fixQSO(qso))
        return newList
        

    def fixFileData(self, fileData):
        retData = None
        log = self.getLogdictData(fileData)
        logApp = log['HEADER']['CREATED-BY'].strip()
        for v in self.BADLOGGERS:
            if (v in logApp):
               newQSOList = self.fixQSOList(log['QSOLIST'])
               break
        #Copy header to new string
        retData = []
        hData = fileData.splitlines()
        hIndex = 0
        addNote = True
        while not(hData[hIndex].startswith('QSO:')):
            if addNote:
                if 'SOAPBOX:' in hData[hIndex]:
                    retData.append('SOAPBOX: fixoldloggers removed obsolete seq. numbers from QSO list.')
                    addNote=False
            retData.append(hData[hIndex])
            hIndex += 1
        #Copy new QSO list
        for qso in newQSOList:
            retData.append('QSO:' + qso)
        retData.append('END-OF-LOG:')
        #print(newQSOList)
        return retData
        
