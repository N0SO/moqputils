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

    def processLabel(self, place, cat, sumitem):
       tsvdata = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
                               place,cat,
                               sumitem['CALLSIGN'],
                               sumitem['OPERATORS'],
                               sumitem['NAME'],
                               sumitem['ADDRESS'],
                               sumitem['CITY'],
                               sumitem['STATEPROV'],
                               sumitem['ZIPCODE'],
                               sumitem['COUNTRY'],                               
                               sumitem['EMAIL']))
       return tsvdata
 
    def Labels_processAll(self, mydb, HEADERSTG, CATLST):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('./moqputils/configs/qrzsettings.cfg')
        tsvdata = [HEADERSTG]
        for CAT in CATLST: 
            if (isinstance(CAT, list)):
                cat = CAT[0].upper()
                catlist = CAT[1].upper()
            else:
                cat = CAT.upper()
                catlist = cat
            #print(catlist)
            sumlist = self.get_awardquery(mydb, catlist)
            if (sumlist):
                for place in range(2):
                    if place == 0:
                        placestg = 'FIRST PLACE'
                    if place == 1:
                        placestg = 'SECOND PLACE'
                    #print('{} {}'.format(placestg, len(sumlist)))
                    if len(sumlist) > place:
                        tsvline = self.processLabel(placestg, 
                                                    cat, sumlist[place])
                        if (tsvline):
                            tsvdata.append(tsvline)
            
                        if (len(sumlist[place]['OPERATORS']) > 0):
                            tempData=sumlist[place]
                            ops = sumlist[place]['OPERATORS'].split(' ')
                            if  len(ops)>1:
                                for op in ops:
                                    tempData = sumlist[place]
                                    try:
                                        opdata = qrz.callsign(op.strip())
                                        qrzdata=True
                                    except:
                                        qrzdata=False
                                        tempData['NAME']=\
                                           'NO QRZ FOR {} - {}'.format(op,len(op))
                                   
                                    if qrzdata:
                                        #print(opdata)
                                        tempData = self.swapData(\
                                               sumlist[place], 
                                               op, 
                                               opdata)
                                    tsvline = self.processLabel(placestg, 
                                                    cat, tempData)
                                    if (tsvline):
                                        tsvdata.append(tsvline)
        return tsvdata 

    def swapData(self, oldData, op, opdata):
        if ('fname' in opdata) and ('name' in opdata):
            oldData['NAME']=('{} {}, {}'.format(\
                             opdata['fname'].upper(),
                             opdata['name'].upper(),
                             op.upper()))
        elif ('attn' in opdata) and ('name' in opdata):
            oldData['NAME']=('{} ATTN {}'.format(\
                             opdata['name'].upper(),
                             opdata['att1'].upper()))
        elif ('name' in opdata):
            oldData['NAME']=('{}'.format(\
                             opdata['name'].upper()))
        else:
            oldData['NAME']=('***NO NAME FOR {} ***'.format(\
                             op.upper()))
        if('addr1' in opdata):   
            oldData['ADDRESS']=opdata['addr1'].upper()
        else:
            oldData['ADDRESS']=''
        if ('addr2' in opdata):    
            oldData['CITY'] = opdata['addr2'].upper()
        else:
            oldData['CITY'] = ''
        if('state' in opdata):
            oldData['STATEPROV'] = opdata['state'].upper()
        else:
            oldData['STATEPROV'] = ''
        if ('zip' in opdata):
            oldData['ZIPCODE'] = opdata['zip'].upper()
        else:
            oldData['ZIPCODE'] = ''
        if ('country' in opdata):    
            oldData['COUNTRY'] = opdata['country'].upper()
        else:
            oldData['COUNTRY'] = ''
        if ('email' in opdata):
            oldData['EMAIL'] = opdata['email'].upper()                       

        return oldData

    def export_to_csv(self, dblist, award):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('./moqputils/configs/qrzsettings.cfg')
        tsvlines =['CALL\tOPERATORS\tNAME\tE-MAIL\tFILE\t'+\
                    'S\tH\tO\tW\tM\tE']
        for station in dblist:
            tsvlines.append(self.processLabel(station))
            if (len(station['OPERATORS']) > 0):
                tempData=station
                ops = station['OPERATORS'].split(' ')
                if  len(ops)>1:
                    for op in ops:
                        try:
                            opdata = qrz.callsign(op.strip())
                            qrzdata=True
                        except:
                            qrzdata=False
                            tempData['NAME']=\
                               'NO QRZ FOR {} - {}'.format(op,len(op))
                       
                        if qrzdata:
                            #print(opdata)
                            tempData = self.swapData(\
                                   station, 
                                   op, 
                                   opdata)
                        tsvlines.append(self.processLabel(tempData, op))
        return tsvlines            


    def appMain(self, callsign, extra=None):
        print('commonAwards: %s, %s'%(callsign, extra))
        pass
