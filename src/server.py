##
## File:    server.py
## Date:    9 March 2020
## Author:  Romain Gsd
##

from datetime import datetime, timedelta
import http
from http.server import SimpleHTTPRequestHandler
import logging as log
import os
import secrets
import socketserver
from time import sleep

from mail import Mail

ANSWERED: bool = False
REQ_ID: str = ''


class MyHandler(SimpleHTTPRequestHandler):
    global REQ_ID

    def do_GET(self):
        if self.path == f'/alive={REQ_ID}.html':
            global ANSWERED
            ANSWERED = True
            self.send_response(http.HTTPStatus.FOUND)
            self.send_header('Location', '/index.html')
            self.end_headers()
            log.debug('> User answered, see you in one month')
        return SimpleHTTPRequestHandler.do_GET(self)


class MyTCPServer(socketserver.TCPServer):
    _is_send: bool = False
    _curr_date = datetime.now()
    # First checkup is 10 seconds after server has started
    _next_checkup_date = _curr_date + timedelta(seconds=10)
    _to_answer_date = _next_checkup_date + timedelta(days=2)

    def service_actions(self):
        global REQ_ID
        global ANSWERED
        self._curr_date = datetime.now()

        if self._curr_date > self._to_answer_date:
            log.debug('> Too late to answer, sending data to your contact...')
            # Remove the generated file corresponding to the previous token
            to_delete = f'alive={REQ_ID}.html'
            os.remove(to_delete) if (os.path.isfile(to_delete)) else None
            # Send mail
            mail = Mail('Alarm')
            mail.send_alarm()
            exit(0)
        if not self._is_send or ANSWERED:
            # Remove the generated file corresponding to the previous token
            to_delete = f'alive={REQ_ID}.html'
            os.remove(to_delete) if (os.path.isfile(to_delete)) else None

            # Waiting for date to correspond to next checkup
            while self._curr_date < self._next_checkup_date:
                sleep(2)
                self._curr_date = datetime.now()

            # Generate an url token
            REQ_ID = secrets.token_urlsafe(32)

            # Generate a file where user arrive before being redirected to index.html
            with open(f'alive={REQ_ID}.html', 'w+'):
                log.debug('> Generated html page linked to token')

            # Send Checkup Email
            checkmail = Mail('Checkup')
            checkmail.send_checkup(REQ_ID)

            # Setting next checkup in 30 days
            self._next_checkup_date = self._curr_date + timedelta(days=30)
            if ANSWERED:
                self._to_answer_date = self._next_checkup_date + timedelta(days=2)
            self._is_send = True
            ANSWERED = False


class Server:
    def __init__(self, port: int = 8080):
        log.debug('> Initializing server...')
        self._port: int = port
        self._web_dir: str = os.path.join(os.path.dirname(__file__), '../web')

    def run(self):
        os.chdir(self._web_dir)  # We change dir to 'web' folder

        with MyTCPServer(('', self._port), MyHandler) as httpd:
            log.debug(f'> Serving at port {self._port}')
            log.debug('> First checkup will run in 10 seconds')
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.server_close()
                pass
