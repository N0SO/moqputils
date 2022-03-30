#!/usr/bin/env python
""" Defines contest period in UTC. 
     This will be imported by QSOUtils to set 
     contest start/stop times.
"""
from datetime import datetime
DAY1START = datetime.strptime('2022-04-02 14:00', '%Y-%m-%d %H:%M')
DAY1STOP = datetime.strptime('2022-04-03 04:00', '%Y-%m-%d %H:%M')
DAY2START = datetime.strptime('2022-04-03 14:00', '%Y-%m-%d %H:%M')
DAY2STOP = datetime.strptime('2022-04-03 20:00', '%Y-%m-%d %H:%M')

