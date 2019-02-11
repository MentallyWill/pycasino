from abc import ABCMeta, abstractmethod

from common.model.Bet import Result

class AmountStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.last_result = Result.NOTHING

    @abstractmethod
    def determine_amount(self, game_round):
        pass

