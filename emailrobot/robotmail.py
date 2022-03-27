#!/usr/bin/python
import smtplib, email, datetime, string
from email.mime.text import MIMEText
from robotconfig import *

class robotMail():

   def __init__(self, sender = None, recipient = None, subject = None, body = None):
      if (sender != None):
         self.sendrobotmail(sender, recipient, subject, body)
      pass

   def emailResults(self, msgparts, logdict=None):
        """If logdict is defined, this is a CAB file. Send the
           following to the log processors and the submitter."""
        if (logdict):
            header=logdict['HEADER']
            # E-mail log processors
            psubject = ('New MOQP Logfile Received from %s' % (header['CALLSIGN']))
            pmessage = ('CABRILLO format logfile %s received.' % (msgparts['fname']))
            self.sendrobotmail( ROBOTSENDER, LOGPROCESSORS, psubject, pmessage )
		                         
            mailackmessage = 'Thank you for your Missouri QSO Party log submission.\n '
            mailackmessage += 'Your log has been accepted by the Log Processing Robot\n '
            mailackmessage += 'and has been forwarded to the MOQP Log Processing Team\n '
            mailackmessage += 'for scoring.\n\n'
            mailackmessage += '-- 73 de The MOQP Log Processing Robot'
            
            self.sendrobotmail( ROBOTSENDER,
                                msgparts['replyto'],
                                'Re: Your MOQP %s Log Submission for %s' %
                                (msgparts['method'], header['CALLSIGN']),
                                mailackmessage )
        else:
            # Inform log processors that log is being held for their review.
            mailmessage = """A new MOQP logfile was received -- I don't know how to process it:\n"""
            mailmessage += ('From: %s\nSubject: %s\nReceived by: %s\n\n' %
                           (msgparts['replyto'], 
                            msgparts['subject'],
                            msgparts['method']))
            mailmessage += 'The file attached is of the wrong type or is corrupted, or the message is SPAM.\n'
            mailmessage += ('The file is saved in the humanreview folder:\nFile name: %s\n' % (msgparts['fname']))
            mailmessage += """Please check the robot logfile and examine the file itself to verify I have not missed a valid log file.
     
            73 de the MOQP Log Processing Robot
            """           
            self.sendrobotmail( ROBOTSENDER,
                                 LOGPROCESSORS,
                                 'New MOQP Logfile Received -- further processing is required',
                                 mailmessage)
            
        return True

   def process_goodlog(self, sender, subject, savedlog):
      #self.createDBEntry(logname, subject, timerec, savedlog)
      #print 'SUCCESS!,; {0},; {1},; {2},; {3}'.format(logname, sender, timerec, savedlog)
      # e-mail the log processing team to let them know a new log is available
#      message = 'A new logfile has been received via e-mail:\nFrom: {0}\nSubject: {1}\nDate: {2}, Logfile Name: {3}, Date/time received:{4}\n'.format(sender, subject, date, savedlog, timerec)
      message = 'A new logfile has been received via e-mail:\nFrom: %s\nSubject: %s\nLogfile Name: %s\n'% \
                (sender, subject, savedlog)
      subject = "[MOQP log submission] from %s"%(sender)
      self.sendrobotmail(ROBOTSENDER, LOGPROCESSORS, subject, message)
      
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


      self.sendrobotmail(ROBOTSENDER, sender, subject, message)
#      return savedlog

   def process_badlog(self, sender, subject):
      message = """Logfile missing or of wrong file type in MOQP e-mail:\n
From: %s\n
Subject:%s\n"""%(sender, subject)
      message +="""The e-mail message had no log file attached or the 
      attachment was of the wrong type. Acceptable file formats:
          .LOG, .CBR, .CAB, .DAT (Plain text CABRILLO format)
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
      self.sendrobotmail(ROBOTSENDER, LOGPROCESSORS,subject, message)
      pass


   def sendrobotmail(self, sender, to, subject, body):
      msg = MIMEText(body)
      msg['Subject'] = subject
      msg['From'] = sender
      msg['To'] = to
      try:
         smtpObj = smtplib.SMTP(imap_host, 25)
         smtpObj.login(imap_user, imap_pass)
         smtpObj.sendmail(sender, to, msg.as_string())         
      except:
         print "Error: unable to send email"

if __name__=='__main__':
    app = robotMail(ROBOTSENDER, "mikeheit@aol.com","TEST MESSAGE","This is a test message")

