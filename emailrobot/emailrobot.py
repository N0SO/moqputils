#!/usr/bin/python
"""
emailrobot - Process Missouri QSO Party log files received as 
             e-mail attachments.

This program will read e-mail from the e-mail account defined in 
robotconfig.py, then process the attached files. It calls 
cabrillofilter.py to verify the integrety of the Cabrillo format
log file, and to pull data about the station and submitter for
inclusion in the MOQP database file defined in robotconfig.py.

This script is called with an exec() statement from emailrobot.php.
emailrobot.php writes the data to the SQL database -- I could never
get the SQL functions to work on w0ma.org via python.
"""
import getpass, imaplib, smtplib, os, email, datetime, string
from robotconfig import *
from cabrillofilter import *
from email.mime.text import MIMEText

VERSION = '1.0.3'
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
      
      sender = mail["From"]
      subject = mail["Subject"]
      date =  mail["Date"]
      log = None
      nametype = None
      fname = None

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
      
      #print sender, subject, date, nametype   
      return sender, subject, date, fname, nametype, log
      
   def saveLog(self, filename, logdata, filetype):
      now = datetime.datetime.now()
      timestring = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S-%f")
      logfilename = timestring + '-' + filename
      logfilename = logfilename.lower()
      if (logfilename.endswith('.csv')):
          tempdata = ''
          for line in logdata:
              tempdata += line.replace(',',' ')
          logdata = tempdata
      #open(logwait + logfilename, 'wb').write(logdata) # Save for log processing
      #print(os.getcwd())
      if ( open(logwait + logfilename, 'wb').writelines(logdata) ):
         return "!!!UNABLE TO SAVE LOGFILE!!!"
      else:
         return logfilename
         
   def createDBEntry(self, sender, subject, date, logname):
      # Open database connection
      db = MySQLdb.connect(dbhostname,dbusername,dbpassword,dbname )

      # prepare a cursor object using cursor() method
      cursor = db.cursor()

      # Prepare SQL query to INSERT a record into the database.
      sql = "INSERT INTO logs_received(STA_CALL, EMAIL, \
                                       RECEIVED_BY, FILENAME, \
                                       DATE_REC) \
                         VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
                                ('TE0ST', sender,'EMAIL', logname, date)
      try:
         # Execute the SQL command
         cursor.execute(sql)
         print "DB Success!"
         db.commit()
      except:
         # Rollback in case there is any error
         print "Error writing data to database!"
         db.rollback()

      # disconnect from server
      db.close()
      

   def extract_call(self, s):
      call = ""
      count = 0
      hasletters = 0
      hasnumbers = 0

      for c in s:
         if (c in string.digits):
            call += c
            hasnumbers += 1
         elif (c in string.letters):
            call += c
            hasletters += 1
         else:
            if (count < 3):
               call = "INVALID"
            break

         count += 1
         if (count >= 8):
            break

      if ( (hasletters == 0) or (hasnumbers == 0) ):
         call = "INVALID"

      if (call != "INVALID"):
         call = call.upper()

      #print "s= {0}, call = {1}, count = {2}, hasletters ={3}, hasnumbers={4}".format(s, call, count, hasletters, hasnumbers)

      return call

   def sendrobotmail(self, to, subject, body):
      msg = MIMEText(body)
      msg['Subject'] = subject
      msg['From'] = ROBOTSENDER
      msg['To'] = to
      try:
         smtpObj = smtplib.SMTP(imap_host, 25)
         smtpObj.login(imap_user, imap_pass)
         smtpObj.sendmail(ROBOTSENDER, to, msg.as_string())         
      except:
         print "Error: unable to send email"

   def process_goodlog(self, sender, subject, savedlog):
      #self.createDBEntry(logname, subject, timerec, savedlog)
      #print 'SUCCESS!,; {0},; {1},; {2},; {3}'.format(logname, sender, timerec, savedlog)
      # e-mail the log processing team to let them know a new log is available
