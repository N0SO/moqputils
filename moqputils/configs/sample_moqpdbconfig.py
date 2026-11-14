#!/usr/bin/python
# Replace the items below with your database:
#   server name,
#   user name,
#   password, and
#   Database name
#
#          Reco
#   Rename to:
#      contestyear_moqpdbconfig.py 
#   then then create a symlink from that file
#   to moqpdbconfig.py
# DO NOT ADD FILES WITH YOUR SERVER INFO TO
# GITHUB. It's hard to undo. (Ask me how I know).
#
HOSTNAME = 'yourhost'
USER = 'youruser'
PW = 'yourpassword'
YEAR='2027'
DBNAME = f'YOURPREFIX_{YEAR}'

"""Check for good parameters if run from CL"""
if __name__ == '__main__':
	print(f'{HOSTNAME=}\n{USER=}\n{PW=}\n{YEAR=}\n{DBNAME=}')


