##
## File:    server.py
## Date:    9 March 2020
## Author:  Romain Gsd
##

import http.server
import socketserver
import os
import secrets
import logging as log
from time import sleep
from mail import Mail
from datetime import datetime, timedelta

ANSWERED : bool = False

class MyHandler(http.server.SimpleHTTPRequestHandler):
	_id : str = ""

	def do_GET(self):
		if self.path == "/alive=" + self._id + ".html":
			global ANSWERED
			ANSWERED = True
			self.send_response(302)
			self.send_header('Location', "/index.html")
			self.end_headers()
			log.debug("> User answered, see you in one month")
		return http.server.SimpleHTTPRequestHandler.do_GET(self)

class MyTCPServer(socketserver.TCPServer):
	_is_send = False
	_curr_date = datetime.now()
	#First checkup is 10 seconds after server has started
	_next_checkup_date = _curr_date + timedelta(seconds=10)
	_to_answer_date = _next_checkup_date + timedelta(days=2)

	def service_actions(self):
		global ANSWERED
		self._curr_date = datetime.now()

		if (self._curr_date > self._to_answer_date):
			log.debug("> Too late to answer, sending data to your contact...")
			#Remove the generated file corresponding to the previous token
			to_delete = "alive=" + self.RequestHandlerClass._id + ".html"
			os.remove(to_delete) if (os.path.isfile(to_delete)) else None
			#Send mail
			mail = Mail("Alarm")
			mail.send_alarm()
			exit(0)
		if (not self._is_send or ANSWERED):
			#Remove the generated file corresponding to the previous token
			to_delete = "alive=" + self.RequestHandlerClass._id + ".html"
			os.remove(to_delete) if (os.path.isfile(to_delete)) else None

			#Waiting for date to correspond to next checkup
			while self._curr_date < self._next_checkup_date:
				sleep(2)
				self._curr_date = datetime.now()

			#Generate an url token
			self.RequestHandlerClass._id = secrets.token_urlsafe(32)

			#Generate a file where user arrive before being redirected to index.html
			with open("alive="+self.RequestHandlerClass._id + ".html", "w+"):
				log.debug("> Generated html page linked to token")

			#Send Checkup Email
			checkmail = Mail("Checkup")
			checkmail.send_checkup(self.RequestHandlerClass._id)

			#Setting next checkup in 30 days
			self._next_checkup_date = self._curr_date + timedelta(days=30)
			if ANSWERED:
				self._to_answer_date = self._next_checkup_date + timedelta(days=2)
			self._is_send = True
			ANSWERED = False


class Server:
	_port = 8080
	_web_dir = ""

	def __init__(self, port: int =8080):
		log.debug("> Initializing server...")
		self._port : int = port
		self._web_dir : str = os.path.join(os.path.dirname(__file__), '../web')

	def run(self):
		Handler = MyHandler
		os.chdir(self._web_dir) #We change dir to 'web' folder

		with MyTCPServer(("", self._port), Handler) as httpd:
			log.debug("> Serving at port %d", self._port)
			log.debug("> First checkup will run in 10 seconds")
			try:
				httpd.serve_forever()
			except KeyboardInterrupt: 
				httpd.server_close()
				pass
