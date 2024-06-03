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
       
    def processOneLine(self, cat):
        formatStg = \
             '{} PLACE\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'
        placestg=''
        if cat['place']==1:
            placestg='FIRST'
        if cat['place']==2:
            placestg = 'SECOND'
        
        tsvdata = (formatStg.format(\
                      placestg,
                      cat['award'],
                      cat['callsign'],
                      cat['operators'],
                      cat['name'],
                      cat['address'],
                      cat['city'],
                      cat['state'],
                      cat['zip'],
                      cat['country'],
                      cat['email'],
                      cat['plaque']))
        return tsvdata
 
    def new_processAll(self, HEADERSTG, CATLIST):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('/home/pi/Projects/moqputils/moqputils/configs/qrzsettings.cfg')
        tsvdata = [HEADERSTG]
        for cat in CATLIST:
            #print (cat)
            ops=[]
            if cat['operators']!= None:
                ops = cat['operators'].split(' ')
            #print('Number of ops={}, {}'.format(len(ops), ops))
            if (len(ops)>1): #Multi-op
                for op in ops:
                    #print('op {} of ops {}'.format(op, ops))
                    tempData = cat
                    try:
                        opdata = qrz.callsign(op.strip())
                        #print('Op Data for {} = {}'.format(op, opdata))
                        qrzdata=True
                    except:
                        qrzdata=False
                        tempData['name']=\
                            'NO QRZ FOR {} - {}'.format(op,len(op))
                        #print('No QRZ for {}'.format(op))           
                    if qrzdata:
                        #print(opdata)
                        tempData = self.swapData(\
                                               cat, 
                                               op, 
                                               opdata)
                    tsvdata.append(self.processOneLine(tempData))
            else: #Single-op
                tsvdata.append(self.processOneLine(cat))
        return tsvdata


    def Labels_processAll(self, mydb, HEADERSTG, CATLST):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('/home/pi/Projects/moqputils/moqputils/configs/qrzsettings.cfg')
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
                        ops = sumlist[place]['OPERATORS'].split(' ')
                        if (len(ops)>1): #Multi-op
                            #tempData=sumlist[place]
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
                        else: #Single-op
                            if sumlist[place]['OPERATORS'] == \
                                     sumlist[place]['CALLSIGN']:
                                #Single-op using own call
                                sumlist[place]['OPERATORS'] = ''
                            tsvline = self.processLabel(placestg, 
                                                    cat, sumlist[place])
                            if (tsvline):
                                tsvdata.append(tsvline)
        return tsvdata 

    def swapData(self, oldData, op, opdata):
        if ('fname' in opdata) and ('name' in opdata):
            oldData['name']=('{} {}, {}'.format(\
                             opdata['fname'].upper(),
                             opdata['name'].upper(),
                             op.upper()))
        elif ('attn' in opdata) and ('name' in opdata):
            oldData['name']=('{} ATTN {}'.format(\
                             opdata['name'].upper(),
                             opdata['att1'].upper()))
        elif ('name' in opdata):
            oldData['name']=('{}'.format(\
                             opdata['name'].upper()))
        else:
            oldData['name']=('***NO NAME FOR {} ***'.format(\
                             op.upper()))
        if('addr1' in opdata):   
            oldData['address']=opdata['addr1'].upper()
        else:
            oldData['address']=''
        if ('addr2' in opdata):    
            oldData['city'] = opdata['addr2'].upper()
        else:
            oldData['city'] = ''
        if('state' in opdata):
            oldData['state'] = opdata['state'].upper()
        else:
            oldData['state'] = ''
        if ('zip' in opdata):
            oldData['zip'] = opdata['zip'].upper()
        else:
            oldData['zip'] = ''
        if ('country' in opdata):    
            oldData['country'] = opdata['country'].upper()
        else:
            oldData['COUNTRY'] = ''
        if ('email' in opdata):
            oldData['email'] = opdata['email'].upper()                       

        return oldData

    def export_to_csv(self, dblist, award):
        from qrzutils.qrz.qrzlookup import QRZLookup
        qrz=QRZLookup('/home/pi/Projects/moqputils/moqputils/configs/qrzsettings.cfg')
        if award=='SHOWME':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'S\tH\tO\tW\tM\tE\tWC']
        elif award=='MISSOURI':
            tsvlines =['CALL\tOPERATORS\tNAME\tADDRESS\tCITY\t'+\
                    'STATE\tZIP\tCOUNTRY\tE-MAIL\tFILE\t'+\
                    'M\tI\tS\tS\tO\tU\tR\tI\tWC']
            
        for station in dblist:
            if len(station['OPERATORS']) > 0:
                ops = station['OPERATORS'].split(' ')
                if len(ops) > 1: #Multi-op station
                    tempData = station
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
                    
                else: #Single-op station
                    if station['CALLSIGN'] == station['OPERATORS']:
                        station['OPERATORS'] = ''
                    tsvlines.append(self.processLabel(station))
        return tsvlines            


    def appMain(self, callsign, extra=None):
        print('commonAwards: %s, %s'%(callsign, extra))
        pass
