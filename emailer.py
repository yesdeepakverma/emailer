from email import Encoders
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText

import os
import smtplib
import sys


class SendEmail(object):
    """
    Don't forget to enable less secure app for gmail account
    and https://accounts.google.com/b/0/DisplayUnlockCaptcha
    """

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465

    EMAIL_FROM = "{} <{}> ".format('Name', "gmail_user_name")

    mailer = None

    def __new__(cls, *args, **kwargs):
        if cls.mailer is None:
            cls.mailer = object.__new__(cls, *args, **kwargs)
        return cls.mailer

    def __init__(self, server=None, port=None):
        self.server_name = server or self.SMTP_SERVER
        self.server_port = port or self.SMTP_PORT
        self.server = smtplib.SMTP_SSL(self.server_name, self.server_port)
        self.server.ehlo()
 
    @property
    def header(self):
        return "This is email header"

    @property
    def footer(self):
        return "This is email Footer"

    def login(self, user=None, password=None):
        self.user = user or self.USER
        password = password or self.PASSWORD
        self.server.login(self.user, password)

    def build_body(self, from_, to, body, subject, email_type='html'):
        multipart = MIMEMultipart()
        multipart['Subject'] = subject
        multipart['From'] = from_
        multipart['To'] = (isinstance(to, list) and to[0] or to)

        body = self.header+body+self.footer
        multipart.attach(MIMEText(body, email_type))
        return multipart.as_string()

    def send_email(self, email_to, email_subject, email_body, email_from=None, attachemnt=None):
        email_from = email_from or self.EMAIL_FROM
        email_body = self.build_body(email_from, email_to, email_body, email_subject)
        self.server.sendmail(email_from, email_to, email_body)
        print("Email sent successfully to: {},\n with body: {}".format(email_to, email_body))

    def quit(self):
        self.server.quit()
        sys.exit(0)

