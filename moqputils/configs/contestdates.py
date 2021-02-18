#!/usr/bin/python
""" Defines contest period in UTC. 
     This will be imported by QSOUtils to set 
     contest start/stop times.
"""
from datetime import datetime
DAY1START = datetime.strptime('2020-04-04 14:00', '%Y-%m-%d %H:%M')
DAY1STOP = datetime.strptime('2020-04-05 04:00', '%Y-%m-%d %H:%M')
DAY2START = datetime.strptime('2020-04-05 14:00', '%Y-%m-%d %H:%M')
DAY2STOP = datetime.strptime('2020-04-05 20:00', '%Y-%m-%d %H:%M')

