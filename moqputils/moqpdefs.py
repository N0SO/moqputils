#!/usr/bin/env python3
"""
moqpdefs - Some standard MOQP definitions for Missouri counties,
           states, Canadian provinces, etc.
           
"""

CONTEST =['MISSOURI QSO PARTY', 
          'MOQP', 
          'MQP',
          'MO-QSO-PARTY',
          'MO QSO PARTY']

INSTATE = ['MO', 'MISSOURI']

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT NB'

STATIONS = ['FIXED', 'MOBILE','PORTABLE', 'ROVER','EXPEDITION',
            'HQ','SCHOOL']
DIGIMODES = ['RY', 'DG', 'DIG', 'DIGI', 'RTTY']
MODES2 = ['PH', 'SSB', 'USB', 'LSB', 'FM', 'DV']
MODES3 = ['CW', 'RY', 'DG', 'DIG', 'DIGI', 'RTTY'] 
MODES = ['PH', 'SSB', 'USB', 'LSB', 'FM', 'DV',
         'CW', 'RY', 'DG', 'DIG', 'DIGI', 'RTTY', 
         'MIXED']

OVERLAY = 'ROOKIE'

US = \
'CT EMA ME NH RI VT WMA ENY NLI NNJ NNY SNJ WNY DE EPA MDC WPA '+\
'AL GA KY NC NFL SC SFL WCF TN VA PR VI AR LA MS NM NTX OK STX '+\
'WTX EB LAX ORG SB SCV SDG SF SJV SV PAC AZ EWA ID MT NV OR UT '+\
'WWA WY AK MI OH WV IL IN WI CO IA KS MN NE ND SD CA HI'

DX = 'DX DK2 DL8 HA8 ON4'

MOCOUNTY = [ 'ADR', 'AND', 'ATC', 'AUD', 'BAR', 'BTN', 'BAT', 
             'BEN', 'BOL', 'BOO', 'BUC', 'BTR', 'CWL', 'CAL', 
             'CAM', 'CPG', 'CRL', 'CAR', 'CAS', 'CED', 'CHN', 
             'CHR', 'CLK', 'CLA', 'CLN', 'COL', 'COP', 'CRA', 
             'DAD', 'DAL', 'DVS', 'DEK', 'DEN', 'DGL', 'DUN', 
             'FRA', 'GAS', 'GEN', 'GRN', 'GRU', 'HAR', 'HEN', 
             'HIC', 'HLT', 'HOW', 'HWL', 'IRN', 'JAC', 'JAS', 
             'JEF', 'JON', 'KNX', 'LAC', 'LAF', 'LAW', 'LEW', 
             'LCN', 'LIN', 'LIV', 'MAC', 'MAD', 'MRE', 'MAR', 
             'MCD', 'MER', 'MIL', 'MIS', 'MNT', 'MON', 'MGM', 
             'MOR', 'NMD', 'NWT', 'NOD', 'ORE', 'OSA', 'OZA', 
             'PEM', 'PER', 'PET', 'PHE', 'PIK', 'PLA', 'POL', 
             'PUL', 'PUT', 'RAL', 'RAN', 'RAY', 'REY', 'RIP', 
             'SAL', 'SCH', 'SCT', 'SCO', 'SHA', 'SHL', 'STC', 
             'SCL', 'STF', 'STG', 'STL', 'SLC', 'STD', 'STN', 
             'SUL', 'TAN', 'TEX', 'VRN', 'WAR', 'WAS', 'WAY', 
             'WEB', 'WOR', 'WRT' ]

COLUMNHEADERS = 'LOG ERRORS\tCALLSIGN\tOPS\tSTATION\tOPERATOR\t'+\
                'POWER\tMODE\tLOCATION\tOVERLAY\t' + \
                'CW QSO\tPH QSO\tRY QSO\tVHF QSO\t' + \
                'TOTAL\tMULTS\tW0MA\tK0GQ\tCAB FILE\tSCORE\tERRORS\tDUPES\t' + \
                'MOQP CATEGORY\tDIGITAL\tVHF\tROOKIE\n'
