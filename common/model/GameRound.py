from abc import ABCMeta, abstractmethod

# needed? 
class GameRound(object):
    __metaclass__ = ABCMeta

    def __init__(self, bets=[]):
        self.bets = bets

    @abstractmethod
    def start_round(self):
        pass

