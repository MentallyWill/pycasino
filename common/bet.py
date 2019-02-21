from abc import ABCMeta, abstractmethod
from enum import Enum

import logging as log

class Bet:
    __metaclass__ = ABCMeta

    def __init__(self, player, bet_type, wager=10):
        self.wager = wager
        self.bet_type = bet_type
        self.payout = 0
        self.result = Result.NOTHING
        self.player = player
        self.player.bank -= wager
        self.player.total_wagered += wager
    
    @staticmethod
    @abstractmethod
    def is_bet_allowed(self, game_round):
        pass

    @abstractmethod
    def assess_bet(self, game_round):
        pass

    @abstractmethod
    def calculate_payout(self, game_round):
        pass

    def handle_bet(self, game_round):
        self.assess_bet(game_round)
        if self.result != Result.NOTHING:
            log.info('%s is %s', self.bet_type.name, self.result.name)
            self.track_result()
            if self.result == Result.WIN:
                self.calculate_payout(game_round)
            if self.result in {Result.WIN, Result.PUSH}:
                self.pay_player()

    def track_result(self):
        self.player.all_bets[self.bet_type][self.result] += 1

    def pay_player(self):
        log.debug('Paying player payout=%s wager=%s', self.payout, self.wager)
        self.player.all_bets[self.bet_type]['totalWon'] += (self.payout + self.wager)
        self.player.pay(self.payout + self.wager)

    def __str__(self):
        return str(self.__dict__)

class Result(Enum):
    WIN = 0
    LOSE = 1
    PUSH = 2
    NOTHING = 3
