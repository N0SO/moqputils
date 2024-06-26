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

CANADA = 'MAR NL QC ONE ONN ONS GTA MB SK AB BC NT NB PE'

STATIONS = ['FIXED', 'MOBILE','PORTABLE', 'ROVER','EXPEDITION',
            'HQ','SCHOOL']
DIGIMODES = ['RY', 'DG', 'DIG', 'DIGI', 'RTTY', 'FT8', 'FT4']
MODES2 = ['PH', 'PHONE', 'SSB', 'USB', 'LSB', 'FM', 'DV']
MODES3 = ['CW', 'RY', 'DG', 'DIG', 'DIGI', 'RTTY',
          'FT8', 'FT4']
MODES = ['PH', 'SSB', 'USB', 'LSB', 'FM', 'DV',
         'CW', 'RY', 'DG', 'DIG', 'DIGI', 'RTTY',
         'FT8', 'FT4', 'MIXED']
         
CTMODE = ['CW', 'PHONE', 'SSB', 'MIXED', 'DIGITAL', 'CW+DIGITAL',
          'PHONE+DIGITAL',
          'MIXED+DIGITAL']
         
CTOPERATOR = ['SINGLE-OP', 'MULTI-OP', 'CHECKLOG']

CTSTATION = [\
              'FIXED',
              'MOBILE',
              'EXPEDITION',
              'UNLIMITED',
              'MOBILE-UNLIMITED',
              'SCHOOL',
              'DISTRIBUTED',
              'ROVER',
              'PORTABLE'\
              ]

CTPOWER = ['LOW', 'HIGH', 'QRP']



OVERLAY = 'ROOKIE'

US = \
'CT EMA ME NH RI VT WMA ENY NLI NNJ NNY SNJ WNY DE EPA MDC WPA '+\
'AL GA KY NC NFL SC SFL WCF TN VA PR VI AR LA MS NM NTX OK STX '+\
'WTX EB LAX ORG SB SCV SDG SF SJV SV PAC AZ EWA ID MT NV OR UT '+\
'WWA WY AK MI OH WV IL IN WI CO IA KS MN NE ND SD CA HI'

DX = 'DX DK2 DL3 DL8 DM3 EA4 F5 F8 HA8 JE2 JO7 LY5 OK1 OK4 OL2 '+\
     'ON4 OM2 OM3 OT6 IZ4 YV5 '+\
     'HA9 HB9 RZ1 SM3 UA3 WP4 '+\
     '9A3 VP8 F4 PA3 G0 LA8 '+\
     'ZF2 SN3 S51 SN7 SP1 SQ4 SN2 SP8 VP2 HP6 CE4 LU3 LU5 NP3 T10 '+\
     'RW3 EA3 IZ5 OD2 SP5 PY3 TO60 CT9 AO75 '

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
                'TOTAL\tMULTS\tW0MA\tK0GQ\tCAB FILE\tSCORE\tDUPES\t' + \
                'SHOWME\tMISSOURI\t' + \
                'MOQP CATEGORY\tDIGITAL\tVHF\tROOKIE\n'
