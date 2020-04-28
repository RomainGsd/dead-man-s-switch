##
## File:    tools.py
## Date:    12 March 2020
## Author:  Romain Goasdoué
##

import requests

def get_ip():
	f = requests.request('GET', 'http://myip.dnsomatic.com')
	ip = f.text
	return ip
