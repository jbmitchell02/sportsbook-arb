class MLBOpportunity:
    def __init__(self, market, home_team, away_team, point, book1, book2, odds1, odds2, returns):
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
            self._print_h2h()
        elif self.market == 'spreads':
            self._print_spreads()
        elif self.market == 'totals':
            self._print_totals()

    def _print_h2h(self):
        print(f'H2H: {self.away_team} @ {self.home_team} - {round(self.returns*100, 3)}%')
        print(f'    {self.book1}: {self.odds1} {self.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
        print(f'    {self.book2}: {self.odds2} {self.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        print()

    def _print_spreads(self):
        print(f'Spread {self.point}: {self.away_team} @ {self.home_team} - {round(self.returns*100, 3)}%')
        print(f'    {self.book1}: {self.odds1} {self.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
        print(f'    {self.book2}: {self.odds2} {self.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        print()

    def _print_totals(self):
        print(f'Total {self.point}: {self.away_team} @ {self.home_team} - {round(self.returns*100, 3)}%')
        print(f'    {self.book1}: {self.odds1} {self.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
        print(f'    {self.book2}: {self.odds2} {self.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        print()

    def __lt__(self, other):
        return self.returns < other.returns