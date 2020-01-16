#!/usr/bin/python

import os
from moqpcategory import *
from bothawards import *

"""
ShowMe - For command line operations. 
"""
class MOQPCertificates(MOQPCategory):

    def __init__(self, pathname = None):
        if (pathname):
            self.appMain(pathname)
            
            
    def scoreFile(self, pathname, HEADER=False):
        log = self.parseLog(pathname)
        if log:
            if (log['ERRORS'] == []):
                bawards = BothAwards()
                result = (bawards.appMain(\
                           log['HEADER']['CALLSIGN'],
                           log['QSOLIST']))
                #print(result)
                if (HEADER):
                   print('STATION\tSHOWME AWARD\tS\tH\t O\tW\tM\tE\tWC\t' \
                      'MISSOURI AWARD\tM\tI\tS\tS\t O\tU\tR\tI\tWC\t' \
                      'W0MA BONUS\tK0GQ BONUS')
                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' \
                      '%s\t%s' \
                        %(log['HEADER']['CALLSIGN'],
                          result['SHOWME']['QUALIFY'],
                          result['SHOWME']['CALLS']['S'],
                          result['SHOWME']['CALLS']['H'],
                          result['SHOWME']['CALLS']['O'],
                          result['SHOWME']['CALLS']['W'],
                          result['SHOWME']['CALLS']['M'],
                          result['SHOWME']['CALLS']['E'],
                          result['SHOWME']['WILDCARD'],
                          result['MO']['QUALIFY'],
                          result['MO']['CALLS']['M'],
                          result['MO']['CALLS']['I0'],
                          result['MO']['CALLS']['S0'],
                          result['MO']['CALLS']['S1'],
                          result['MO']['CALLS']['O'],
                          result['MO']['CALLS']['U'],
                          result['MO']['CALLS']['R'],
                          result['MO']['CALLS']['I1'],
                          result['MO']['WILDCARD'],
                          result['BONUS']['W0MA'],
                          result['BONUS']['K0GQ']))
                          
            else:
                print('log file %s has errors' \
                %(pathname))
        else:
            print(\
            'File %s does not exist or is not in CABRILLO Format'\
                %(pathname))

    def scoreFileList(self, pathname):
        for (dirName, subdirList, fileList) in os.walk(pathname, 
                                                   topdown=True):
           if (fileList != ''): 
               Headers = True
               for fileName in fileList:
                   fullPath = ('%s/%s'%(dirName, fileName))
                   self.scoreFile(fullPath, Headers)
                   if (Headers): Headers = False

    def appMain(self, pathname):
        #print('Input path: %s'%(pathname))
        if (os.path.isfile(pathname)):
            self.scoreFile(pathname, HEADER = True)
        else:
            self.scoreFileList(pathname)

if __name__ == '__main__':
   app = ShowMeAward()
   """
   app._checkcall_('N0S')
   app._checkcall_('W0H')
   app._checkcall_('W0O')
   app._checkcall_('W0W')
   app._checkcall_('W0M')
   app._checkcall_('W0E')
   print(app._bingo_(app.award, SHOWMEKEYS))
   print(app.award)
   """
