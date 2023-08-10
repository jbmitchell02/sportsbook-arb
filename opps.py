

class MLBOpportunity:
    '''
    Class to hold MLB arbitrage opportunities.
    '''

    def __init__(self, market, home_team, away_team, point, book1, book2, odds1, odds2, returns):
        '''
        market: 'h2h', 'spreads', or 'totals'
        point: 0 for h2h, home team spread for spreads, total for totals
        '''
        self.market = market
        self.home_team = home_team
        self.away_team = away_team
        self.point = point
        self.book1 = book1
        self.book2 = book2
        self.odds1 = odds1
        self.odds2 = odds2
        self.returns = returns

    def print(self):
        if self.market == 'h2h':
            print(f'H2H: {self.away_team} @ {self.home_team} {round(self.returns*100, 3)}%')
            print(f'    {self.book1}: {self.odds1} {self.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
            print(f'    {self.book2}: {self.odds2} {self.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        elif self.market == 'spreads':
            spread = '{:+}'.format(self.point)
            print(f'Spread {spread}: {self.away_team} @ {self.home_team} {round(self.returns*100, 3)}%')
            print(f'    {self.book1}: {self.odds1} {self.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
            print(f'    {self.book2}: {self.odds2} {self.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        elif self.market == 'totals':
            print(f'Total {self.point}: {self.away_team} @ {self.home_team} {round(self.returns*100, 3)}%')
            print(f'    {self.book1}: {self.odds1} Over, {round(self.odds2/self.odds1, 3)}*B2')
            print(f'    {self.book2}: {self.odds2} Under, {round(self.odds1/self.odds2, 3)}*B1')
        print()

    def __lt__(self, other):
        return self.returns < other.returns
