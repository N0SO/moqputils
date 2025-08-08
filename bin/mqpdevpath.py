#!/usr/bin/env python
"""
If the development module source paths exist, 
add them to the python path
"""

import os.path
import sys

whereami = os.path.split( os.path.realpath(__file__) )
pathsplit = os.path.split(whereami[0])
#print("here I am :", whereami, pathsplit)

DEVMODPATH = [pathsplit[0],
              '/home/pi/Projects/moqputils/moqputils',
              '/home/pi/Projects/moqputils',
              '/home/pi/Projects']
#os.chdir(pathsplit[0])

for mypath in DEVMODPATH:
        if (os.path.exists(mypath) and \
           (os.path.isfile(mypath) == False)):
              if (mypath not in sys.path):
                  #print(f'Adding {mypath} to sys.path...')
                  sys.path.insert(0, mypath)
              #else:
                  #print(f'{mypath} already in sys.path...')
        else:
            print(f'{mypath} does not exist or is a file...')

#print('python path = {}'.format(sys.path))
