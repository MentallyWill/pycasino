#!/usr/bin/env python3

import argparse
import sys
import logging as log
import logging.config
import yaml

from config import config
from blackjack.blackjack import Blackjack
from craps.craps import Craps

def main():
    log.info('Welcome to pycasino')
    log.debug('config=%s', config)

    if not config['playUntil']:
        log.error("No simulation end configured.")

    game = globals().get(config['game'], lambda: log.error('Unsupported game: %s', config['game']))()
    if game is not None:
        game.play()

def craps():
    log.info('Starting a game of craps')
    return Craps()

def blackjack():
    log.info('Starting a game of blackjack')
    return Blackjack()

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('game', help='game to play [craps | blackjack]')
    parser.add_argument('-r', '--rounds', help='number of rounds to play', type=int)
    parser.add_argument('-sl', '--stop-loss', help='percent down before stopping', type=float)
    parser.add_argument('-sg', '--stop-gain', help='percent up before stopping', type=float)
    parser.add_argument('-b', '--bankrupt', help='stop when bankrupt', action='store_true')
    parser.add_argument('-l', '--log', help='log level [INFO | DEBUG | WARN | ERROR]')
    return parser

def override_config(args):
    if args.log is not None:
        # validate it's INFO/WARN/...?
        config['logging']['loggers']['']['level'] = args.log.upper()
        configure_logging()

    config['game'] = args.game
    playUntil = list()
    if args.rounds is not None:
        config['rounds'] = args.rounds
        playUntil.append('ROUND_COUNT')
    if args.stop_loss is not None:
        config['stopLoss'] = args.stop_loss
        playUntil.append('STOP_LOSS')
    if args.stop_gain is not None:
        config['stopGain'] = args.stop_gain
        playUntil.append('STOP_GAIN')

    if playUntil:
        config['playUntil'] = playUntil
    log.debug('Using config=%s', config)

def configure_logging():
    logging.config.dictConfig(config['logging'])

if __name__ == '__main__':
    configure_logging()

    #TODO be much more thoughtful about logging?
    parser = setup_parser()
    args = parser.parse_args()
    override_config(args)
    
    main()

