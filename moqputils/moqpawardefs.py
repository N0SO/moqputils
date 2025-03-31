#!/usr/bin/python3
CATLABELHEADER =   'RANK\tAWARD\tSTATION\tOPERATORS\t'+ \
                   'NAME\tADDRESS\tCITY\tSTATE\tZIP\t'+ \
                   'COUNTRY\tEMAIL'

STATELIST = [  ["ALABAMA","'AL','ALABAMA'"],
               ["ALASKA","'AK','ALASKA'"],
               ["ARIZONA","'AZ','ARIZONA'"],
               ["ARKANSAS","'AR','ARKANSAS'"],
               ["CALIFORNIA","'CA','EB','LAX','ORG','SBA','SCV','SDG','SF','SJV','SV','PAC'"],
               ["COLORADO","'CO','COLORADO'"],
               ["CONNECTICUT","'CT','CONNECTICUT'"],
               ["DELAWARE","'DE','DELAWARE'"],
               ["FLORIDA","'FL','FLORIDA','NFL','SFL','WCF'"],
               ["GEORGIA","'GA','GEORGIA'"],
               ["HAWAII","'HI','HAWAII'"],
               ["IDAHO","'ID','IDAHO'"],
               ["ILLINOIS","'IL','ILLINOIS'"],
               ["INDIANA","'IN','INDIANA'"],
               ["IOWA","'IA','IOWA'"],
               ["KANSAS","'KS','KANSAS'"],
               ["KENTUCKY","'KY','KENTUCKY'"],
               ["LOUISIANA","'LA','LOUISIANA'"],
               ["MAINE","'ME','MAINE'"],
               ["MARYLAND","'MD','MARYLAND'"],
               ["MASSACHUSETTS","'MA','EMA','WMA','MASSACHUSETTS'"],
               ["MICHIGAN","'MI','MICHIGAN'"],
               ["MINNESOTA","'MN','MINNESOTA'"],
               ["MISSISSIPPI","'MS','MISSISSIPPI'"],
               ["MISSOURI","'MO','MISSOURI'"],
               ["MONTANA","'MT','MONTANA'"],
               ["NEBRASKA","'NE','NEBRASKA'"],
               ["NEVADA","'NV','NEVADA'"],
               ["NEW HAMPSHIRE","'NH','NEW HAMPSHIRE'"],
               ["NEW JERSEY","'NJ','NNJ','SNJ','NEW JERSEY'"],
               ["NEW MEXICO","'NM','NEW MEXICO'"],
               ["NEW YORK","'NY','ENY','NLI','NNY','WNY','NEW YORK'"],
               ["NORTH CAROLINA","'NC','NORTH CAROLINA'"],
               ["NORTH DAKOTA","'ND','NORTH DAKOTA'"],
               ["OHIO","'OH','OHIO'"],
               ["OKLAHOMA","'OK','OKLAHOMA'"],
               ["OREGON","'OR','OREGON'"],
               ["MAINE","'ME','MAINE'"],
               ["PENNSYLVANIA","'PA','EPA','WPA','PENNSYLVANIA'"],
               ["RHODE ISLAND","'RI','RHODE ISLAND'"],
               ["SOUTH CAROLINA","'SC','SOUTH CAROLINA'"],
               ["SOUTH DAKOTA","'SD','SOUTH DAKOTA'"],
               ["TENNESSEE","'TN','TENNESSEE'"],
               ["TEXAS","'TX','TEXAS'"],
               ["UTAH","'UT','UTAH'"],
               ["VIRGINIA","'VA','VIRGINIA'"],
               ["VERMONT","'VT','VERMONT'"],
               ["WASHINGTON","'WA','EWA','WWA','WASHINGTON'"],
               ["WEST VIRGINIA","'WV','WEST VIRGINIA'"],
               ["WISCONSIN","'WI','WISCONSIN'"],
               ["WYOMING","'WY','WYOMING'"],
               ["ALBERTA","'AB','ALBERTA'"],
               ["BRITISH COLUMBIA","'BC','BRITISH COLUMBIA'"],
               ["MANITOBA","'MB','MANITOBA'"],
               ["NEW BRUNSWICK","'NB','NEW BRUNSWICK'"],
               ["NEWFOUNDLAND","'NL','NEWFOUNDLAND','LABRADOR'"],
               ["NOVA SCOTIA","'NS','NOVA SCOTIA'"],
               ["ONTARIO","'ON','ONS','ONN','ONTARIO'"],
               ["PRINCE EDWARD ISLAND","'PE','PRINCE EDWARD ISLAND'"],
               ["QUEBEC","'QC','QUEBEC'"],
               ["SASKATCHEWAN","'SK','SASKATCHEWAN'"],
               ["NORTHWEST TERRITORIES","'NT','NORTHWEST TERRITORIES'"],
               ["NUNAVUT","'NU','NUNAVUT'"],
               ["YUKON","'YT','YUKON'"] ]

