from abc import ABCMeta, abstractmethod
import importlib
from common.model.BettingStrategy import BettingStrategy
from config import config
import logging as log

class Player(object):
    __metaclass__ = ABCMeta

    def __init__(self, betting_strategies, bankroll):
        self.bankroll = bankroll
        self.bank = bankroll
        self.betting_strategies = [self.load_betting_strategy(strat) for strat in betting_strategies]
        self.total_wagered = 0
        self.bets = []
        self.all_bets = {}
        self.stop_loss_amount = bankroll - (bankroll * config['stopLoss'])
        self.stop_gain_amount = bankroll + (bankroll * config['stopGain'])

    @abstractmethod
    def make_bets(self, game_round):
        pass
    
    @abstractmethod
    def play_round(self, game_round):
        pass
   
    def can_continue(self, table_min):
        if 'STOP_LOSS' in config['playUntil'] and self.bank <= self.stop_loss_amount:
            return False
        elif 'STOP_GAIN' in config['playUntil'] and self.bank >= self.stop_gain_amount:
            return False
        elif 'BANKRUPT' in config['playUntil'] and self.bank < table_min:
            return False
        else:
            return True
        
    def pay(self, amount):
        self.bank += amount

    def load_betting_strategy(self, strat):
        amount_module = importlib.import_module(strat['amountStrategy'])
        amount_class = getattr(amount_module, strat['amountStrategy'].split('.')[-1])
        bet_module = importlib.import_module(strat['bet'])
        bet_class = getattr(bet_module, strat['bet'].split('.')[-1])
        return BettingStrategy(bet_class, amount_class())

    def __str__(self):
        return str(self.__dict__)
