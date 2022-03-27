#!/usr/bin/env python
"""
emailrobot - Process Missouri QSO Party log files received as 
             e-mail attachments.

This program will read e-mail from the e-mail account defined in 
robotconfig.py, then process the attached files. It calls 
cabrillofilter.py to verify the integrety of the Cabrillo format
log file, and to pull data about the station and submitter for
inclusion in the MOQP database file defined in robotconfig.py.

This script is intended to be called from the cron daemon to periodically
check for new logs, but could be triggered from a web browser as well.

Update History:
* Sat Mar 26 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V2.0.0 - Support for Python SQL functions added to w0ma.org server.
-          This app was refactored to eliminate the need for calling
-          a PHP script to perform the SQL functions.
-          Also, fixes for issues #11, #12, #13, #14, and a partial
-          for #15. 15 could use some refinement for further sorting
-          of excel and pdf docs.

"""
import getpass, imaplib, smtplib, os, email, string, datetime
import mysql.connector
from robotconfig import *
from cabrillofilter import *
from robotmail import *
from email.mime.text import MIMEText

VERSION = '2.0.0'
ERRORINLOG = "Error! attached log is NOT a plain text file!"
CTYPES = ['text/x-log',
          'application/octet-stream',
          'text/plain','application/pdf',
          'application/vnd.ms-excel',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

class emailRobot():

   def __init__(self, auto=False):
      if(auto):
          self.main()
     
   def getVersion(self):
      return self.VERSION
      
   def connect(self):
      M = imaplib.IMAP4_SSL(imap_host,'993')
      M.login(imap_user, imap_pass)
      return M

   def close(self, M):
      M.close()
      M.logout()
      
   def process_message_string(self, s):
      mail = email.message_from_string(s[0][1])
      
      """
      #For debuging...
      print(dir(mail))
      print(mail['values'])
      print(mail['items'])
      print(mail['Body'])
      """
      sender = mail["From"]
      replyto = mail["Reply-To"]
      subject = mail["Subject"]
      date =  mail["Date"]
      log = None
      nametype = None
      fname = None
      method = None
      
      mailparts = dict()
      mailparts['sender'] = mail["From"]
      mailparts['replyto'] = mail["Reply-To"]
      mailparts['subject'] = mail["Subject"]
      mailparts['date'] =  mail["Date"]

      if mail.is_multipart():
         #print"multi---"
         pcount = 0
         for part in mail.walk():
            pcount += 1
            fname = part.get_filename()
            ctype = part.get_content_type()
            log = part.get_payload(decode=True)
            #print ('Multi part %d - CTYPE = %s\nPayload = %s'%(pcount, ctype, log))
            if (fname != None):
               for c in '/\\ ,':
                  fname = fname.replace(c,'-')
               #fname = fname.replace('/','_')
               #fname = fname.replace('\\','_')
               #fname = fname.replace(' ','-')
               if ctype in CTYPES:
                  #print("\nctype = %s\nfile name = %s\n"%(ctype, fname))
                  log = part.get_payload(decode=True)
                  #Gets file extension from filename
                  tmparry = fname.split('.')
                  if (len(tmparry) >1):
                     nametype = tmparry[len(tmparry) - 1]  # gets file extension
                  else:
                     if (fname.startswith('=?UTF-8')):
                        nametype = '.UTF'
                     else:
                        nametype = '.DAT'
                     fname += nametype
                  break
      else:
         #print "Not multi--"
         log = mail.get_payload()
      
      mailparts['log'] = log
      mailparts['nametype'] = nametype
      mailparts['fname'] = fname
      if ('MOQP WEB' in mailparts['subject']):
          mailparts['method'] = 'WEB'
      else:
          mailparts['method'] = 'EMAIL'
      #print sender, subject, date, nametype   
      #return sender, subject, date, fname, nametype, log, replyto, mailparts
      return mailparts
        
   def createDBEntry(self, status, msgparts, logdict):
       cnx = mysql.connector.connect(user=dbusername, password=dbpassword, 
                                     host=dbhostname, database=dbname)
       timestring = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
       curser=cnx.cursor(prepared=True)
       query = """INSERT INTO logs_received 
                            (STA_CALL,
	      					 OP_NAME,
	      					 EMAIL,
	                         RECEIVED_BY,
	                         FILENAME,
	                         DATE_REC,
	                         EMAILSUBJ)	
	       
	             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
       params = (logdict['HEADER']['CALLSIGN'],
	            logdict['HEADER']['NAME'],
	            msgparts['replyto'],
	            msgparts['method'],
	            msgparts['fname'],
	            timestring,
	            msgparts['subject'])
	                    
       #print('query = %s'%(query))
       curser.execute(query, params)
       cnx.commit()
       cnx.close()

   def main(self):
      mailSender = robotMail() # For sending results to recipients and senders
      M = self.connect()
      M.select('INBOX')
      typ, data = M.search(None, 'unseen')
      msgs = data[0].split()
      newfiles = []
      for uid in msgs:
         if(len(uid) > 0):
             print('--------\nrobotmail: %s'% \
                (datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S-%f")))
             print('robotmail: Processing message uid: %s'%(uid))
         typ, s = M.fetch(uid, '(RFC822)')

         """
         print ('typ = %s\n'%(typ))
         print "s = ",s
         """

         msgparts = self.process_message_string(s)
         print ("Sender = %s\nReply-To = %s\nSubject = %s\nFile name = %s\nFile Type = %s\n"%(msgparts['sender'], 
                           msgparts['replyto'], 
                           msgparts['subject'], 
                           msgparts['fname'], 
                           msgparts['nametype']))
         if ( (msgparts['replyto'] == None) or (len(msgparts['replyto'])<3) ):
             """Reply-to address does not exist, use sender address
                Fix for issue #11"""
             msgparts['replyto']=msgparts['sender']
         #print('msgparts = %s'%(msgparts))
         status = 'e-mail robot, '         
         if (msgparts['fname'] != None):
         
             cabFilter = CabrilloFilter()
             logdict = cabFilter.main(msgparts['log'])
             #print('emailrobot: logdict (285) =%s'%(logdict) )
             if (logdict):
                 logcall=cabFilter.stripCallsign(logdict['HEADER']['CALLSIGN'])
                 logemail=logdict['HEADER']['EMAIL']
                 print('emailrobot(291):\nlogcall=%s\nlogemail=%s\n'%(logcall, logemail))
                 msgparts['fname']=logcall.upper()+'.LOG'
                 open(logready + msgparts['fname'], 'wb').writelines(msgparts['log'])
                 status += 'Accepted, ,'

             else:
                 #Not a CAB file, but may be PDF, CSV or other type
                 #Need code here to sort PDFs, CSVs, XLS, etc.
                 nameparts= os.path.splitext(msgparts['fname'])
                 filetype = nameparts[1].upper()
                 if (nameparts[1].upper() in ('.CSV','.PDF','.XLS','.XLSX')):
                     open(logwait + msgparts['fname'], 'wb').writelines(msgparts['log'])
                     status += '*WAITING*, for human action, '
                 else:
                     open(logfurther + msgparts['fname'], 'wb').writelines(msgparts['log'])
                     status += '*REJECTED*, unknown file type ['+filetype+'], '
                     
         else:
             status += '*REJECTED*, No logfile, '   
         print('%s ,"%s", "%s", "%s", %s, %s\n--------' \
                    % (status, 
                       msgparts['date'], 
                       msgparts['sender'], 
                       msgparts['subject'], 
                       msgparts['nametype'], 
                       msgparts['fname']))

         if ('*REJECTED*' in status):
            mailSender.process_bademail(msgparts['replyto'], 
                                        msgparts['subject'], 
                                        msgparts['date'])
         elif ('*WAITING*' in status):
             """Send messages to sender/log processors the file 
                needs attention.
                Code TBD."""
             mailSender.emailResults(msgparts, logdict)
         elif ('Accepted' in status):
             """Write log specifics to logs received DB and
                send messages to sender/log processors"""
             self.createDBEntry(status, msgparts, logdict)
             mailSender.emailResults(msgparts, logdict)
if __name__=='__main__':
    mailbot = emailRobot(True)
