from config import config
from common.amountstrategy.AmountStrategy import AmountStrategy
from craps.CrapsRound import CrapsRound

class TableMin(AmountStrategy):

    def __init__(self):
        super(TableMin, self).__init__()

    def determine_amount(self, game_round):
        if isinstance(game_round, CrapsRound):
            return config['craps']['tableMin']
        #TODO elif blackjack

