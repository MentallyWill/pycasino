from common.model.Bet import Result
from common.model.Player import Player
from craps.bets.PassLineBet import PassLineBet
import logging as log

class CrapsPlayer(Player):

    def __init__(self, betting_strategies, bankroll=1000):
        super(CrapsPlayer, self).__init__(betting_strategies, bankroll)

    def make_bets(self, game_round):
        # clean this up, move to base class?
        bets = [strat.bet(self, game_round, strat.amount_strategy.determine_amount(game_round)) 
                for strat in self.betting_strategies if strat.bet.is_bet_allowed(game_round)]
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

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

