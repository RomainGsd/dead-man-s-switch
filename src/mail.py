##
## File:    mail.py
## Date:    8 March 2020
## Author:  Romain Gsd
##

import smtplib, ssl
import logging as log
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tools import get_ip

class Mail:
	_port = 465
	_password = _user = _sender_email = _checkup_email = _smtp_server = ""
	_ip = get_ip()

	def __init__(self, what):
		log.debug("> %s mail is about to be send", what)
		try:
			with open("../mail_parameters.json", "r") as params_fd:
				params = json.load(params_fd)
				self._user = params["user"]
				self._password = params["password"]
				self._smtp_server = params["smtp_server"]
				self._checkup_email = params["checkup_mail"]
				self._sender_email = params["sender_mail"]
				self._alarm_email = params["alarm_mail"]
		except FileNotFoundError:
			log.error("No parameters file, check parameters_howto.md")
			log.debug("Exiting...")
			exit(0)
		except:
			log.error("[Error] Mail init")
			exit(0)

	def send_checkup(self, mail_id):
		message = MIMEMultipart("alternative")
		message["Subject"] = "Hello, friend"
		message["From"] = self._sender_email
		message["To"] = self._checkup_email
		text = """
		DeadMan's Switch Checkup.
		=========================
		You have 48h to click on this link:
		http://""" + self._ip + ":8080/alive=""" + mail_id + ".html"

		message.attach(MIMEText(text, "plain"))
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as smtpserver:
			try:
				ret = smtpserver.login(self._user, self._password)
			except smtplib.SMTPAuthenticationError:
				log.fatal("[FATAL] Mail server login failed")
				exit(0)
			ret = smtpserver.sendmail(self._sender_email, self._checkup_email, message.as_string())
			log.debug("%s", ret)
			smtpserver.quit()
			log.debug("> Checkup mail send")
			log.debug("> Waiting for user to answer...")

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
				log.fatal("[FATAL] Mail server login failed")
				exit(0)
			server.sendmail(self._sender_email, self._alarm_email, message.as_string())
			server.quit()
			log.debug("> Alarm mail sent, goodbye")
