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

DEVMODPATH = [pathsplit[0],'/home/pi/Projects']
#print('Using DEVMODPATH=',DEVMODPATH)
os.chdir(pathsplit[0])

for mypath in DEVMODPATH:
        if ( os.path.exists(mypath) and \
          (os.path.isfile(mypath) == False) ):
            sys.path.insert(0, mypath)

#print('python path = {}'.format(sys.path))
