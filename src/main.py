##
## File:    server.py
## Date:    8 march 2020
## Author:  Romain Gsd
##

import logging as log

from server import Server

log.basicConfig(level=log.DEBUG)

if __name__ == '__main__':
    log.info('==================================')
    log.info("||\tDead Man's Switch\t||")
    log.info('==================================')

    server = Server()
    server.run()
