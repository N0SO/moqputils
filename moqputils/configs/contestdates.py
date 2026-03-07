#!/usr/bin/env python
""" Defines contest period in UTC. 
     This will be imported by QSOUtils to set 
     contest start/stop times.
"""
from datetime import datetime
DAY1START = datetime.strptime('2026-04-11 14:00', '%Y-%m-%d %H:%M')
DAY1STOP = datetime.strptime('2026-04-12 04:00', '%Y-%m-%d %H:%M')
DAY2START = datetime.strptime('2026-04-12 14:00', '%Y-%m-%d %H:%M')
DAY2STOP = datetime.strptime('2026-04-12 20:00', '%Y-%m-%d %H:%M')
"""
print('Using contest dates:\n{} - {}\n{} - {}'.format(DAY1START,
                                                      DAY1STOP,
                                                      DAY2START,
                                                      DAY2STOP))

"""
