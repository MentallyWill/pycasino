import importlib

from common.bet import Result
from common.betting_strategy import BettingStrategy
from config import config
import logging as log

class Player:

    def __init__(self, betting_strategies, bankroll):
        self.bankroll = bankroll
        self.bank = bankroll
        self.betting_strategies = [self.load_betting_strategy(strat) for strat in betting_strategies]
        self.total_wagered = 0
        self.bets = []
        self.all_bets = {}
        self.stop_loss_amount = bankroll - (bankroll * config['stopLoss'])
        self.stop_gain_amount = bankroll + (bankroll * config['stopGain'])
        log.debug('Constructed player=%s', self)

    def make_bets(self, game_round):
        bets = [strat.bet(self, game_round, strat.amount_strategy.determine_amount(game_round)) for strat in self.betting_strategies if strat.bet.is_bet_allowed(game_round)]
        for bet in bets:
            bet_data = self.all_bets.get(bet.bet_type, {'timesPlaced': 0,
                                                        'totalWagered': 0,
                                                        'totalWon': 0,
                                                        Result.WIN: 0,
                                                        Result.LOSE: 0,
                                                        Result.PUSH: 0})
            bet_data['timesPlaced'] += 1
            bet_data['totalWagered'] += bet.wager
            self.all_bets[bet.bet_type] = bet_data
        return bets
    
    def play_round(self, game_round):
        return game_round
  
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

    #TODO this is brittle? if nothing else it looks ugly
    def load_betting_strategy(self, strat):
        strat_path = strat['amountStrategy']
        strat_index = strat_path.rfind('.')
        amount_module = importlib.import_module(strat_path[0:strat_index])
        amount_class = getattr(amount_module, strat_path[strat_index+1:])
       
        bet_path = strat['bet']
        bet_index = bet_path.rfind('.')
        bet_module = importlib.import_module(bet_path[0:bet_index])
        bet_class = getattr(bet_module, bet_path[bet_index+1:])
        return BettingStrategy(bet_class, amount_class())

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
