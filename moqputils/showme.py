#!/usr/bin/python
"""
ShowMe  - Determine which Missouri QSO Party stations 
          qualify for the ShowMe and/or MISSOURI awards

Update History:
* Thu Dec 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start of work
"""

from moqpcategory import *
import os



class ShowMe(MOQPCategory):

    

    def __init__(self, filename = None):
        if (filename):
           if (filename):
              self.appMain(filename)

    def appMain(self, pathname):
        print('Input path: %s'%(pathname))
        
    