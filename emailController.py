from google.appengine.api import mail
from secrets import *
import logging

def send_email(to, subject, body):
  logging.info('sending an email from ' + Secrets.EMAIL_FROM + ' to: ' + to)
  message = mail.EmailMessage(sender=Secrets.EMAIL_FROM, subject=subject, body=body, to=to)
  message.send()

def send_email_to_admins(subject, body):
  logging.info('sending an email from ' + Secrets.EMAIL_FROM + ' to: ' + Secrets.ADMIN_EMAIL)
  message = mail.AdminEmailMessage(sender=Secrets.EMAIL_FROM, subject=subject, body=body)
  message.send()
