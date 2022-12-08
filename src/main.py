##
## File:    server.py
## Date:    8 march 2020
## Author:  Romain Gsd
##

from typing import overload
from mail import Mail
from server import Server
import logging as log
import asyncio
import sys

log.basicConfig(level=log.DEBUG)

if __name__=="__main__":
	log.info("==================================")
	log.info("||\tDead Man's Switch\t||")
	log.info("==================================")

	server = Server()
	server.run()
