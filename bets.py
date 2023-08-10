
from arb import MLBArbitrage


def convert_to_american(odds):
    '''
    Convert decimal odds to american odds
    '''
    if odds >= 2:
        return round((odds - 1) * 100)
    else:
        return round(-100 / (odds - 1))


class MLBBet:

    def __init__(self, opp, b1, b2, P):
        self.opp = opp
        self.bet1 = b1
        self.bet2 = b2
        self.profit = P
    
    def print(self):
        opp = self.opp
        market = opp.market
        if market == 'h2h':
            print(f'H2H: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        elif market == 'spreads':
            spread = '{:+}'.format(opp.point)
            print(f'Spread {spread}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        elif market == 'totals':
            total = '{:+}'.format(opp.point)
            print(f'Total {total}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        odds1 = '{:+}'.format(convert_to_american(opp.odds1))
        odds2 = '{:+}'.format(convert_to_american(opp.odds2))
        print(f'    {opp.book1}: {odds1} {opp.home_team}, ${round(self.bet1, 3)}')
        print(f'    {opp.book2}: {odds2} {opp.away_team}, ${round(self.bet2, 3)}')
        print()

    def __lt__(self, other):
        return self.profit < other.profit


class MLBBetting:
    '''
    get live bets with this
    '''

    def __init__(self, apiKey, funds, markets=['h2h', 'spreads', 'totals'], regions='us'):
        self.arb = MLBArbitrage(apiKey, markets, ','.join(funds.keys()), regions)
        self.funds = funds
        self.bets = []

    def update_bets(self, return_threshold=0):
        self.bets = []
        self.arb.update_opps(return_threshold)
        for opp in self.arb.opportunities:
            b1, b2 = self._calc_bets(opp)
            P = opp.returns * (b1 + b2)
            self.bets.append(MLBBet(opp, b1, b2, P))
        self.bets.sort(reverse=True)

    def _calc_bets(self, opp):
        '''
        idk if this is right
        '''
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
        
    def print_bets(self):
        for bet in self.bets:
            bet.print()
