##
## File:    mail.py
## Date:    8 March 2020
## Author:  Romain Gsd
##

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import logging as log
import smtplib
import ssl

from tools import get_ip


class Mail:
    _port: int = 465
    _ip: str = get_ip()

    def __init__(self, what: str):
        log.debug('> %s mail is about to be send', what)
        try:
            with open('../mail_parameters.json', 'r') as params_fd:
                params = json.load(params_fd)
                self._user: str = params.get('user', '')
                self._password: str = params.get('password', '')
                self._smtp_server: str = params.get('smtp_server', '')
                self._checkup_email: str = params.get('checkup_mail', '')
                self._sender_email: str = params.get('sender_mail', '')
                self._alarm_email: str = params.get('alarm_mail', '')
        except FileNotFoundError:
            log.error('No parameters file, check parameters_howto.md')
            log.debug('Exiting...')
            exit(0)
        except Exception:
            log.error('[Error] Mail init')
            exit(0)

    def send_checkup(self, mail_id: str):
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Hello, friend'
        message['From'] = self._sender_email
        message['To'] = self._checkup_email
        text = (
            """
		DeadMan's Switch Checkup.
		=========================
		You have 48h to click on this link:
		http://"""
            + self._ip
            + ':8080/alive='
            '' + mail_id + '.html'
        )

        message.attach(MIMEText(text, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as smtpserver:
            try:
                ret = smtpserver.login(self._user, self._password)
            except smtplib.SMTPAuthenticationError:
                log.fatal('[FATAL] Mail server login failed')
                exit(0)
            except Exception:
                log.error(f'send_checkup fail : {ret}')
                exit(0)
            sendmail_ret = smtpserver.sendmail(self._sender_email, self._checkup_email, message.as_string())
            log.debug(f'{sendmail_ret}')
            smtpserver.quit()
            log.debug('> Checkup mail send')
            log.debug('> Waiting for user to answer...')

    def send_alarm(self):
        message = MIMEMultipart('alternative')
        message['Subject'] = self._user + " isn't responding since 48h"
        message['From'] = self._sender_email
        message['To'] = self._alarm_email
        text = (
            '\
		'
            + self._user
            + """ hasn't responded to its deadman's switch since 48 hours.
		He wanted to share this with you if it had to happen:
		`Be me, me bee`"""
        )

        message.attach(MIMEText(text, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as server:
            try:
                server.login(self._user, self._password)
            except Exception:
                log.fatal('[FATAL] Mail server login failed')
                exit(0)
            server.sendmail(self._sender_email, self._alarm_email, message.as_string())
            server.quit()
            log.debug('> Alarm mail sent, goodbye')
