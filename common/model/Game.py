from abc import ABCMeta, abstractmethod
from enum import Enum

from common.model.Bet import Result
import logging as log

class Game(object):
    __metaclass__ = ABCMeta

    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        #TODO use for stats
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
       
        for player in self.players:
            game_round = player.play_round(game_round)
       
        game_round = self.dealer.play_round(game_round)
        for bet in game_round.bets:
            bet.handle_bet(game_round)

