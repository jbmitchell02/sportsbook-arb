
from odds import MLBDataHandler
from opps import MLBOpportunity


def calc_returns(v1, v2):
    top = v1 * v2
    bottom = v1 + v2
    return (top/bottom) - 1


class MLBArbitrage:
    '''
    Class to handle MLB arbitrage opportunities. Uses MLBDataHandler to get the odds and then finds the opportunities.

    self.opportunities: List of MLBOpportunity objects, sorted by highest returns
    '''

    def __init__(self, apiKey, markets=['h2h', 'spreads', 'totals'], bookmakers='all', regions='us'):
        self.datahandler = MLBDataHandler(apiKey, markets, bookmakers, regions)
        self.opportunities = []

    def update_opps(self, return_threshold=0):
        new_opps = []
        self.datahandler.update_odds()
        mlb_odds = self.datahandler.odds
        for details, odds in mlb_odds.items():
            new_opps += self._find_opps(details, odds, return_threshold)
        new_opps.sort(reverse=True)
        self.opportunities = new_opps

    def _find_opps(self, details, odds, return_threshold):
        '''
        we probably need a better way to do this
        '''
        opps = []
        for i, v1 in enumerate(odds.iloc[:, 1]):
            for j, v2 in enumerate(odds.iloc[:, 2]):
                R = calc_returns(v1, v2)
                if R > return_threshold:
                    market = details[0]
                    home_team = details[1]
                    away_team = details[2]
                    point = 0
                    if market == 'spreads' or market == 'totals':
                        point = details[3]
                    book1 = odds.iloc[i, 0]
                    book2 = odds.iloc[j, 0]
                    opps.append(MLBOpportunity(market, home_team, away_team, point, book1, book2, v1, v2, R))
        return opps

    def print_opps(self):
        for opp in self.opportunities:
            opp.print()
