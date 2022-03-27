#!/usr/bin/env python
import os, shutil, datetime
from robotconfig import *
from robotmail import *
from cabrilloutils.CabrilloUtils import *
"""
cabrillofilter.py - Parse a text file to determine if it meets
                    ARRL CABRILLO Format log file. If so, extract 
                    the CALL, NAME, ADDRESS, etc.
"""
VERSION = '1.0.1'

class CabrilloFilter(CabrilloUtils):
    def __init__(self, log=None, path=None):
        if (log or path):
            self.main(log, path)

    def getVersion(self):
        return self.VERSION
        
    
    def main(self, logtext=None, logpath=None):
        #print('cabrillofilter (75) logtext = %s'%(logtext))
        if(logtext):
            logdict = self.getLogdictData(logtext)
        else:
            logdict = self.getLogdict(logpath)
        
        #print('cabrillofilter (81) logdict = %s'%(logdict))
        
        return logdict


if __name__=='__main__':
    app = CabrilloFilter(logwait)

    
