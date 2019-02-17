from abc import ABCMeta, abstractmethod

from common.bet import Result
from config import config
from craps.craps import CrapsRound

class AmountStrategy:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.last_result = Result.NOTHING

    @abstractmethod
    def determine_amount(self, game_round):
        pass

class TableMin(AmountStrategy):
    
    def __init__(self):
        super(TableMin, self).__init__()

    #TODO can this be cleaned up? Should an amountstrat know what game?
    def determine_amount(self, game_round):
        if isinstance(game_round, CrapsRound):
            return config['craps']['tableMin']
        #TODO elif blackjack

