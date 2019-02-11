class BettingStrategy:

    def __init__(self, bet, amount_strategy):
        self.bet = bet
        self.amount_strategy = amount_strategy

    def __str__(self):
        return '(' + self.bet.__name__ + ': ' + self.amount_strategy.__class__.__name__ + ')' 

    def __repr__(self):
        return str(self.__dict__)
