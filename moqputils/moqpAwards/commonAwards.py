#!/usr/bin/python3
class commonAwards():
    
    def __init__(self, callsign = None):
        if (callsign):
            self.appMain(callsign)

    def AwardDisplay(self, AwardList):
       for line in AwardList:
           print('%s'%(line))

    def setPlacement(self, place, qdata):
       placestg = None
       rqdata = None
       qlen = len(qdata)
       if (place == '1'):
           placestg = "FIRST PLACE"
           if (qlen > 0):
               rqdata = qdata[0]
       elif (place == '2'):
           placestg = "SECOND PLACE"
           if (qlen > 1):
               rqdata = qdata[1]
       return placestg, rqdata
       

    def processHeader(self, mydb, place, cat, sumitem):
       tsvdata = '%s\t%s\t'%(place, cat)
       if (sumitem):
           if 'CLUB' in cat:
               tsvdata += '%s'%(sumitem['NAME'])
           else:
               tsvdata += ("%s\t%s\t%s"%( \
                               sumitem['NAME'],
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS']))
       else:
           tsvdata += 'NO ENTRY'
       return tsvdata
 
    def appMain(self, callsign, extra=None):
        print('commonAwards: %s, %s'%(callsign, extra))
        pass
