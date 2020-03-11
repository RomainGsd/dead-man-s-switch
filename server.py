##
## File:    server.py
## Date:    9 March 2020
## Author:  Romain Goasdoué
##

import http.server
import socketserver
import os
import secrets
from time import sleep
from mail import Mail
from datetime import datetime, timedelta

ANSWERED = False

class MyHandler(http.server.SimpleHTTPRequestHandler):
    _id = ""

    def do_GET(self):
        if self.path == "/alive=" + self._id + ".html":
            global ANSWERED
            ANSWERED = True
            self.send_response(302)
            self.send_header('Location', "/index.html")
            self.end_headers()
            print("> User answered")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

class MyTCPServer(socketserver.TCPServer):
    _is_send = False
    _curr_date = datetime.now()
    #First checkup is 30 seconds after server's start
    _run_date = _curr_date + timedelta(seconds=30)

    def service_actions(self):
        global ANSWERED
        if (not self._is_send or ANSWERED):
            while self._curr_date < self._run_date:
                sleep(2)
                self._curr_date = datetime.now()
            #Remove the generated file corresponding to the previous id
            to_delete = "alive=" + self.RequestHandlerClass._id + ".html"
            os.remove(to_delete) if (os.path.isfile(to_delete)) else None

            #Generate an url token
            self.RequestHandlerClass._id = secrets.token_urlsafe(32)

            #Generate a file where user arrive before being redirected to index.html
            with open("alive="+self.RequestHandlerClass._id + ".html", "w+"):
                print("> Generated html page linked to token")

            #Send Checkup Email
            checkmail = Mail("Checkup")
            checkmail.send_checkup(self.RequestHandlerClass._id)

            self._is_send = True
            ANSWERED = False
            #Setting next checkup in 30 days
            self._run_date = self._curr_date + timedelta(days=30)


class Server:
    _port = 8080
    _web_dir = ""

    def __init__(self, port=8080):
        print("> Initializing server...")
        self._port = port
        self._web_dir = os.path.join(os.path.dirname(__file__), 'web')

    def run(self):
        Handler = MyHandler
        os.chdir(self._web_dir) #We change dir to 'web' folder

        with MyTCPServer(("", self._port), Handler) as httpd:
            print("> Serving at port", self._port)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt: pass; httpd.server_close()