#!/usr/bin/env python
import os, shutil, datetime
from robotconfig import *
from robotmail import *
from cabrilloutils.CabrilloUtils import *
"""
cabrillofilter.py - Parse a text file to determine if it meets
                    ARRL CABRILLO Format log file. If so, extract 
                    the CALL, NAME, ADDRESS, etc.
"""
VERSION = '1.0.1'

class CabrilloFilter(CabrilloUtils):
    def __init__(self, log=None, path=None):
        if (log or path):
            self.main(log, path)

    def getVersion(self):
        return self.VERSION
        
    def getLogData(self, cab, path):
        """
        Read the logfile data and do your best to make it a
        usage Cabrillo format file
        """
        lfile = path.lower()
        #print ('====>>>> %s\n%s\n'%(path, lfile))
        filedata = ('INCORRECT FILE TYPE - Submitted file %s is needs to be of type .LOG, .TXT or .CSV'%(path))
        if ( lfile.endswith('.log') or lfile.endswith('.txt') or lfile.endswith('.csv') ):
			filedata = cab.readFile(path)
			#print ('====>>>> filedata = %s'%(filedata))
			if (lfile.endswith('.csv') or lfile.endswith('.txt')):
				tempdata = []
				for line in filedata:
					#Replace , with (space) and remove extra white space
					tempdata += cab.packLine(line)
				filedata = tempdata
        return filedata
        
    def emailResults(self, sender, subject, Rec_by, filen, good = False, cabCall = 'BADFILE', cabFileName = 'BADFILE'):
        if (good):
            # E-mail log processors
            psubject = ('New MOQP Logfile Received from %s' % (cabCall.upper()))
            pmessage = ('CABRILLO format logfile %s received.' % (cabFileName))
            mailapp = robotMail( ROBOTSENDER, LOGPROCESSORS, psubject, pmessage )
		                         
            mailackmessage = 'Thank you for your Missouri QSO Party log submission.\n '
            mailackmessage += 'Your log has been accepted by the Log Processing Robot\n '
            mailackmessage += 'and has been forwarded to the MOQP Log Processing Team\n '
            mailackmessage += 'for scoring.\n\n'
            mailackmessage += '-- 73 de The MOQP Log Processing Robot'
            
            mailapp = robotMail( ROBOTSENDER,
                                sender,
                                'Re: Your MOQP %s Log Submission' % (Rec_by),
                                mailackmessage )
        else:
            # Inform log processors that log is being held for their review.
            mailmessage = """A new MOQP logfile was received -- I don't know how to process it:\n"""
            mailmessage += ('From: %s\nSubject: %s\nReceived by: %s\n\n' % (sender, subject, Rec_by))
            mailmessage += 'The file attached is of the wrong type or is corrupted, or the message is SPAM.\n'
            mailmessage += ('The file is saved in the humanreview folder:\nFile name: %s\n' % (filen))
            mailmessage += """Please check the robot logfile and examine the file itself to verify I have not missed a valid log file.
     
            73 de the MOQP Log Processing Robot
            """           
            mailapp = robotMail( ROBOTSENDER,
                                 LOGPROCESSORS,
                                 'New MOQP Logfile Received -- further processing is required',
                                 mailmessage)
            
        return True
    
    def main(self, logtext=None, logpath=None):
        #print('cabrillofilter (75) logtext = %s'%(logtext))
        if(logtext):
            logdict = self.getLogdictData(logtext)
        else:
            logdict = self.getLogdict(logpath)
        
        #print('cabrillofilter (81) logdict = %s'%(logdict))
        
        return logdict

    def oldmain(self, path, startfromMail,fileList):
        #for root, dirs, files in os.walk(path):
            addtodb_list = ''
            #for file in files:
            #print('=====>fileList\n%s' % (fileList))
            if (fileList == None):
                #Read list from a file
                with open('filelist.txt') as f:
                    fileList = f.read().splitlines()
            for fileEntry in fileList:
                #print('+++++++>fileEntry\n%s' % (fileEntry))
                lineEntry=fileEntry.split(',')
                #print lineEntry
                sender = lineEntry[0]
                subject = lineEntry[1]
                filen = lineEntry[2]
                cabrillofile = False # default to further processing needed
                message = 'cabrillofilter, '
                cabCall = ''
                cabFileName =''
                lfile = filen.lower()
                now = datetime.datetime.now()
                timestring = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                cab = CabrilloUtils()
                if (startfromMail):
                    Rec_by = 'EMAIL'
                else:
                    Rec_by = 'WEB'
                
                # Get logfile data    
                filedata = self.getLogData(cab, logwait + filen)
                #print filedata

                # Is this a Cabrillo log?
                if (cab.IsThisACabFile(filedata)):
                    #fetch some of the parameters to record receiveing the file
                    cabCall, cabName, cabEmail, cabAddress, cabAddCity, \
                    cabAddState, cabAddZip, cabAddCountry = cab.getCabParams(filedata)
                    if (len(cabCall) > 0):
                        cabrillofile = True
                        cabFileName = cabCall.replace('/','-')
                        cabFileName = cabFileName.replace('\\','-')
                        cabFileName = cabFileName.upper() + '.LOG'
                if (cabrillofile):
                    #Move the file to the ready for processing folder
                    shutil.move(logwait + filen, logready + cabFileName)
                    # Remove comma chars from address lines
                    cabAddress = cab.packLine(cabAddress)
                    cabAddCity = cab.packLine(cabAddCity)
                    cabAddState = cab.packLine(cabAddState)
                    cabAddZip = cab.packLine(cabAddZip)
                    cabAddCountry = cab.packLine(cabAddCountry)
                    message += ('Accepted, ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' \
                                                         % ( timestring,
                                                             Rec_by,
                                                             sender,
                                                             subject,  
                                                             cabCall.upper(), 
                                                             cabEmail,
                                                             cabName, 
                                                             cabAddress, 
                                                             cabAddCity, 
                                                             cabAddState, 
                                                             cabAddZip, 
                                                             cabAddCountry,
                                                             logwait + filen, 
                                                             logready + cabFileName))
                                                             
                    print message
                    addtodb_list += ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' \
                                                         % ( timestring,
                                                             Rec_by, 
                                                             sender,
                                                             subject, 
                                                             cabCall.upper(), 
                                                             cabEmail,
                                                             cabName, 
                                                             cabAddress, 
                                                             cabAddCity, 
                                                             cabAddState, 
                                                             cabAddZip, 
                                                             cabAddCountry,
                                                             cabFileName ))

                    # Acknowledge receipt and accceptance of file sender
                    self.emailResults(sender, subject, Rec_by, filen, 
                                              True,
                                              cabCall,
                                              cabFileName )

                else:
                    # Not a cabrillo file or cant determine op call sign -- further processing by a human needed.
                    shutil.move(path + filen, logfurther)
                    message += ('*REJECTED*, Not a CABRILLO file,%s,%s,%s.%s, , , , , , , , ,%s moved to:,%s' \
                                                         % ( timestring,
                                                             Rec_by,
                                                             sender,
                                                             subject,  
                                                             logwait + filen, 
                                                             logfurther + filen))
                                                             
                    #Tell log processors to review
                    self.emailResults(sender, subject, Rec_by, filen, good = False)
            
                    
                    print message
            open('database.txt', 'wb').write(addtodb_list) 
                        
if __name__=='__main__':
    app = CabrilloFilter(logwait)

    
