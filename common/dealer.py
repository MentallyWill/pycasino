from common.player import Player

class Dealer(Player):

    def __init__(self, bankroll=0):
        super(Dealer, self).__init__([], bankroll)

    def make_bets(self):
        pass
    
    def play_round(self, game_round):
        return game_round 

    def __str__(self):
        return str(self.__dict__)

