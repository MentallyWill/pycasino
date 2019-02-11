#!/usr/bin/env python3

import sys
import logging as log
import logging.config
import yaml

from config import config
from blackjack.Blackjack import Blackjack
from craps.Craps import Craps

def main():
    if not config['playUntil']:
        log.error("No simulation end configured.")

    #TODO add argline parser 
    type = sys.argv[1]
    if type == "craps":
        log.info("Starting a game of craps")
        game = Craps()
    elif type == "blackjack":
        log.info("Starting a game of blackjack")
        game = Blackjack()
    else:
        print("usage: [game] must be craps or blackjack")

    game.play()

if __name__ == '__main__':
    logging.config.dictConfig(config['logging'])
    log.info('Welcome to pycasino')
    log.debug('config=%s', config)

    main()

