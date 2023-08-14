
from arb import Opportunity, Arbitrage


def convert_to_american(odds):
    '''
    Convert decimal odds to american odds
    '''
    if odds >= 2:
        return round((odds - 1) * 100)
    else:
        return round(-100 / (odds - 1))
    

class Bet:

    def __init__(self, opp: Opportunity, b1, b2, P):
        self.opp = opp
        self.bet1 = b1
        self.bet2 = b2
        self.profit = P

    def __str__(self):
        result = []
        result.append(str(self.opp.game_details))
        odds1 = '{:+}'.format(convert_to_american(self.opp.odds1))
        odds2 = '{:+}'.format(convert_to_american(self.opp.odds2))
        if self.opp.bet_type == 'h2h':
            result.append(f'H2H (${round(self.profit, 3)})')
            result.append(f'    {self.opp.book1}: {odds1} {self.opp.game_details.home_team}, ${round(self.bet1, 3)}')
            result.append(f'    {self.opp.book2}: {odds2} {self.opp.game_details.away_team}, ${round(self.bet2, 3)}')
        elif self.opp.bet_type == 'spreads':
            spread = '{:+}'.format(self.opp.point)
            result.append(f'Spread {spread} {self.opp.game_details.home_team} (${round(self.profit, 3)})')
            result.append(f'    {self.opp.book1}: {odds1} {self.opp.game_details.home_team}, ${round(self.bet1, 3)}')
            result.append(f'    {self.opp.book2}: {odds2} {self.opp.game_details.away_team}, ${round(self.bet2, 3)}')
        elif self.opp.bet_type == 'totals':
            result.append(f'Total {self.opp.point} (${round(self.profit, 3)})')
            result.append(f'    {self.opp.book1}: {odds1} Over, ${round(self.bet1, 3)}')
            result.append(f'    {self.opp.book2}: {odds2} Under, ${round(self.bet2, 3)}')
        return '\n'.join(result)
    
    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.profit < other.profit
    

class Betting:

    def __init__(self, apiKey, sports, funds, markets=['h2h', 'spreads', 'totals']):
        self.arb = Arbitrage(apiKey, sports, markets)
        self.funds = funds
        self.bets = []
  
    def update_bets(self, return_threshold=0):
        self.bets.clear()
        self.arb.update_opps(return_threshold, sort=False)
        for opp in self.arb.opportunities:
            if opp.book1 in self.funds.keys() and opp.book2 in self.funds.keys():
                b1, b2 = self._calc_bets(opp)
                P = opp.returns * (b1 + b2)
                bet = Bet(opp, b1, b2, P)
                self.bets.append(bet)
        self.bets.sort(reverse=True)

    def print_bets(self):
        for bet in self.bets:
            print(bet)
            print()

    def _calc_bets(self, opp):
        book1 = opp.book1
        book2 = opp.book2
        odds1 = opp.odds1
        odds2 = opp.odds2
        funds1 = self.funds[book1]
        funds2 = self.funds[book2]
        b1 = (odds2 / odds1) * funds2
        b2 = (odds1 / odds2) * funds1
        if b1 > funds1:
            return funds1, b2
        else:
            return b1, funds2


if __name__ == '__main__':
    uva_apiKey = 'acb9ca2b9b8fc48935534934b731019c'
    my_apiKey = '9abea1938e493d654b86a31a14fd2ab6'
    my_sports = [
        #'americanfootball_cfl',
        #'americanfootball_ncaaf',
        #'americanfootball_nfl',
        #'americanfootball_nfl_preseason',
        #'americanfootball_xfl',
        'baseball_mlb',
        #'baseball_mlb_preseason',
        #'baseball_ncaa',
        #'basketball_euroleague',
        #'basketball_nba',
        #'basketball_nba_preseason',
        #'basketball_ncaab',
        #'basketball_wnba',
        #'icehockey_nhl'
        ]
    my_funds = {
        'barstool': 100,
        'draftkings': 100,
        'fanduel': 100
        }
    my_markets = [
        'h2h',
        'spreads',
        'totals'
    ]
    betting = Betting(uva_apiKey, my_sports, my_funds, my_markets)
    betting.update_bets()
    betting.print_bets()
