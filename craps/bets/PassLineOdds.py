from common.model.Bet import Bet
from common.model.Bet import Result
from craps.bets.CrapsBet import CrapsBet
import logging as log

class PassLineOdds(Bet):

    def __init__(self, player, game_round, wager=10):
        if game_round.point in {6, 8}:
            self.payout_ratio = 6/5
        elif game_round.point in {5, 9}:
            self.payout_ratio = 3/2
        elif game_round.point in {4, 10}:
            self.payout_ratio = 2/1
        log.info('Placing pass line odds bet wager=%s, player.bank=%s, player.total_wagered=%s', wager, player.bank,
                 player.total_wagered)
        super(PassLineOdds, self).__init__(player, CrapsBet.PASS_LINE_ODDS, wager)

    def is_bet_allowed(game_round):
        #TODO make multiplayer?
        #TODO is there a cleaner way to do this? 
        found_pass_line = False
        if game_round.point is not None:
            for bet in game_round.bets:
                if bet.bet_type == CrapsBet.PASS_LINE_ODDS:
                    return False
                elif bet.bet_type == CrapsBet.PASS_LINE:
                    found_pass_line = True
        return found_pass_line and game_round.point in {4, 5, 6, 8, 9, 10}

    def assess_bet(self, game_round):
        """Only placed with point on board. Wins if point is hit, loses on 7-out"""
        if game_round.roll == game_round.point:
            self.result = Result.WIN
        elif game_round.roll == 7:
            self.result = Result.LOSE

    def calculate_payout(self):
        """Pass line odds pay 6:5 for {6, 8}, 3:2 for {5, 9}, and 2:1 for {4, 10}"""
        self.payout = self.wager * self.payout_ratio

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

