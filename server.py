##
## File:    server.py
## Date:    9 March 2020
## Author:  Romain Goasdoué
##

import http.server
import socketserver
import os
from mail import Mail

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/alive002":
            self.send_response(302)
            self.send_header('Location', "/")
            self.end_headers()
            print("> User answered")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

class MyTCPServer(socketserver.TCPServer):
    def service_actions(self):
        print("> Do actions")
        #checkmail = Mail("Checkup")
        #checkmail.send_checkup(id)


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