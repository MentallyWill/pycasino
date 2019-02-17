from abc import ABCMeta, abstractmethod
from enum import Enum

from common.bet import Result
from config import config
import logging as log

class Game:
    __metaclass__ = ABCMeta

    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        self.roundNo = 0
        #TODO use for stats or remove
        self.rounds = []

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def create_round(self, prev_round):
        pass

    @abstractmethod
    def assess_bets(self):
        pass

    def play_round(self, game_round):
        for player in self.players:
            game_round.bets += player.make_bets(game_round)

        game_round.start_round()
        # pass-by-ref: returning game_round unnecessary?
        for player in self.players:
            game_round = player.play_round(game_round)
       
        game_round = self.dealer.play_round(game_round)
        for bet in game_round.bets:
            bet.handle_bet(game_round)
        return game_round

    def should_continue(self):
        if 'ROUND_COUNT' in config['playUntil'] and self.roundNo >= config['rounds']:
            return False

        for player in self.players:
            if player.can_continue(config['craps']['tableMin']):
                self.roundNo += 1
                return True
        else:
            return False

    def print_results(self):
        log.info('=======================================================================================')
        log.info('======================================= RESULTS =======================================')
        log.info('=======================================================================================')
        log.info('Rounds Played: %s', self.roundNo)
        #TODO check these are correct
        for player in self.players:
            log.info('---------------------------------------------------------------------------------------')
            log.info('Player with betting strategy: %s',
                     ' '.join(str(betting_strategy) for betting_strategy in player.betting_strategies))
            log.info('Starting bank: %s, ending bank: %s, total wagered: %s', player.bankroll, player.bank, player.total_wagered)
            log.info('OVERALL HOUSE EDGE: %s', (player.bankroll - player.bank) / player.total_wagered)
            for bet_type, bet_data in player.all_bets.items():
                house_edge = (bet_data['totalWagered'] - bet_data['totalWon']) / bet_data['totalWagered']
                log.info('***********')
                log.info('%s = {Times=%s, %s=%s, %s=%s, %s=%s, Total Winnings=%s, Total Wagered=%s}', bet_type.name,
                         bet_data['timesPlaced'], Result.WIN.name, bet_data[Result.WIN],
                         Result.LOSE.name, bet_data[Result.LOSE], Result.PUSH.name, bet_data[Result.PUSH],
                         bet_data['totalWon'], bet_data['totalWagered'])
                log.info('HOUSE EDGE: %s', house_edge)

class GameRound:
    __metaclass__ = ABCMeta

    def __init__(self, bets=[]):
        self.bets = bets

    @abstractmethod
    def start_round(self):
        pass
