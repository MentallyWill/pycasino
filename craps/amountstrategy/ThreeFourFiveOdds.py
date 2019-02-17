from common.amount_strategy import AmountStrategy
from craps.bets import CrapsBet
import logging as log

class ThreeFourFiveOdds(AmountStrategy):

    def __init__(self):
        super(ThreeFourFiveOdds, self).__init__()
  
    def determine_amount(self, game_round):
        #TODO make multiplayer?
        #TODO this should take a player with a history of bets too? 
        factor = 1
        if game_round.point in {6, 8}:
            factor = 5
        elif game_round.point in {5, 9}:
            factor = 4
        elif game_round.point in {4, 10}:
            factor = 3
        
        for bet in game_round.bets:
            if bet.bet_type == CrapsBet.PASS_LINE:
                return bet.wager * factor
