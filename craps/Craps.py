import random

from common.bet import Result
from common.dealer import Dealer
from common.game import Game
from common.game import GameRound
from common.player import Player
from config import config
import logging as log

class Craps(Game):

    def __init__(self):
        log.debug("Initializing craps")
        self.prev_round = CrapsRound()
        players = [Player(player['bettingStrategy'], player['bankroll']) for player in config['craps']['players']]
        dealer = Dealer()
        log.debug('Playing craps with players=%s and dealer=%s', players, dealer)
        super(Craps, self).__init__(players, dealer)

    #TODO this can probably go into the base class?
    def play(self):
        log.debug("Let's play craps!")
        game_round = CrapsRound()
        # If there are unresolved bets, continue playing 
        while self.should_continue() or game_round.bets:
            log.debug('Playing round %s with game_round=%s', self.roundNo, game_round)
            self.play_round(game_round)
            #TODO add final state to game.rounds[] for stats purposes later? or just use stat collector for useful info?
            # reset for next round
            game_round = CrapsRound(game_round)

        # Finalize, return any active bets as pushes
        #TODO is this needed anymore?
        final_game_state = CrapsRound(game_round)
        for bet in final_game_state.bets:
            bet.result = Result.PUSH
            bet.track_result()
            bet.pay_player()
        self.print_results()
    
class CrapsRound(GameRound):

    def __init__(self, prev_round=None):
        self.die1 = 0
        self.die2 = 0
        self.roll = 0
        self.point = None
        self.rolls = set()
        super(CrapsRound, self).__init__([])
        if prev_round is not None and not prev_round.is_seven_out():
            self.init_round(prev_round)

    def init_round(self, prev_round):
        if prev_round.is_point_on():
            self.point = None if prev_round.is_point_hit() else prev_round.point
        elif prev_round.roll in {4, 5, 6, 8, 9, 10}:
            self.point = prev_round.roll
        self.rolls = prev_round.rolls
        self.bets = [bet for bet in prev_round.bets if bet.result == Result.NOTHING]

    def start_round(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.roll = self.die1 + self.die2
        if self.roll != 7:
            self.rolls.add(self.roll)
        log.info('Rolled %s (%s, %s) and the point is %s', self.roll, self.die1, self.die2, self.point)

    def is_seven_out(self):
        return self.is_point_on() and self.roll == 7

    def is_point_on(self):
        return self.point is not None

    def is_point_hit(self):
        return self.point == self.roll

    def __str__(self):
        return str(self.__dict__)
