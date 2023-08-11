
import sqlite3
from odds import GameDetails, OddsHandler


class Opportunity:

    def __init__(self, game_details: GameDetails, bet_type, point, book1, book2, odds1, odds2, returns):
        self.game_details = game_details
        self.bet_type = bet_type
        self.point = point
        self.book1 = book1
        self.book2 = book2
        self.odds1 = odds1
        self.odds2 = odds2
        self.returns = returns
        #self._add_to_db()

    def _add_to_db(self):
        if self.returns > 0:
            conn = sqlite3.connect('opps.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mlb_opps (sport, bet_type, home_team, away_team, point, book1, book2, odds1, odds2, returns)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.game_details.sport_key,
                self.bet_type,
                self.game_details.home_team,
                self.game_details.away_team,
                self.point,
                self.book1,
                self.book2,
                self.odds1,
                self.odds2,
                self.returns))
            conn.commit()
            conn.close()

    def __str__(self):
        result = []
        result.append(str(self.game_details))
        if self.bet_type == 'h2h':
            result.append(f'H2H ({round(self.returns * 100, 3)}%)')
            result.append(f'    {self.book1}: {self.odds1} {self.game_details.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
            result.append(f'    {self.book2}: {self.odds2} {self.game_details.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        elif self.bet_type == 'spreads':
            spread = '{:+}'.format(self.point)
            result.append(f'Spread {spread} {self.game_details.home_team} ({round(self.returns * 100, 3)}%)')
            result.append(f'    {self.book1}: {self.odds1} {self.game_details.home_team}, {round(self.odds2/self.odds1, 3)}*B2')
            result.append(f'    {self.book2}: {self.odds2} {self.game_details.away_team}, {round(self.odds1/self.odds2, 3)}*B1')
        elif self.bet_type == 'totals':
            result.append(f'Total {self.point} ({round(self.returns * 100, 3)}%)')
            result.append(f'    {self.book1}: {self.odds1} Over, {round(self.odds2/self.odds1, 3)}*B2')
            result.append(f'    {self.book2}: {self.odds2} Under, {round(self.odds1/self.odds2, 3)}*B1')
        return '\n'.join(result)
    
    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.returns < other.returns


class Arbitrage:

    def __init__(self, apiKey, sports, bookmakers, markets=['h2h', 'spreads', 'totals']):
        self.oddshandler = OddsHandler(apiKey, sports, bookmakers, markets)
        self.opportunities = []

    def update_opps(self, return_threshold=0, sort=True):
        self.opportunities.clear()
        self.oddshandler.update_odds()
        for key, odds in self.oddshandler.odds.items():
            self._find_opps(key, odds, return_threshold)
        if sort:
            self.opportunities.sort(reverse=True)

    def print_opps(self):
        for opp in self.opportunities:
            print(opp)
            print()
    
    def _find_opps(self, key, odds, return_threshold):
        for i, v1 in enumerate(odds.iloc[:, 1]):
            for j, v2 in enumerate(odds.iloc[:, 2]):
                R = self._calc_returns(v1, v2)
                if R > return_threshold:
                    game_details, bet_type, point = key
                    book1 = odds.iloc[i, 0]
                    book2 = odds.iloc[j, 0]
                    opp = Opportunity(game_details, bet_type, point, book1, book2, v1, v2, R)
                    self.opportunities.append(opp)

    def _calc_returns(self, v1, v2):
        top = v1 * v2
        bottom = v1 + v2
        return (top/bottom) - 1