#      message = 'A new logfile has been received via e-mail:\nFrom: {0}\nSubject: {1}\nDate: {2}, Logfile Name: {3}, Date/time received:{4}\n'.format(sender, subject, date, savedlog, timerec)
      message = 'A new logfile has been received via e-mail:\nFrom: %s\nSubject: %s\nLogfile Name: %s\n'% \
                (sender, subject, savedlog)
      subject = "[MOQP log submission] from %s"%(sender)
      self.sendrobotmail(LOGPROCESSORS,subject, message)
      
      # e-mail the log submitter to acknowledge log receipt
      subject = 'Thank You For Submitting Your Missouri QSO Party Log'
      message ="""Thank you for submitting your Missouri QSO party log. 
You may verify your log has been received by visiting:
http://w0ma.org/mo_qso_party/logsubmission/logsreceived.php
Please note, it could take up to 24 hours before your call
appears in our Received Logs list. If the log processing
robot has difficulty processing your log file, we may contact
you for further information.


73 and thanks for making the Missouri QSO party fun!

The MOQP Log Contest Robot"""


      self.sendrobotmail(sender, subject, message)
#      return savedlog

   def process_badlog(self, sender, subject):
      message = """Logfile missing or of wrong file type in MOQP e-mail:\n
From: %s\n
Subject:%s\n"""%(sender, subject)
      message +="""The e-mail message appeared to have a callsign as the first word of the SUBJECT,
but there was no log file attached or the attachment was of the wrong type. Acceptable file formats:
Plain text (.TXT, .LOG)
.CSV (exported from MS Excel)
.XLS, .XLXS (MS Excel)
.PDF

Please resubmit your log by attaching the file to an e-mail or by using the web based log submission
form.

73,
The MOQP Log Contest Robot"""
      subject = "No logfile attached to e-mail received from %s"%(sender)
      self.sendrobotmail(LOGPROCESSORS,subject, message)
   
      pass

   def process_bademail(self, sender, subject, date):
      message = ('A suspicious MOQP logfile was received via e-mail:\nFrom: %s\nSubject: %s\nDate: %s.\n\nCould be SPAM.' \
                   % (sender, subject, date))
      message+="""The e-mail contained no logfile attachment or the attachment was 
      of the wrong type. I can't tell if the e-mail is an attempt to submit a logfile 
      or if it is SPAM. Please check the robot logfile and examine the e-mail to 
      verify I have not missed a valid log file.
      
      73 de the MOQP Log Processing Robot
      """           
      subject = "MOQP e-mail logfile rejected"
      self.sendrobotmail(LOGPROCESSORS,subject, message)
      pass
           
   
   def main(self):
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
         #print ('typ = %s\n'%(typ))
         #print "s = ",s
         sender, subject, date, filename, filetype, log = self.process_message_string(s)
         print ("Sender = %s\nSubject = %s\nFile name = %s\nFile Type = %s\n"%(sender, subject, filename, filetype))
         #logname = self.extract_call(subject)
         savedlog = None
         status = 'e-mail robot, '
         if (filename != None):
            # Log file of correct type found - save and accept it.
            savedlog = self.saveLog(filename, log, filetype)
            if (savedlog != "!!!UNABLE TO SAVE LOGFILE!!!"):
               status += 'Accepted, ,'
               newfiles.append( ('%s,%s,%s' \
                   % (sender.replace(',',' '), 
                      subject.replace(',',' '), 
                      savedlog) ) )
            else:
               status += '*REJECTED*, error saving logfile, '
         else:
            status += '*REJECTED*, No logfile or wrong logfile type, '   
         print('%s ,%s, %s, %s, %s, %s\n--------' \
                    % (status, 
                       date.replace(',',' '), 
                       sender.replace(',',' '), 
                       subject.replace(',',' '), 
                       filetype, 
                       savedlog))
         #if (newfiles != ''):
         #   with open('new-emails.txt', 'w') as tfile:
         #      tfile.write('%s'%(newfiles))
         if ('*REJECTED*' in status):
            self.process_bademail(sender, subject, date)
      dbFiles = open('filelist.txt','w')
      for dbentry in newfiles:
         dbFiles.write("%s\n" % dbentry)
      dbFiles.close()
      if (len(newfiles) > 0):
         cabfilter = CabrilloFilter(logwait, True, newfiles) 
              

if __name__=='__main__':
    mailbot = emailRobot(True)
    #bot.process_goodlog('mheitmann@n0so.net', 'Test Log', '2014-03-27', 'TEST LOG DATA', 'N0SO')
    #bot.sendrobotmail('mheitmann@n0so.net','Subject: This is a test','\nThis is a test message')
    #bot.createDBEntry('TE0ST', 'TE0ST@ARRL.NET, '2017-03-13', 'TE0ST.LOG'):
    #print bot.extract_call("w100aw-log.log")
    #bot.main()  
    #os.system('pwd')
    #os.system("ls -l "+logpath)
