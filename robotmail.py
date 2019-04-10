#!/usr/bin/python
import smtplib, email, datetime, string
from email.mime.text import MIMEText
from robotconfig import *

VERSION = '1.0.0'

class robotMail():

   def __init__(self, sender = None, recipient = None, subject = None, body = None):
      if (sender != None):
         self.sendrobotmail(sender, recipient, subject, body)
      pass

   def getVersion(self):
      return self.VERSION

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
    print app.getVersion()

