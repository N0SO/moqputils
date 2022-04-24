#!/usr/bin/env python
"""
Update History:
* Sat Apr 23 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 -First interation for 2021 MOQP.
"""

DESCRIPTION = \
"""makehtml.py  - Generates an html table of certificate winners based
		  on two list files provided as inputs:
                     -f --file_list - A list of certificate file names.
		     -c --call_list - A list of callsigns and operators.
		  The resulting html table is intended to be copy/pasted
		  into a SHOWME or MISSOURI report for the web page.
"""

EPILOG = \
"""
Running with no parameters will launch the GUI.
"""

import os, sys, argparse
VERSION = '0.0.1'
ARGS = None

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser(\
                               description = DESCRIPTION,
                                           epilog = EPILOG)
        parser.add_argument('-v', '--version', 
                                  action='version', 
                                  version = VERSION)
        parser.add_argument('-f', '--file_list',
                                   #action='store_true',
                                   default=None,
            help="""The file containing the list of certificate file
	            names. The list should be ordered to match the list
		    of station callsigns and operators passed as -c or 
		    --call_list.""")
        parser.add_argument('-c', '--call_list',
                                   default=None,
            help="""The file containing the list of STATIONS and OPERATORS.
	            This is expected to be the output of the mqpawards -s or
		    mqpawards -m command. The callsign/operator list must
		    be ordered to match the list of certificate files list
		    passed as -f or --file_list.""")

        args = parser.parse_args()
        print(args)
        return args

args=get_args()

if (args.args.file_list==None) or (args.args.call_list==None):
	exit()

with open(args.args.file_list) as f:
	lines=f.readlines()

with open(args.args.call_list) as f:
        calls=f.readlines()
	
i=0
print('<table>')
print('<tr><th>STATION</th><th>OPERATORS</th><AWARD DOWNLOAD LINK</th></tr>')
for line in lines:
        if line != '':
	    callparts =calls[i].split('\t')
            if len(callparts)>=3:
                print('<tr><td>%s</td><td>%s</td><td><a href="./%s">DOWNLOAD</td></tr>' \
		            %(callparts[1].strip(),
			      callparts[2].strip(),
			      line.strip()))
        i += 1
print('</table>')	
	
