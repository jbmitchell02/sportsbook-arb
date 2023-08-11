
from odds import DataHandler


class Opportunity:

    def __init__(self, sport, market, home_team, away_team, point, book1, book2, odds1, odds2, returns):
        self.sport = sport
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
        print(self.sport)
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


class Arbitrage:

    def __init__(self, apiKey, sports, bookmakers, markets=['h2h', 'spreads', 'totals']):
        self.datahandler = DataHandler(apiKey, sports, bookmakers, markets)
        self.opportunities = []

    def _calc_returns(self, v1, v2):
        top = v1 * v2
        bottom = v1 + v2
        return (top/bottom) - 1
    
    def _find_opps(self, details, odds, return_threshold):
        for i, v1 in enumerate(odds.iloc[:, 1]):
            for j, v2 in enumerate(odds.iloc[:, 2]):
                R = self._calc_returns(v1, v2)
                if R > return_threshold:
                    sport = details[0]
                    market = details[1]
                    home_team = details[2]
                    away_team = details[3]
                    point = 0
                    if market == 'spreads' or market == 'totals':
                        point = details[4]
                    book1 = odds.iloc[i, 0]
                    book2 = odds.iloc[j, 0]
                    opp = Opportunity(sport, market, home_team, away_team, point, book1, book2, v1, v2, R)
                    self.opportunities.append(opp)

    def update_opps(self, return_threshold=0, sort=True):
        self.opportunities = []
        self.datahandler.update_odds()
        for details, odds in self.datahandler.odds.items():
            self._find_opps(details, odds, return_threshold)
        if sort:
            self.opportunities.sort(reverse=True)

    def print_opps(self):
        for opp in self.opportunities:
            opp.print()