PLAQUELIST = [ ["MISSOURI FIXED MULTI-OP","'MISSOURI FIXED MULTI-OP'"],
    ["MISSOURI FIXED SINGLE-OP HIGH POWER",
                   "'MISSOURI FIXED SINGLE-OP HIGH POWER'"],
    ["MISSOURI FIXED SINGLE-OP LOW POWER", 
                   "'MISSOURI FIXED SINGLE-OP LOW POWER'"],
    ["MISSOURI FIXED SINGLE-OP QRP POWER",
                   "'MISSOURI FIXED SINGLE-OP QRP POWER'"],
    ["MISSOURI EXPEDITION", 
               "'MISSOURI EXPEDITION', "+\
               "'MISSOURI EXPEDITION MULTI-OP', "+\
               "'MISSOURI EXPEDITION SINGLE-OP HIGH POWER', "+\
               "'MISSOURI EXPEDITION SINGLE-OP LOW POWER', "+\
               "'MISSOURI EXPEDITION SINGLE-OP QRP POWER'"],
    ["MISSOURI MOBILE UNLIMITED", "'MISSOURI MOBILE UNLIMITED'"],
    ["MISSOURI MOBILE MULTI-OP",
                 "'MISSOURI MOBILE MULTI-OP', "+\
                 "'MISSOURI MOBILE MULTI-OP LOW POWER', "+\
                 "'MISSOURI MOBILE MULTI-OP LOW POWER MIXED'"],
    ["MISSOURI MOBILE SINGLE-OP LOW POWER MIXED",
                 "'MISSOURI MOBILE SINGLE-OP LOW POWER', "+\
                 "'MISSOURI MOBILE SINGLE-OP LOW POWER MIXED'"],
    ["MISSOURI MOBILE SINGLE-OP LOW POWER CW",
                 "'MISSOURI MOBILE SINGLE-OP LOW POWER CW'"],
    ["MISSOURI MOBILE SINGLE-OP LOW POWER PHONE", 
                 "'MISSOURI MOBILE SINGLE-OP LOW POWER PHONE'"],
    ["US SINGLE OPERATOR HIGH POWER",
                 "'US SINGLE OPERATOR HIGH POWER', "+\
                 "'US SINGLE-OP HIGH POWER'"],
    ["US SINGLE OPERATOR LOW POWER",
                 "'US SINGLE OPERATOR LOW POWER', "+\
                 "'US SINGLE-OP LOW POWER'"],
    ["US SINGLE OPERATOR QRP POWER",
                 "'US SINGLE OPERATOR QRP POWER', "+\
                 "'US SINGLE-OP QRP POWER'"],
    ["DX","'DX'"],
    ["MISSOURI ROOKIE", 
                      "'MISSOURI ROOKIE', 'ROOKIE'"],
    ["MISSOURI SCHOOL CLUB", 
                       "'MISSOURI SCHOOL CLUB'"],
    ["HIGHEST DIGITAL","'HIGHEST DIGITAL', "+\
                       "'MISSOURI HIGHEST DIGITAL'"],
    ["HIGHEST NUMBER OF COUNTIES",
                        "'HIGHEST NUMBER OF COUNTIES'"] ]

ADDITIONALFIRST = [\
    'MISSOURI EXPEDITION MULTI-OP',
    'MISSOURI EXPEDITION SINGLE-OP HIGH POWER',
    'MISSOURI EXPEDITION SINGLE-OP LOW POWER',
    'MISSOURI EXPEDITION SINGLE-OP QRP POWER',
    'US MULTI-OP',
    'CANADA',
    'MISSOURI CLUB',
    'NON-MISSOURI HIGHEST DIGITAL',
    'MISSOURI VHF',
    'NON-MISSOURI VHF' ]

AWARDLIST = [\
    'MISSOURI FIXED MULTI-OP',
    'MISSOURI FIXED SINGLE-OP HIGH POWER',
    'MISSOURI FIXED SINGLE-OP LOW POWER',
    'MISSOURI FIXED SINGLE-OP QRP POWER',
    'MISSOURI EXPEDITION MULTI-OP',
    'MISSOURI EXPEDITION SINGLE-OP HIGH POWER',
    'MISSOURI EXPEDITION SINGLE-OP LOW POWER',
    'MISSOURI EXPEDITION SINGLE-OP QRP POWER',
    'MISSOURI MOBILE UNLIMITED',
    'MISSOURI MOBILE MULTI-OP',
    'MISSOURI MOBILE SINGLE-OP LOW POWER MIXED',
    'MISSOURI MOBILE SINGLE-OP LOW POWER CW',
    'MISSOURI MOBILE SINGLE-OP LOW POWER PHONE',
    'US SINGLE-OP HIGH POWER',
    'US SINGLE-OP LOW POWER',
    'US SINGLE-OP QRP POWER',
    'US MULTI-OP',
    'CANADA',
    'DX',
    'CHECKLOG']

if __name__ == '__main__':
    """ For testing only """
    print("\nSTATELIST len = {}".format(len(STATELIST)))
    for state in STATELIST:
        print('{}\n\t{}'.format(state[0], state[1]))

    print('\nAWARDLIST len = {}'.format(len(AWARDLIST)))
    for award in AWARDLIST:
        print('{}'.format(award))

    print('\nPLAQUELIST len = {}'.format(len(PLAQUELIST)))
    for plaque in PLAQUELIST:
        print('{}\n\t{}'.format(plaque[0], plaque[1]))
