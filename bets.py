
from arb import MLBArbitrage


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
            self._print_h2h(opp)
        elif market == 'spreads':
            self._print_spreads(opp)
        elif market == 'totals':
            self._print_totals(opp)

    def _print_h2h(self, opp):
        print(f'H2H: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        print(f'    {opp.book1}: {opp.odds1} {opp.home_team}, ${round(self.bet1, 3)}')
        print(f'    {opp.book2}: {opp.odds2} {opp.away_team}, ${round(self.bet2, 3)}')
        print()
    
    def _print_spreads(self, opp):
        print(f'Spread {opp.point}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        print(f'    {opp.book1}: {opp.odds1} {opp.home_team}, ${round(self.bet1, 3)}')
        print(f'    {opp.book2}: {opp.odds2} {opp.away_team}, ${round(self.bet2, 3)}')
        print()

    def _print_totals(self, opp):
        print(f'Total {opp.point}: {opp.away_team} @ {opp.home_team} ${round(self.profit, 3)}')
        print(f'    {opp.book1}: {opp.odds1} {opp.home_team}, ${round(self.bet1, 3)}')
        print(f'    {opp.book2}: {opp.odds2} {opp.away_team}, ${round(self.bet2, 3)}')
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
