##
## File:    mail.py
## Date:    8 March 2020
## Author:  Romain Gsd
##

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tools import get_ip

class Mail:
	_port = 465
	_password = _user = _sender_email = _checkup_email = _smtp_server = ""
	_ip = get_ip()

	def __init__(self, what):
		print("> " + what + " mail is about to be send")
		try:
			with open("../credentials", "r") as fd:
				params = fd.read().splitlines()
				self._user = params[0]
				self._password = params[1]
				self._smtp_server = params[2]
				self._checkup_email = params[3]
				self._sender_email = params[4]
				self._alarm_email = params[5]
		except FileNotFoundError:
			print("No credentials file, check credentials_example.md")
			print("Exiting...")
		except:
			print("[Error] Mail init")
		finally:
			exit(0)

	def send_checkup(self, mail_id):
		message = MIMEMultipart("alternative")
		message["Subject"] = "Hello, friend"
		message["From"] = self._sender_email
		message["To"] = self._checkup_email
		text = """\
		DMS Checkup.
		You have 48h to click on this link:
		http://""" + self._ip + ":8080/alive=""" + mail_id + ".html"

		message.attach(MIMEText(text, "plain"))
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as smtpserver:
			try:
				ret = smtpserver.login(self._user, self._password)
			except SMTPException:
				print("[FATAL] Mail server login failed")
				exit(0)
			ret = smtpserver.sendmail(self._sender_email, self._checkup_email, message.as_string())
			print(ret)
			smtpserver.quit()
			print("> Checkup mail send")
			print("> Waiting for user to answer...")

	def send_alarm(self):
		message = MIMEMultipart("alternative")
		message["Subject"] = self._user + " isn't responding since 48h"
		message["From"] = self._sender_email
		message["To"] = self._alarm_email
		text = "\
		" + self._user + """ hasn't responded to its deadman's switch since 48 hours.
		He wanted to share this with you if it has to happend:
		Be me, me bee"""

		message.attach(MIMEText(text, "plain"))
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as server:
			try:
				server.login(self._user, self._password)
			except:
				print("[FATAL] Mail server login failed")
				exit(0)
			server.sendmail(self._sender_email, self._alarm_email, message.as_string())
			server.quit()
			print("> Alarm mail sent, goodbye")
