#!/usr/bin/env python
# coding: utf-8

## Import Email Module Requirements:
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

## Import Variables via Files from Directory:
from emailConfigurationVariables import list_of_receiver_email_addresses, email_username, email_password, email_subject, email_body

## To / From:
sender = email_username
receivers = list_of_receiver_email_addresses

## Configuration:
msg = MIMEText(email_body, 'html')
msg['Subject'] = email_subject
msg['From'] = sender
msg['To'] = ','.join(receivers)

## Authentication:
s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
s.login(user = email_username, password = email_password) # The App Password Needed AFTER the Google Update for Less Secure Apps: https://support.google.com/accounts/answer/6010255?hl=en&visit_id=637902943692838375-3915028692&p=less-secure-apps&rd=1#zippy=%2Cif-less-secure-app-access-is-on-for-your-account%2Cupdate-your-app-or-operating-system%2Cuse-more-secure-apps%2Cuse-an-app-password
s.sendmail(sender, receivers, msg.as_string())
s.quit()






