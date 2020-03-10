##
## File:    mail.py
## Date:    8 March 2020
## Author:  Romain Goasdoué
##

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail:
    _port = 465
    _password = _user = _sender_email = _checkup_email = _smtp_server = ""

    def __init__(self, what):
        print("> " + what + " mail is about to be send")
        with open("../credentials", "r") as fd:
            params = fd.read().splitlines()
            self._user = params[0]
            self._password = params[1]
            self._smtp_server = params[2]
            self._checkup_email = params[3]
            self._sender_email = params[4]

    def send_checkup(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Hello, friend"
        message["From"] = self._sender_email
        message["To"] = self._checkup_email
        text = """\
        I would like to know if you are ok.
        You have 48h to click on this link: http://localhost:8080/alive002"""

        message.attach(MIMEText(text, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as server:
            server.login(self._user, self._password)
            server.sendmail(self._sender_email, self._checkup_email, message.as_string())
            server.quit()
            print("> Checkup mail send")
            print("> Waiting for user to answer...")
