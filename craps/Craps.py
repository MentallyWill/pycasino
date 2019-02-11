from common.model.Bet import Result
from common.model.Dealer import Dealer
from common.model.Game import Game
from config import config
from craps.CrapsPlayer import CrapsPlayer
from craps.CrapsRound import CrapsRound
import logging as log

class Craps(Game):

    def __init__(self):
        log.debug("Initializing craps")
        self.prev_round = CrapsRound()
        players = [CrapsPlayer(player['bettingStrategy'], player['bankroll']) for player in config['craps']['players']]
        dealer = Dealer()
        self.roundNo = 0
        log.debug('Playing craps with players=%s and dealer=%s', players, dealer)
        super(Craps, self).__init__(players, dealer)

    def play(self):
        log.debug("Let's play craps!")
        game_round = CrapsRound()
        while self.should_continue():
            game_round = CrapsRound(game_round)
            log.debug('Playing round %s with game_round=%s', self.roundNo, game_round)
            self.play_round(game_round)
        # Finalize, return any active bets as pushes
        #TODO should "ending" just mean no new bets accepted, play out rest of bets?
        final_game_state = CrapsRound(game_round)
        for bet in final_game_state.bets:
            bet.result = Result.PUSH
            bet.track_result()
            bet.pay_player()
        self.print_results()
        
    def should_continue(self):
        if 'ROUND_COUNT' in config['playUntil'] and self.roundNo == config['roundCount']:
            return False

        for player in self.players:
            if player.can_continue(config['craps']['tableMin']):
                self.roundNo += 1
                return True
        else:
            return False

    def print_results(self):
        log.info('=======================================================================================')
        log.info('======================================= RESULTS =======================================')
        log.info('=======================================================================================')
        log.info('Rounds Played: %s', self.roundNo)
        #TODO check these are correct
        for player in self.players:
            log.info('---------------------------------------------------------------------------------------')
            log.info('Player with betting strategy: %s', 
                     ' '.join(str(betting_strategy) for betting_strategy in player.betting_strategies))
            log.info('Starting bank: %s, ending bank: %s, total wagered: %s', player.bankroll, player.bank, player.total_wagered)
            log.info('OVERALL HOUSE EDGE: %s', (player.bankroll - player.bank) / player.total_wagered)
            for bet_type, bet_data in player.all_bets.items():
                house_edge = (bet_data['totalWagered'] - bet_data['totalWon']) / bet_data['totalWagered']
                log.info('***********')
                log.info('%s = {Times=%s, %s=%s, %s=%s, %s=%s, Total Winnings=%s, Total Wagered=%s}', bet_type.name, 
                         bet_data['timesPlaced'], Result.WIN.name, bet_data[Result.WIN], 
                         Result.LOSE.name, bet_data[Result.LOSE], Result.PUSH.name, bet_data[Result.PUSH], 
                         bet_data['totalWon'], bet_data['totalWagered'])
                log.info('HOUSE EDGE: %s', house_edge)

