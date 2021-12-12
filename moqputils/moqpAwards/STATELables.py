#!/usr/bin/python3
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from moqputils.moqpawardefs import *

class STATELabels(STATEAwards):

    def ShowAward(self, mydb, place, state, sdata):

        tsvdata = '%s\t%s\t'%(place,state)
        if (sdata):     
            tsvdata += '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d'%(\
                               sdata['CALLSIGN'],
                               sdata['OPERATORS'],
                               sdata['NAME'],
                               sdata['ADDRESS'],
                               sdata['CITY'],
                               sdata['STATEPROV'],
                               sdata['ZIPCODE'],
                               sdata['COUNTRY'],                               
                               sdata['EMAIL'],
                               sdata['SCORE'])
        else:
            tsvdata += 'NO ENTRY'
        return tsvdata
