
from arb import Arbitrage


def convert_to_american(odds):
    '''
    Convert decimal odds to american odds
    '''
    if odds >= 2:
        return round((odds - 1) * 100)
    else:
        return round(-100 / (odds - 1))
    

class Bet:

    def __init__(self, opp, b1, b2, P):
        self.opp = opp
        self.bet1 = b1
        self.bet2 = b2
        self.profit = P

    def print(self):
        opp = self.opp
        market = opp.market
        odds1 = '{:+}'.format(convert_to_american(opp.odds1))
        odds2 = '{:+}'.format(convert_to_american(opp.odds2))
        print(opp.sport)
        if market == 'h2h':
            print(f'H2H: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
            print(f'    {opp.book1}: {odds1} {opp.home_team}, ${round(self.bet1, 3)}')
            print(f'    {opp.book2}: {odds2} {opp.away_team}, ${round(self.bet2, 3)}')
        elif market == 'spreads':
            spread = '{:+}'.format(opp.point)
            print
            print(f'Spread {spread}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
            print(f'    {opp.book1}: {odds1} {opp.home_team}, ${round(self.bet1, 3)}')
            print(f'    {opp.book2}: {odds2} {opp.away_team}, ${round(self.bet2, 3)}')
        elif market == 'totals':
            print(f'Total {opp.point}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
            print(f'    {opp.book1}: {odds1} Over, ${round(self.bet1, 3)}')
            print(f'    {opp.book2}: {odds2} Under, ${round(self.bet2, 3)}')
        print()

    def __lt__(self, other):
        return self.profit < other.profit
    

class Betting:

    def __init__(self, apiKey, sports, funds, markets=['h2h', 'spreads', 'totals']):
        self.arb = Arbitrage(apiKey, sports, funds.keys(), markets)
        self.funds = funds
        self.bets = []

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
        
    def update_bets(self, return_threshold=0):
        self.bets = []
        self.arb.update_opps(return_threshold, sort=False)
        for opp in self.arb.opportunities:
            b1, b2 = self._calc_bets(opp)
            P = opp.returns * (b1 + b2)
            self.bets.append(Bet(opp, b1, b2, P))
        self.bets.sort(reverse=True)

    def print_bets(self):
        for bet in self.bets:
            bet.print()


if __name__ == '__main__':
    uva_apiKey = 'acb9ca2b9b8fc48935534934b731019c'
    my_apiKey = '9abea1938e493d654b86a31a14fd2ab6'
    sports = [
        #'baseball_mlb',
        #'americanfootball_nfl_preseason'
        ]
    my_funds = {
        'barstool': 100,
        'draftkings': 100,
        'fanduel': 100
        }
    betting = Betting(my_apiKey, sports, my_funds)
    betting.update_bets(-0.02)
    betting.print_bets()
