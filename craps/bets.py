from enum import Enum

from common.bet import Bet
from common.bet import Result
import logging as log

class CrapsBet(Enum):
    PASS_LINE = 0
    PASS_LINE_ODDS = 1
    FIELD = 2

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