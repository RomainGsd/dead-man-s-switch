##
## File:    server.py
## Date:    8 march 2020
## Author:  Romain Gsd
##

from typing import overload
from mail import Mail
from server import Server
import asyncio
import sys

if __name__=="__main__":
	print("==================================")
	print("||\tDead Man's Switch\t||")
	print("==================================")

	server = Server()
	server.run()
