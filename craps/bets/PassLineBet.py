from common.model.Bet import Bet
from common.model.Bet import Result
from craps.bets.CrapsBet import CrapsBet
import logging as log

class PassLineBet(Bet):

    def __init__(self, player, game_round, wager=10):
        #TODO ensure bank has enough if BANKRUPT mode?
        log.info('Placing pass line bet wager=%s, player.bank=%s', wager, player.bank) 
        super(PassLineBet, self).__init__(player, CrapsBet.PASS_LINE, wager)

    def is_bet_allowed(game_round):
        # bet already on the board, belonging to player?
        return game_round.point is None

    def assess_bet(self, game_round):
        """No point on board wins on 7, 11 and loses on 2, 3, 12. 
           Point on board it wins, 7 loses"""
        if game_round.point is None:
            if game_round.roll in {2, 3, 12}:
                self.result = Result.LOSE
            elif game_round.roll in {7, 11}:
                self.result = Result.WIN
        else:
            if game_round.roll == game_round.point:
                self.result = Result.WIN
            elif game_round.roll == 7:
                self.result = Result.LOSE

    def calculate_payout(self):
        """Pass line pays 1:1"""
        self.payout = self.wager

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

